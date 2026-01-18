# LogosReach Pathway Recommendation System

## Simple Documentation

---

## Overview

The Pathway Recommendation System analyzes user questions and automatically suggests the most appropriate spiritual pathway for their journey.

**Flow:** ask Question → AI Analysis → Pathway Suggestion → User Enrollment

---

## How It Works

### Step 1: Asks Question

Ask the question to the user:
-What spiritual guidance or help are you seeking today?

### Step 2: AI Analysis

The system analyzes:

- **Keywords** - Specific words in the question
- **Topics** - Main subject (salvation, prayer, marriage, etc.)
- **Intent** - What the user really needs
- **Sentiment** - User's emotional state

### Step 3: Classify Question

Based on analysis, system categorizes the question:

- Salvation/Gospel
- Prayer
- Bible Study
- Relationships
- Anxiety/Fear
- Financial Issues
- Grief/Loss
- Parenting
- Purpose/Calling
- Crisis

### Step 4: Match to Pathway

System recommends the best pathway with confidence score.

### Step 5: Present to User

User receives:

- Pathway name
- What it covers
- Duration (7-30 days)
- Daily structure
- Expected outcomes

### Step 6: Enrollment

User can:

- ✅ Accept and start pathway
- 🔄 View alternative pathways
- 💾 Save for later

---

## Available Pathways (12 Core)

### 1. Discovering Jesus (7-10 days)

**For:** Seekers, non-believers
**Keywords:** salvation, saved, gospel, accept christ, who is jesus
**Covers:** Introduction to Christianity, Gospel message

### 2. New Believer Foundations (14 days)

**For:** New Christians (0-6 months)
**Keywords:** new christian, just saved, baptism, next steps
**Covers:** Basic Christian living, prayer, bible reading

### 3. Water Baptism (7 days)

**For:** Believers considering baptism
**Keywords:** baptism, baptized, water baptism
**Covers:** Baptism meaning, preparation, commitment

### 4. Growing in Prayer (7 days)

**For:** Anyone wanting to pray better
**Keywords:** how to pray, prayer help, teach me to pray
**Covers:** Prayer basics, building prayer life

### 5. Understanding the Bible (10-14 days)

**For:** Anyone wanting to study Scripture
**Keywords:** bible study, understand bible, scripture
**Covers:** How to read and study the Bible

### 6. Finding Purpose & Calling (14-21 days)

**For:** Seeking life direction
**Keywords:** purpose, calling, what should i do, direction
**Covers:** Discovering God's plan for your life

### 7. Marriage & Relationships (14-21 days)

**For:** Married couples or engaged
**Keywords:** marriage, spouse, relationship, conflict
**Covers:** Biblical marriage, communication, conflict

### 8. Parenting with Faith (14 days)

**For:** Parents
**Keywords:** parenting, kids, children, raising kids
**Covers:** Biblical parenting, family discipleship

### 9. Overcoming Anxiety (10-14 days)

**For:** Struggling with anxiety/fear
**Keywords:** anxiety, worry, fear, stressed, panic
**Covers:** Finding peace, trusting God, managing anxiety

### 10. Healing from Grief (21-30 days)

**For:** Experiencing loss
**Keywords:** grief, loss, death, died, mourning
**Covers:** Processing grief, finding hope, healing

### 11. Financial Stewardship (14-21 days)

**For:** Financial struggles or questions
**Keywords:** money, finances, debt, financial stress
**Covers:** Biblical finances, stewardship, budgeting

### 12. Crisis Support (Variable)

**For:** Emergency situations
**Keywords:** crisis, help, emergency, desperate
**Covers:** Immediate support, safety, resources

---

## Additional Prayer Pathways

### 13. Deeper Walk with God (14 days)

**For:** Spiritual breakthrough
**Keywords:** breakthrough, deeper, more of god, hungry

### 14. Finding Peace (10 days)

**For:** Anxiety through prayer
**Keywords:** peace, calm, rest, stillness

### 15. Trusting God's Timing (7 days)

