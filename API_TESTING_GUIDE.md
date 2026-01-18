# LogosReach API Testing Guide

## Overview

LogosReach is an AI-powered spiritual pathway recommendation system. It analyzes user questionnaire responses and recommends personalized spiritual growth pathways using Mistral 7B AI.

## Base URL
```
http://localhost:8000
```

## Authentication

All protected endpoints require an API key in the header:
```
X-API-Key: your_api_key_here
```

---

## API Endpoints

### 1. Health Check (Public)

**Purpose:** Check if the API server is running and properly configured.

**When to use:**
- Before making other API calls
- For monitoring/health checks
- To verify configuration status

```
GET /health
```

**Headers:** None required (public endpoint)

**Response:**
```json
{
    "status": "healthy",
    "api_key_configured": true,
    "openrouter_configured": true,
    "database_configured": true,
    "cache_size": 0
}
```

**Test with cURL:**
```bash
curl http://localhost:8000/health
```

---

### 2. Root Info (Public)

**Purpose:** Get API information and list of all available endpoints.

**When to use:**
- To discover available endpoints
- To check API version

```
GET /
```

**Headers:** None required (public endpoint)

**Response:**
```json
{
    "name": "LogosReach Pathway Recommendation API",
    "version": "1.0.0",
    "status": "running",
    "authentication": "Required. Pass X-API-Key header for protected endpoints.",
    "features": [
        "Async database operations",
        "Connection pooling",
        "Response caching",
        "Multi-worker support",
        "API key authentication"
    ],
    "endpoints": {
        "public": {
            "root": "GET /",
            "health": "GET /health"
        },
        "protected": {
            "questions": "GET /questions/{entry_type}",
            "pathways": "GET /pathways",
            "recommend": "POST /recommend",
            "user_history": "GET /users/{user_id}/history"
        }
    }
}
```

**Test with cURL:**
```bash
curl http://localhost:8000/
```

---

### 3. Get Questions (Protected)

**Purpose:** Retrieve questionnaire questions based on user's Christianity knowledge level.

**When to use:**
- When starting the onboarding flow
- To display questions to the user in your frontend

**Entry Types:**
- `no_im_new` - For users new to Christianity (10 questions)
- `yes_i_know` - For users who know Christianity (10 questions)

```
GET /questions/{entry_type}
```

**Headers:**
```
X-API-Key: your_api_key_here
```

**Path Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| entry_type | string | Either `no_im_new` or `yes_i_know` |

**Response (for `no_im_new`):**
```json
{
    "entry_type": "no_im_new",
    "initial_question": {
        "id": "christianity_knowledge",
        "question": "Do you have knowledge of Christianity?",
        "description": "This helps us personalize your learning journey and questions",
        "options": [
            {
                "value": "yes_i_know",
                "label": "Yes, I Know",
                "description": "I have knowledge of Christianity and the Bible"
            },
            {
                "value": "no_im_new",
                "label": "No, I'm New",
                "description": "I'm new to Christianity and want to learn"
            }
        ]
    },
    "questions": {
        "total_questions": 10,
        "questions": [
            {
                "question_number": 1,
                "progress": "10%",
                "question": "How would you describe your current interest in spirituality or personal growth?",
                "options": [
                    "Very interested",
                    "Somewhat interested",
                    "Curious but unsure",
                    "Not very interested"
                ]
            }
            // ... more questions
        ]
    }
}
```

**Test with cURL:**
```bash
# Get questions for new users
curl -H "X-API-Key: your_api_key_here" http://localhost:8000/questions/no_im_new

# Get questions for existing believers
curl -H "X-API-Key: your_api_key_here" http://localhost:8000/questions/yes_i_know
```

---

### 4. Get Pathways (Protected)

**Purpose:** Retrieve list of all available spiritual growth pathways.

**When to use:**
- To display pathway options to users
- For reference/admin purposes

```
GET /pathways
```

**Headers:**
```
X-API-Key: your_api_key_here
```

