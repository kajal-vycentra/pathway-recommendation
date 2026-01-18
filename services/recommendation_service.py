import json
import logging
import asyncio
import httpx
from typing import Dict, Optional, Tuple
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from config import settings
from cache import RedisCache
from models import (
    EntryType,
    PathwayRecommendation,
    DetectedProfile,
    RecommendationRequest,
)
from db_models import (
    User,
    QuestionnaireResponse,
    PathwayRecommendationRecord,
)

logger = logging.getLogger(__name__)


class RecommendationService:
    """
    Scalable service for generating pathway recommendations.

    Features:
    - Fully async database operations (non-blocking)
    - Connection pooling with httpx
    - In-memory caching for similar answer patterns
    - Optimized for concurrent requests
    - Sends BOTH questions AND answers to AI for accurate analysis
    """

    SYSTEM_PROMPT = """You are LogosReach Pathway Recommendation AI.

Your role:
Analyze structured questionnaire answers and recommend ONE pathway from the predefined list only.

You must:
- Use spiritual, emotional, and intent understanding
- NOT use hardcoded scoring
- NOT invent new pathways
- Choose ONLY from the pathways provided below
- Act like a compassionate spiritual counselor
- Base decision on overall pattern, not single answer
- Carefully read BOTH the question and the answer to understand context

AVAILABLE PATHWAYS:

1. Discovering Jesus (7-10 days)
   Theme: seeker, new to Christianity, not familiar with Jesus, curiosity about faith

2. New Believer Foundations (14 days)
   Theme: recently believed, needs basics of faith

3. Water Baptism (7 days)
   Theme: baptism, public declaration of faith

4. Growing in Prayer (7 days)
   Theme: learning to pray, anxiety, peace, trusting God

5. Understanding the Bible (10-14 days)
   Theme: confused about scripture, wants deeper context

6. Finding Purpose & Calling (14-21 days)
   Theme: purpose, calling, career direction, meaning in life

7. Marriage & Relationships (14-21 days)
   Theme: marriage issues, relationship struggles, family

8. Parenting with Faith (14 days)
   Theme: parenting, raising children, family faith

9. Overcoming Anxiety (10-14 days)
   Theme: worry, fear, need peace, anxiety, stress

10. Healing from Grief (21-30 days)
    Theme: loss, grief, mourning, bereavement

11. Financial Stewardship (14-21 days)
    Theme: finances, money management, stewardship, debt

12. Crisis Support (Variable)
    Theme: urgent help, hopelessness, fear, crisis, emergency

ANALYSIS CRITERIA:

1. Spiritual Stage
   - seeker: New to Christianity, doesn't know Jesus
   - new_believer: Recently accepted faith, needs foundation
   - growing_believer: Active in faith, wants to grow deeper
   - struggling_believer: Knows faith but facing challenges, distant

2. Emotional Signals
   - anxious: Worried, fearful, stressed
   - confused: Uncertain, needs clarity
   - curious: Open to learning, exploring
   - painful: Hurting, grieving
   - open: Receptive, willing
   - hopeful: Positive outlook
   - distressed: Urgent need, crisis

3. Knowledge Level
   - Familiarity with Jesus (from questions about teachings)
   - Bible exposure (from reading frequency questions)
   - Prayer life (from prayer habit questions)

4. Primary Need
   - salvation: Needs to know Jesus
   - peace: Needs calm, anxiety relief
   - understanding: Needs Bible knowledge
   - purpose: Needs direction, calling
   - healing: Needs emotional/spiritual healing
   - growth: Needs to deepen faith
   - guidance: Needs wisdom for decisions

OUTPUT FORMAT:
You MUST return ONLY valid JSON with this exact structure (no markdown, no explanation outside JSON):

{
  "recommended_pathway": "Pathway Name (duration)",
  "confidence": 0.85,
  "detected_profile": {
    "spiritual_stage": "seeker|new_believer|growing_believer|struggling_believer",
    "primary_need": "salvation|peace|understanding|purpose|healing|growth|guidance",
    "emotional_state": "anxious|confused|curious|painful|open|hopeful|distressed"
  },
  "reasoning": "2-3 sentences explaining the decision based on the specific questions and answers",
  "next_step_message": "Encouraging message to the user about starting their pathway"
}"""

    # Shared HTTP client for connection pooling
    _http_client: Optional[httpx.AsyncClient] = None

    # Cache for questions.json (loaded once)
    _questions_data: Optional[Dict] = None

    def __init__(self):
        self.api_key = settings.OPENROUTER_API_KEY
        self.base_url = settings.OPENROUTER_BASE_URL
        self.model = settings.AI_MODEL

    @classmethod
    def _load_questions(cls) -> Dict:
        """Load questions from JSON file (cached)."""
        if cls._questions_data is None:
            try:
                with open("questions.json", "r", encoding="utf-8") as f:
                    cls._questions_data = json.load(f)
            except FileNotFoundError:
                cls._questions_data = {"flows": {}}
        return cls._questions_data

    @classmethod
    async def get_http_client(cls) -> httpx.AsyncClient:
        """Get or create shared HTTP client with connection pooling."""
        if cls._http_client is None or cls._http_client.is_closed:
            cls._http_client = httpx.AsyncClient(
                timeout=30.0,
                limits=httpx.Limits(
                    max_keepalive_connections=20,
                    max_connections=100,
                    keepalive_expiry=30.0
                )
            )
        return cls._http_client

    @classmethod
    async def close_http_client(cls):
        """Close shared HTTP client (call on shutdown)."""
        if cls._http_client is not None:
            await cls._http_client.aclose()
            cls._http_client = None

    def _get_question_text(self, entry_type: str, question_key: str) -> str:
        """
        Get the actual question text for a given question key.

        Args:
            entry_type: 'yes_i_know' or 'no_im_new'
            question_key: e.g., 'Q1', 'Q2', etc.

        Returns:
            The full question text or the key if not found
        """
        questions_data = self._load_questions()

        # Extract question number from key (Q1 -> 1, Q2 -> 2, etc.)
        try:
            q_num = int(question_key.replace("Q", "").replace("q", ""))
        except ValueError:
            return question_key

        # Get questions for this entry type
        flow = questions_data.get("flows", {}).get(entry_type, {})
        questions = flow.get("questions", [])

        # Find the question with matching number
        for q in questions:
            if q.get("question_number") == q_num:
                return q.get("question", question_key)

        return question_key

    async def _get_or_create_user(
        self, db: AsyncSession, external_user_id: Optional[str] = None
    ) -> User:
        """Get existing user or create a new one (async)."""
        if external_user_id:
            result = await db.execute(
                select(User).where(User.external_user_id == external_user_id)
            )
            user = result.scalar_one_or_none()
            if user:
                return user

        # Create new user
        user = User(external_user_id=external_user_id)
        db.add(user)
        await db.commit()
        await db.refresh(user)
        return user

    async def _store_questionnaire_response(
        self,
        db: AsyncSession,
        user: User,
        entry_type: str,
        answers: Dict[str, str]
    ) -> QuestionnaireResponse:
        """Store questionnaire answers in database (async)."""
        response = QuestionnaireResponse(
            user_id=user.id,
            entry_type=entry_type,
            answers=answers
        )
        db.add(response)
        await db.commit()
        await db.refresh(response)
        return response

    async def _store_recommendation(
        self,
        db: AsyncSession,
        user: User,
        questionnaire_response: QuestionnaireResponse,
        recommendation: PathwayRecommendation,
        raw_response: Dict
    ) -> PathwayRecommendationRecord:
        """Store AI recommendation in database (async)."""
        record = PathwayRecommendationRecord(
            user_id=user.id,
            questionnaire_response_id=questionnaire_response.id,
            recommended_pathway=recommendation.recommended_pathway,
            confidence=recommendation.confidence,
            spiritual_stage=recommendation.detected_profile.spiritual_stage,
            primary_need=recommendation.detected_profile.primary_need,
            emotional_state=recommendation.detected_profile.emotional_state,
            reasoning=recommendation.reasoning,
            next_step_message=recommendation.next_step_message,
            raw_ai_response=raw_response
        )
        db.add(record)
        await db.commit()
        await db.refresh(record)
        return record

    def _format_user_prompt(self, request: RecommendationRequest) -> str:
        """
        Format the user's answers WITH the actual questions for AI context.

        This is critical! The AI needs to know WHAT was asked to understand
        what the answer means. For example:
        - "Yes" to "Are you interested in Christianity?" = positive indicator
        - "Yes" to "Are you in crisis?" = urgent need

        Without the question, "Yes" is meaningless.
        """
        entry_type_value = request.entry_type.value

        # Determine entry type label
        if request.entry_type == EntryType.YES_I_KNOW:
            entry_label = "Existing Believer (Has knowledge of Christianity)"
            entry_context = "This user already knows about Christianity and the Bible. They are looking to grow deeper in their faith or address specific spiritual needs."
        else:
            entry_label = "New to Christianity (No prior knowledge)"
            entry_context = "This user is new to Christianity and exploring faith for the first time. They may be a seeker or someone curious about spiritual matters."

        # Build Q&A pairs with FULL question text
        qa_pairs = []
        for key, answer in sorted(request.answers.items()):
            question_text = self._get_question_text(entry_type_value, key)
            qa_pairs.append(f"Q: {question_text}\nA: {answer}")

        qa_text = "\n\n".join(qa_pairs)

        return f"""USER PROFILE:
Entry Type: {entry_label}
Context: {entry_context}

QUESTIONNAIRE RESPONSES:
========================
{qa_text}
========================

INSTRUCTIONS:
Based on the above questions and answers, analyze this user's:
1. Spiritual Stage - Where are they in their faith journey?
2. Emotional State - What emotions or feelings do their answers reveal?
3. Primary Need - What is their most pressing spiritual need?

Then recommend the BEST matching pathway from the provided list.
Return your response in the exact JSON format specified."""

    async def _call_ai_api_with_retry(self, user_prompt: str) -> Dict:
        """
        Call OpenRouter AI API with retry logic for resilience.

        Retries on:
        - Connection errors
        - Timeout errors
        - 5xx server errors
        - 429 rate limit errors
        """
        last_exception = None

        for attempt in range(settings.AI_MAX_RETRIES):
            try:
                return await self._call_ai_api_once(user_prompt)
            except httpx.TimeoutException as e:
                last_exception = e
                logger.warning(f"AI API timeout (attempt {attempt + 1}/{settings.AI_MAX_RETRIES}): {e}")
            except httpx.ConnectError as e:
                last_exception = e
                logger.warning(f"AI API connection error (attempt {attempt + 1}/{settings.AI_MAX_RETRIES}): {e}")
            except httpx.HTTPStatusError as e:
                if e.response.status_code in (429, 500, 502, 503, 504):
                    last_exception = e
                    logger.warning(f"AI API error {e.response.status_code} (attempt {attempt + 1}/{settings.AI_MAX_RETRIES})")
                else:
                    raise  # Don't retry on 4xx errors (except 429)
            except Exception as e:
                last_exception = e
                logger.error(f"Unexpected AI API error (attempt {attempt + 1}/{settings.AI_MAX_RETRIES}): {e}")

            # Wait before retry with exponential backoff
            if attempt < settings.AI_MAX_RETRIES - 1:
                wait_time = settings.AI_RETRY_DELAY * (2 ** attempt)
                logger.info(f"Retrying in {wait_time}s...")
                await asyncio.sleep(wait_time)

        raise Exception(f"AI API failed after {settings.AI_MAX_RETRIES} attempts: {last_exception}")

    async def _call_ai_api_once(self, user_prompt: str) -> Dict:
        """Single AI API call (used by retry wrapper)."""
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": self.SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt}
            ],
            "temperature": 0.3,
            "max_tokens": 500,
        }

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://logosreach.com",
            "X-Title": "LogosReach Pathway Recommendation"
        }

        client = await self.get_http_client()
        response = await client.post(
            self.base_url,
            json=payload,
            headers=headers
        )
        response.raise_for_status()

        result = response.json()
        ai_content = result["choices"][0]["message"]["content"]
        return self._parse_ai_response(ai_content)

    async def get_recommendation(
        self,
        request: RecommendationRequest,
        db: AsyncSession
    ) -> Tuple[PathwayRecommendation, str, str]:
        """
        Get pathway recommendation from OpenRouter AI and store in database.

        Optimized for scalability:
        - Async database operations
        - Redis caching shared across workers
        - Connection pooling for AI API calls
        - Retry logic for AI API resilience
        - Sends BOTH questions AND answers to AI

        Args:
            request: The recommendation request with entry type and answers
            db: Async database session

        Returns:
            Tuple of (PathwayRecommendation, user_id, recommendation_id)
        """
        if not self.api_key:
            raise ValueError("OPENROUTER_API_KEY is not set. Please set it in environment variables.")

        # 1. Get or create user (async)
        user = await self._get_or_create_user(db, request.user_id)

        # 2. Store questionnaire answers (async)
        questionnaire_response = await self._store_questionnaire_response(
            db,
            user,
            request.entry_type.value,
            request.answers
        )

        # 3. Check Redis cache for similar answer patterns
        cache_key = RedisCache.generate_cache_key(request.entry_type.value, request.answers)
        recommendation_data = await RedisCache.get(cache_key)

        if recommendation_data is None:
            # Cache miss - call AI API with retry logic
            logger.info(f"Cache miss for key {cache_key[:16]}..., calling AI API")
            user_prompt = self._format_user_prompt(request)
            recommendation_data = await self._call_ai_api_with_retry(user_prompt)
            # Store in Redis cache
            await RedisCache.set(cache_key, recommendation_data)
            logger.info(f"Cached response for key {cache_key[:16]}...")
        else:
            logger.info(f"Cache hit for key {cache_key[:16]}...")

        # 4. Create recommendation object
        recommendation = PathwayRecommendation(
            recommended_pathway=recommendation_data["recommended_pathway"],
            confidence=recommendation_data["confidence"],
            detected_profile=DetectedProfile(
                spiritual_stage=recommendation_data["detected_profile"]["spiritual_stage"],
                primary_need=recommendation_data["detected_profile"]["primary_need"],
                emotional_state=recommendation_data["detected_profile"]["emotional_state"]
            ),
            reasoning=recommendation_data["reasoning"],
            next_step_message=recommendation_data["next_step_message"]
        )

        # 5. Store recommendation in database (async)
        recommendation_record = await self._store_recommendation(
            db,
            user,
            questionnaire_response,
            recommendation,
            recommendation_data
        )

        return recommendation, str(user.id), str(recommendation_record.id)

    def _parse_ai_response(self, content: str) -> Dict:
        """Parse the AI response content to extract JSON."""
        content = content.strip()

        if content.startswith("```json"):
            content = content[7:]
        elif content.startswith("```"):
            content = content[3:]

        if content.endswith("```"):
            content = content[:-3]

        content = content.strip()

        try:
            return json.loads(content)
        except json.JSONDecodeError as e:
            start_idx = content.find("{")
            end_idx = content.rfind("}") + 1

            if start_idx != -1 and end_idx > start_idx:
                json_str = content[start_idx:end_idx]
                return json.loads(json_str)

            raise ValueError(f"Failed to parse AI response as JSON: {e}")

    async def get_user_history(self, db: AsyncSession, external_user_id: str) -> list:
        """Get user's recommendation history (async)."""
        result = await db.execute(
            select(User).where(User.external_user_id == external_user_id)
        )
        user = result.scalar_one_or_none()

        if not user:
            return []

        result = await db.execute(
            select(PathwayRecommendationRecord)
            .where(PathwayRecommendationRecord.user_id == user.id)
            .order_by(PathwayRecommendationRecord.created_at.desc())
        )
        recommendations = result.scalars().all()

        return [
            {
                "id": str(rec.id),
                "recommended_pathway": rec.recommended_pathway,
                "confidence": rec.confidence,
                "spiritual_stage": rec.spiritual_stage,
                "primary_need": rec.primary_need,
                "emotional_state": rec.emotional_state,
                "reasoning": rec.reasoning,
                "created_at": rec.created_at.isoformat()
            }
            for rec in recommendations
        ]