**For:** Unanswered prayers
**Keywords:** waiting, unanswered, why hasn't god, timing

### 16. Intercessory Prayer (10 days)

**For:** Praying for others
**Keywords:** pray for others, intercession, prayer warrior

---

## Keyword Matching Examples

### Example 1: Salvation Question

**User:** "How do I become a Christian?"
**Keywords Detected:** become, christian
**Category:** Salvation/Gospel
**Recommended:** Pathway 1 - Discovering Jesus
**Confidence:** 95%

### Example 2: Anxiety Question

**User:** "I'm so anxious all the time, can prayer help?"
**Keywords Detected:** anxious, prayer help
**Category:** Anxiety + Prayer
**Recommended:** Pathway 9 - Overcoming Anxiety
**Alternative:** Pathway 14 - Finding Peace
**Confidence:** 90%

### Example 3: Marriage Question

**User:** "My marriage is struggling, we keep fighting"
**Keywords Detected:** marriage, struggling, fighting
**Category:** Relationships
**Recommended:** Pathway 7 - Marriage & Relationships
**Confidence:** 92%

### Example 4: Purpose Question

**User:** "I don't know what God wants me to do with my life"
**Keywords Detected:** what god wants, life, do
**Category:** Purpose/Calling
**Recommended:** Pathway 6 - Finding Purpose & Calling
**Confidence:** 88%

### Example 5: Multiple Topics

**User:** "I just lost my job and I'm really anxious about money"
**Keywords Detected:** lost job, anxious, money
**Categories:** Anxiety + Financial
**Recommended:** Pathway 11 - Financial Stewardship
**Alternative:** Pathway 9 - Overcoming Anxiety
**Confidence:** 85%

---

## System Logic

### Confidence Scoring

- **90-100%** - Very confident match, single clear pathway
- **75-89%** - Confident match, offer alternatives
- **60-74%** - Moderate match, show multiple options
- **Below 60%** - Ask clarifying questions

### Priority Rules

1. **Crisis keywords** → Always route to Crisis Support first
2. **Salvation seekers** → Discovering Jesus or New Believer
3. **Single clear topic** → Direct pathway match
4. **Multiple topics** → Recommend primary, show alternatives
5. **Unclear question** → Ask for clarification

---

## User Experience Flow

### Initial Recommendation

```
AI: "Based on your question about [topic], I recommend
the '[Pathway Name]' pathway. This [duration]-day journey
will help you [benefit].

Would you like to:
1. ✅ Start this pathway now
2. 🔍 See other pathway options
3. ℹ️ Learn more about this pathway
4. 💬 Ask me more questions first"
```

### User Accepts

```
AI: "Great! You're enrolled in '[Pathway Name]'.

Here's what to expect:
• Day 1 starts now with [topic]
• Daily content takes 10-15 minutes
• You'll receive reminders each day
• Complete at your own pace

Let's begin with Day 1..."
```

### User Wants Alternatives

```
AI: "Here are other pathways that might help:

1. [Alternative 1] - [duration] days
   Focuses on [topic]

2. [Alternative 2] - [duration] days
   Focuses on [topic]

Which interests you?"
```

---

## Technical Implementation

### Input Processing

```python
def analyze_question(user_question: str):
    # 1. Extract keywords
    keywords = extract_keywords(user_question)

    # 2. Identify topics
    topics = identify_topics(keywords)

    # 3. Determine intent
    intent = determine_intent(user_question, topics)

    # 4. Calculate sentiment
    sentiment = analyze_sentiment(user_question)

    return {
        'keywords': keywords,
        'topics': topics,
        'intent': intent,
        'sentiment': sentiment
    }
```

### Pathway Matching

```python
def recommend_pathway(analysis):
    # 1. Check for crisis first
    if is_crisis(analysis):
        return CRISIS_PATHWAY

    # 2. Match keywords to pathways
    matches = []
    for pathway in ALL_PATHWAYS:
        score = calculate_match_score(analysis, pathway)
        matches.append((pathway, score))

    # 3. Sort by confidence
    matches.sort(key=lambda x: x[1], reverse=True)

    # 4. Return top match with alternatives
    return {
        'primary': matches[0],
        'alternatives': matches[1:3],
        'confidence': matches[0][1]
    }
```