**Response:**
```json
{
    "pathways": [
        {
            "id": 1,
            "name": "Discovering Jesus",
            "duration": "7-10 days",
            "theme": "seeker, new to Christianity, not familiar with Jesus, curiosity about faith"
        },
        {
            "id": 2,
            "name": "New Believer Foundations",
            "duration": "14 days",
            "theme": "recently believed, needs basics of faith"
        },
        {
            "id": 3,
            "name": "Water Baptism",
            "duration": "7 days",
            "theme": "baptism, public declaration of faith"
        },
        {
            "id": 4,
            "name": "Growing in Prayer",
            "duration": "7 days",
            "theme": "learning to pray, anxiety, peace, trusting God"
        },
        {
            "id": 5,
            "name": "Understanding the Bible",
            "duration": "10-14 days",
            "theme": "confused about scripture, wants deeper context"
        },
        {
            "id": 6,
            "name": "Finding Purpose & Calling",
            "duration": "14-21 days",
            "theme": "purpose, calling, career direction, meaning in life"
        },
        {
            "id": 7,
            "name": "Marriage & Relationships",
            "duration": "14-21 days",
            "theme": "marriage issues, relationship struggles, family"
        },
        {
            "id": 8,
            "name": "Parenting with Faith",
            "duration": "14 days",
            "theme": "parenting, raising children, family faith"
        },
        {
            "id": 9,
            "name": "Overcoming Anxiety",
            "duration": "10-14 days",
            "theme": "worry, fear, need peace, anxiety, stress"
        },
        {
            "id": 10,
            "name": "Healing from Grief",
            "duration": "21-30 days",
            "theme": "loss, grief, mourning, bereavement"
        },
        {
            "id": 11,
            "name": "Financial Stewardship",
            "duration": "14-21 days",
            "theme": "finances, money management, stewardship, debt"
        },
        {
            "id": 12,
            "name": "Crisis Support",
            "duration": "Variable",
            "theme": "urgent help, hopelessness, fear, crisis, emergency"
        }
    ]
}
```

**Test with cURL:**
```bash
curl -H "X-API-Key: your_api_key_here" http://localhost:8000/pathways
```

---

### 5. Get Recommendation (Protected) ⭐ MAIN API

**Purpose:** Submit user's questionnaire answers and get AI-powered pathway recommendation.

**When to use:**
- After user completes the questionnaire
- This is the MAIN API that processes answers and returns recommendations

**What happens internally:**
1. Creates/finds user in database
2. Stores questionnaire answers
3. Sends answers to Mistral 7B AI for analysis
4. AI analyzes spiritual stage, emotional state, and needs
5. Stores AI recommendation in database
6. Returns recommendation with tracking IDs

```
POST /recommend
```

**Headers:**
```
Content-Type: application/json
X-API-Key: your_api_key_here
```

**Request Body:**
```json
{
    "user_id": "external-user-123",
    "entry_type": "no_im_new",
    "answers": {
        "Q1": "Very interested",
        "Q2": "Personal experiences",
        "Q3": "No, not really",
        "Q4": "Not familiar at all",
        "Q5": "Seeking meaning or purpose",
        "Q6": "Very comfortable",
        "Q7": "Short simple lessons",
        "Q8": "Maybe / unsure",
        "Q9": "How to find peace",
        "Q10": "Very open"
    }
}
```

**Request Fields:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| user_id | string | No | Your backend's user ID (optional, creates new if not provided) |
| entry_type | string | Yes | Either `no_im_new` or `yes_i_know` |
| answers | object | Yes | Dictionary of question numbers to selected answers |

**Response:**
```json
{
    "success": true,
    "data": {
        "recommended_pathway": "Discovering Jesus (7-10 days)",
        "confidence": 0.92,
        "detected_profile": {
            "spiritual_stage": "seeker",
            "primary_need": "salvation",
            "emotional_state": "curious"
        },
        "reasoning": "Based on the user's responses indicating no prior familiarity with Jesus, high openness to learning, and seeking meaning and peace, the Discovering Jesus pathway is the most appropriate starting point for their spiritual journey.",
        "next_step_message": "Welcome to your spiritual journey! The Discovering Jesus pathway will introduce you to the foundational teachings of Christianity in a gentle, easy-to-understand way. Each day brings a short lesson designed to help you explore faith at your own pace."
    },
    "user_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
    "recommendation_id": "f9e8d7c6-b5a4-3210-fedc-ba0987654321"
}
```

**Test with cURL:**

**Example 1: New to Christianity (Seeker)**
```bash
curl -X POST http://localhost:8000/recommend \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your_api_key_here" \
  -d '{
    "user_id": "user-001",
    "entry_type": "no_im_new",
    "answers": {
        "Q1": "Very interested",
        "Q2": "Personal experiences",
        "Q3": "No, not really",
        "Q4": "Not familiar at all",
        "Q5": "Seeking meaning or purpose",
        "Q6": "Very comfortable",
        "Q7": "Short simple lessons",
        "Q8": "Maybe / unsure",
        "Q9": "How to find peace",
        "Q10": "Very open"
    }
}'
```

**Example 2: Existing Believer with Anxiety**
```bash
curl -X POST http://localhost:8000/recommend \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your_api_key_here" \
  -d '{
    "user_id": "user-002",
    "entry_type": "yes_i_know",
    "answers": {
        "Q1": "Several times a week",
        "Q2": "Sometimes confused",
        "Q3": "I pray a few times a week",
        "Q4": "Growing but inconsistent",
        "Q5": "Prayer life,Faith and trust in God",
        "Q6": "Somewhat familiar",
        "Q7": "Simple daily devotionals",
        "Q8": "Yes, occasionally involved",
        "Q9": "Mental and emotional health",
        "Q10": "Grow closer to God through prayer"
    }
}'
```