### Match Score Calculation

```python
def calculate_match_score(analysis, pathway):
    score = 0.0

    # Keyword matching (50% weight)
    keyword_matches = count_keyword_matches(
        analysis['keywords'],
        pathway.keywords
    )
    score += (keyword_matches / len(pathway.keywords)) * 0.5

    # Topic relevance (30% weight)
    topic_relevance = calculate_topic_relevance(
        analysis['topics'],
        pathway.category
    )
    score += topic_relevance * 0.3

    # Intent alignment (20% weight)
    intent_match = check_intent_alignment(
        analysis['intent'],
        pathway.purpose
    )
    score += intent_match * 0.2

    return score
```

---

## JSON Output Examples

### Example 1: Anxiety Question

**User Input:**

```json
{
  "user_id": "user_12345",
  "question": "I'm so anxious all the time, I can't sleep",
  "timestamp": "2026-01-16T10:30:00Z"
}
```

**System Output:**

```json
{
  "analysis": {
    "keywords": ["anxious", "all the time", "can't sleep"],
    "topics": ["anxiety", "sleep", "worry"],
    "intent": "seeking_help_with_anxiety",
    "sentiment": {
      "score": 35,
      "label": "distressed"
    }
  },
  "recommendation": {
    "primary_pathway": {
      "id": 9,
      "name": "Overcoming Anxiety",
      "pathway_type": "OVERCOMING_ANXIETY",
      "description": "Finding peace through faith and practical steps to manage anxiety",
      "duration_days": 14,
      "confidence_score": 0.92,
      "reasoning": "High keyword match for anxiety symptoms and sleep issues",
      "daily_time_commitment": "10-15 minutes",
      "start_date": "2026-01-16",
      "end_date": "2026-01-30"
    },
    "alternative_pathways": [
      {
        "id": 14,
        "name": "Finding Peace (Prayer Pathway)",
        "pathway_type": "FINDING_PEACE",
        "description": "Prayer-focused approach to anxiety and worry",
        "duration_days": 10,
        "confidence_score": 0.78,
        "reasoning": "Prayer-based alternative for anxiety relief"
      },
      {
        "id": 4,
        "name": "Growing in Prayer",
        "pathway_type": "GROWING_IN_PRAYER",
        "description": "Develop a prayer life that brings peace",
        "duration_days": 7,
        "confidence_score": 0.65,
        "reasoning": "Prayer can help manage anxiety symptoms"
      }
    ]
  },
  "next_steps": [
    "Review pathway overview",
    "Accept or select alternative",
    "Begin Day 1 content"
  ],
  "status": "awaiting_user_response",
  "expires_at": "2026-01-23T10:30:00Z"
}
```

---

### Example 2: Salvation Question

**User Input:**

```json
{
  "user_id": "user_67890",
  "question": "How do I become a Christian? What does it mean to be saved?",
  "timestamp": "2026-01-16T14:20:00Z"
}
```

**System Output:**

```json
{
  "analysis": {
    "keywords": ["become christian", "saved", "what does it mean"],
    "topics": ["salvation", "gospel", "conversion"],
    "intent": "seeking_salvation",
    "sentiment": {
      "score": 70,
      "label": "curious_and_open"
    }
  },
  "recommendation": {
    "primary_pathway": {
      "id": 1,
      "name": "Discovering Jesus",
      "pathway_type": "DISCOVERING_JESUS",
      "description": "An introduction to who Jesus is and the Gospel message",
      "duration_days": 10,
      "confidence_score": 0.98,
      "reasoning": "Direct salvation inquiry from seeker",
      "daily_time_commitment": "15-20 minutes",
      "start_date": "2026-01-16",
      "end_date": "2026-01-26",
      "special_notes": "User appears to be a seeker, not yet a believer"
    },
    "alternative_pathways": [],
    "follow_up_pathway": {
      "id": 2,
      "name": "New Believer Foundations",
      "description": "After accepting Christ, this pathway helps establish foundations",
      "note": "Recommended after completing Discovering Jesus"
    }
  },
  "next_steps": [
    "Start Discovering Jesus pathway",
    "Connect with a pastor for questions",
    "Explore baptism after salvation decision"
  ],
  "counselor_notification": {
    "alert_type": "seeker_inquiry",
    "priority": "high",
    "message": "User showing interest in salvation, may need human follow-up"
  },
  "status": "awaiting_user_response",
  "expires_at": "2026-01-23T14:20:00Z"
}
```

---

### Example 3: Marriage Problem

**User Input:**

```json
{
  "user_id": "user_34567",
  "question": "My marriage is falling apart. We fight constantly and I don't know what to do",
  "timestamp": "2026-01-16T19:45:00Z"
}
```

**System Output:**

```json
{
  "analysis": {
    "keywords": [
      "marriage",
      "falling apart",
      "fight",
      "constantly",
      "don't know what to do"
    ],
    "topics": ["marriage", "conflict", "relationships", "crisis"],
    "intent": "seeking_marriage_help",
    "sentiment": {
      "score": 25,
      "label": "distressed_and_desperate"
    }
  },
  "recommendation": {
    "primary_pathway": {
      "id": 7,
      "name": "Marriage & Relationships",
      "pathway_type": "MARRIAGE",
      "description": "Biblical principles for healthy marriage and conflict resolution",
      "duration_days": 21,
      "confidence_score": 0.95,
      "reasoning": "Clear marriage crisis with ongoing conflict",
      "daily_time_commitment": "20-30 minutes",
      "start_date": "2026-01-16",
      "end_date": "2026-02-06",
      "requires_partner": "Recommended for both spouses to participate",
      "special_notes": "High distress level detected, counselor follow-up recommended"
    },
    "alternative_pathways": [
      {
        "id": 4,
        "name": "Growing in Prayer",
        "pathway_type": "GROWING_IN_PRAYER",
        "description": "Prayer support during marriage difficulties",
        "duration_days": 7,
        "confidence_score": 0.68,
        "reasoning": "Prayer can provide support during crisis"
      }
    ]
  },
  "escalation": {
    "recommended": true,
    "reason": "Marriage crisis with high distress",
    "counselor_type": "biblical_counselor",
    "urgency": "high",
    "message": "User needs human counselor for marriage crisis"
  },
  "next_steps": [
    "Start Marriage & Relationships pathway",
    "Schedule appointment with Biblical Counselor",
    "Consider involving both spouses",
    "Access crisis support if needed"
  ],
  "additional_resources": [
    {
      "type": "counselor_session",
      "title": "Marriage Counseling",
      "description": "One-on-one session with trained Biblical Counselor"
    },
    {
      "type": "support_group",
      "title": "Marriage Support Group",
      "description": "Weekly group for couples facing challenges"
    }
  ],
  "status": "awaiting_user_response",
  "expires_at": "2026-01-23T19:45:00Z"
}
```

---

### Example 4: Multiple Topics (Grief + Financial)

**User Input:**

```json
{
  "user_id": "user_78901",
  "question": "My husband died last month and now I'm worried about money. I don't know how I'll pay the bills",
  "timestamp": "2026-01-16T11:15:00Z"
}
```

**System Output:**