**Example 3: Believer Seeking Purpose**
```bash
curl -X POST http://localhost:8000/recommend \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your_api_key_here" \
  -d '{
    "user_id": "user-003",
    "entry_type": "yes_i_know",
    "answers": {
        "Q1": "Daily",
        "Q2": "Very confident",
        "Q3": "I pray daily",
        "Q4": "Deep and intimate",
        "Q5": "Purpose and calling",
        "Q6": "Very familiar",
        "Q7": "Deep Bible study with context",
        "Q8": "Yes, actively involved",
        "Q9": "Career and purpose",
        "Q10": "Apply biblical teachings to daily life"
    }
}'
```

---

### 6. Get User History (Protected)

**Purpose:** Retrieve a user's past pathway recommendations.

**When to use:**
- To show user their recommendation history
- For analytics/tracking purposes
- To see if user has previous recommendations

```
GET /users/{user_id}/history
```

**Headers:**
```
X-API-Key: your_api_key_here
```

**Path Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| user_id | string | The external user ID (your backend's user ID) |

**Response:**
```json
{
    "success": true,
    "user_id": "user-001",
    "recommendations": [
        {
            "id": "f9e8d7c6-b5a4-3210-fedc-ba0987654321",
            "recommended_pathway": "Discovering Jesus (7-10 days)",
            "confidence": 0.92,
            "spiritual_stage": "seeker",
            "primary_need": "salvation",
            "emotional_state": "curious",
            "reasoning": "Based on the user's responses...",
            "created_at": "2024-01-15T10:30:00"
        }
    ]
}
```

**Test with cURL:**
```bash
curl -H "X-API-Key: your_api_key_here" http://localhost:8000/users/user-001/history
```

---

## Complete Testing Flow

### Step 1: Start the Server
```bash
cd d:\vycentric\LogosReach
venv\Scripts\activate
python main.py
```

### Step 2: Check Health
```bash
curl http://localhost:8000/health
```
Expected: `{"status": "healthy", ...}`

### Step 3: Get Questions
```bash
curl -H "X-API-Key: your_api_key_here" http://localhost:8000/questions/no_im_new
```

### Step 4: Submit Answers & Get Recommendation
```bash
curl -X POST http://localhost:8000/recommend \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your_api_key_here" \
  -d '{
    "user_id": "test-user-001",
    "entry_type": "no_im_new",
    "answers": {
        "Q1": "Very interested",
        "Q2": "Personal experiences",
        "Q3": "No, not really",
        "Q4": "Not familiar at all",
        "Q5": "Seeking meaning or purpose",
        "Q6": "Very comfortable",
        "Q7": "Short simple lessons",
        "Q8": "Maybe / unsure",
        "Q9": "How to find peace",
        "Q10": "Very open"
    }
}'
```
**Save the `user_id` and `recommendation_id` from response for future reference!**

### Step 5: Check User History
```bash
curl -H "X-API-Key: your_api_key_here" http://localhost:8000/users/test-user-001/history
```

---

## Error Responses

### 401 Unauthorized - Missing API Key
```json
{
    "detail": "Missing API key. Please provide X-API-Key header."
}
```

### 403 Forbidden - Invalid API Key
```json
{
    "detail": "Invalid API key"
}
```

### 400 Bad Request - Invalid Input
```json
{
    "detail": "entry_type must be 'yes_i_know' or 'no_im_new'"
}
```

### 404 Not Found - Resource Not Found
```json
{
    "detail": "Recommendation not found for this user"
}
```

### 500 Internal Server Error
```json
{
    "success": false,
    "error": "Failed to generate recommendation: OPENROUTER_API_KEY is not set"
}
```

---

## Testing with Postman

### Import Collection
1. Open Postman
2. Create new Collection: "LogosReach API"
3. Add environment variable: `API_KEY` = your key
4. Add environment variable: `BASE_URL` = http://localhost:8000

### Request Examples

**Health Check:**
- Method: GET
- URL: {{BASE_URL}}/health

**Get Questions:**
- Method: GET
- URL: {{BASE_URL}}/questions/no_im_new
- Headers: X-API-Key: {{API_KEY}}

**Recommend Pathway:**
- Method: POST
- URL: {{BASE_URL}}/recommend
- Headers:
  - Content-Type: application/json
  - X-API-Key: {{API_KEY}}
- Body: (raw JSON)

---

## Database Tables

| Table | Purpose |
|-------|---------|
| users | Stores user info with external_user_id mapping |
| questionnaire_responses | Stores all Q&A answers as JSON |
| pathway_recommendations | Stores AI recommendations + detected profile |

---

## Response Time Expectations

| Scenario | Expected Time |
|----------|---------------|
| Health check | < 50ms |
| Get questions | < 100ms |
| Get pathways | < 50ms |
| Recommend (cache hit) | < 200ms |
| Recommend (cache miss - AI call) | 2-5 seconds |
| User history | < 200ms |