```json
{
  "analysis": {
    "keywords": [
      "husband died",
      "last month",
      "worried about money",
      "pay bills"
    ],
    "topics": ["grief", "loss", "financial_stress", "widow"],
    "intent": "multiple_needs_grief_and_financial",
    "sentiment": {
      "score": 20,
      "label": "grieving_and_overwhelmed"
    }
  },
  "recommendation": {
    "primary_pathway": {
      "id": 10,
      "name": "Healing from Grief",
      "pathway_type": "HEALING_GRIEF",
      "description": "Processing loss and finding hope through grief journey",
      "duration_days": 30,
      "confidence_score": 0.88,
      "reasoning": "Recent death prioritized over financial concerns for emotional healing",
      "daily_time_commitment": "15-20 minutes",
      "start_date": "2026-01-16",
      "end_date": "2026-02-15",
      "special_notes": "User experiencing acute grief, recent loss (1 month)"
    },
    "secondary_pathway": {
      "id": 11,
      "name": "Financial Stewardship",
      "pathway_type": "FINANCIAL_STEWARDSHIP",
      "description": "Biblical guidance for financial challenges",
      "duration_days": 21,
      "confidence_score": 0.82,
      "reasoning": "Addressing financial stress after grief stabilizes",
      "recommended_start": "2026-02-16",
      "note": "Start after completing grief pathway or in parallel if user prefers"
    },
    "alternative_pathways": []
  },
  "multi_pathway_plan": {
    "sequence": "sequential_with_option_for_parallel",
    "phase_1": {
      "pathway_id": 10,
      "name": "Healing from Grief",
      "priority": "immediate",
      "reason": "Emotional healing is foundation for handling other challenges"
    },
    "phase_2": {
      "pathway_id": 11,
      "name": "Financial Stewardship",
      "priority": "follow_up",
      "reason": "Address financial concerns with more emotional stability"
    }
  },
  "escalation": {
    "recommended": true,
    "reason": "Multiple crisis factors: recent death, financial distress, very low sentiment",
    "counselor_type": "biblical_counselor",
    "urgency": "high",
    "additional_support": [
      "grief_counseling",
      "financial_assistance_program",
      "widow_support_group"
    ]
  },
  "next_steps": [
    "Begin Healing from Grief pathway immediately",
    "Connect with grief support group",
    "Schedule session with Biblical Counselor",
    "Access church financial assistance resources",
    "Plan to start Financial Stewardship pathway after 2-4 weeks"
  ],
  "additional_resources": [
    {
      "type": "support_group",
      "title": "Grief Support Group",
      "description": "Weekly meetings for those experiencing loss"
    },
    {
      "type": "financial_assistance",
      "title": "Benevolence Fund",
      "description": "Church financial aid for members in crisis"
    },
    {
      "type": "counselor_session",
      "title": "Grief Counseling",
      "description": "Specialized support for loss and bereavement"
    }
  ],
  "status": "awaiting_user_response",
  "expires_at": "2026-01-23T11:15:00Z"
}
```

---

### Example 5: Crisis Detection

**User Input:**

```json
{
  "user_id": "user_45678",
  "question": "I can't take this anymore. I just want it all to end",
  "timestamp": "2026-01-16T22:30:00Z"
}
```

**System Output:**

```json
{
  "analysis": {
    "keywords": ["can't take", "want it all to end"],
    "topics": ["crisis", "suicidal_ideation", "despair"],
    "intent": "expressing_suicidal_thoughts",
    "sentiment": {
      "score": 5,
      "label": "severe_crisis"
    },
    "crisis_detected": true,
    "crisis_indicators": [
      "suicidal_language",
      "extreme_hopelessness",
      "sentiment_critical_low"
    ]
  },
  "recommendation": {
    "primary_pathway": {
      "id": 12,
      "name": "Crisis Support",
      "pathway_type": "CRISIS_SUPPORT",
      "description": "Immediate crisis intervention and safety planning",
      "duration_days": 0,
      "confidence_score": 1.0,
      "reasoning": "CRISIS DETECTED - Immediate intervention required",
      "start_date": "2026-01-16",
      "immediate_action": true
    },
    "alternative_pathways": []
  },
  "crisis_protocol": {
    "activated": true,
    "severity": "extreme",
    "immediate_actions": [
      {
        "action": "display_988_lifeline",
        "status": "completed",
        "timestamp": "2026-01-16T22:30:01Z"
      },
      {
        "action": "escalate_to_crisis_counselor",
        "status": "in_progress",
        "timestamp": "2026-01-16T22:30:02Z"
      },
      {
        "action": "notify_on_call_pastor",
        "status": "completed",
        "method": "SMS",
        "recipient": "Pastor John Smith",
        "timestamp": "2026-01-16T22:30:03Z"
      },
      {
        "action": "log_conversation",
        "status": "completed",
        "purpose": "legal_documentation",
        "timestamp": "2026-01-16T22:30:03Z"
      }
    ]
  },
  "emergency_resources": {
    "primary": {
      "name": "988 Suicide & Crisis Lifeline",
      "phone": "988",
      "available": "24/7",
      "description": "Free, confidential support"
    },
    "secondary": {
      "name": "Crisis Text Line",
      "contact": "Text HOME to 741741",
      "available": "24/7"
    },
    "local": {
      "name": "Local Emergency Services",
      "phone": "911",
      "when_to_call": "Immediate danger to self or others"
    }
  },
  "next_steps": [
    "AI continues engagement (NEVER disconnect)",
    "Crisis counselor takes over conversation",
    "Safety assessment conducted",
    "Emergency services contacted if needed",
    "Follow-up care plan created"
  ],
  "escalation": {
    "recommended": true,
    "reason": "CRISIS - Suicidal ideation detected",
    "counselor_type": "crisis_counselor",
    "urgency": "immediate",
    "auto_escalated": true,
    "human_takeover_required": true,
    "estimated_response_time": "within_minutes"
  },
  "status": "crisis_protocol_active",
  "ai_mode": "crisis_support_continue_engagement",
  "human_counselor_assigned": true,
  "expires_at": null
}
```

---

## JSON Response Schema

### Standard Response Structure

```json
{
  "analysis": {
    "keywords": ["array", "of", "strings"],
    "topics": ["array", "of", "topics"],
    "intent": "string",
    "sentiment": {
      "score": 0-100,
      "label": "string"
    },
    "crisis_detected": boolean
  },
  "recommendation": {
    "primary_pathway": {
      "id": integer,
      "name": "string",
      "pathway_type": "ENUM",
      "description": "string",
      "duration_days": integer,
      "confidence_score": 0.0-1.0,
      "reasoning": "string",
      "daily_time_commitment": "string",
      "start_date": "ISO-8601",
      "end_date": "ISO-8601"
    },
    "alternative_pathways": [
      {
        "id": integer,
        "name": "string",
        "confidence_score": 0.0-1.0
      }
    ]
  },
  "escalation": {
    "recommended": boolean,
    "reason": "string",
    "counselor_type": "string",
    "urgency": "low|medium|high|immediate"
  },
  "next_steps": ["array", "of", "strings"],
  "status": "string",
  "expires_at": "ISO-8601 or null"
}
```

---

## Success Metrics

### System Performance

- **Response Time:** < 2 seconds
- **Accuracy:** > 85% correct pathway match
- **User Acceptance:** > 70% start recommended pathway
- **Completion Rate:** > 60% finish pathway

### User Satisfaction

- Clear recommendations
- Relevant content
- Easy enrollment
- Helpful alternatives

---

## Edge Cases

### Unclear Question

**User:** "I need help"
**Action:** Ask clarifying questions
**Response:** "I'd love to help! Can you tell me more about what you're going through? For example, are you struggling with anxiety, relationships, faith questions, or something else?"

### Multiple Needs

**User:** "I'm depressed about my marriage and financial stress"
**Action:** Acknowledge all needs, prioritize
**Response:** "I hear you're dealing with several challenges. Let's start with [primary pathway] which addresses [main issue]. We can also explore [secondary pathway] afterward."

### No Clear Match

**User:** "Tell me about your church"
**Action:** Provide information, don't force pathway
**Response:** [Provide church info] "Is there a specific area of spiritual growth you're interested in?"

---

## Summary

**Simple 3-Step Process:**

1. User asks question
2. AI analyzes and recommends pathway
3. User enrolls and begins journey

**Key Benefits:**

- Personalized spiritual guidance
- Structured discipleship
- Clear next steps
- Progress tracking
- Daily encouragement

**Result:** Users get the right content at the right time for their spiritual journey.
