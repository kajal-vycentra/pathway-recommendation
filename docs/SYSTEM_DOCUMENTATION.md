# LogosReach Pathway Recommendation System

## Complete Technical Documentation

---

## Table of Contents

1. [System Overview](#1-system-overview)
2. [Architecture](#2-architecture)
3. [Data Flow](#3-data-flow)
4. [Database Schema](#4-database-schema)
5. [AI Processing Logic](#5-ai-processing-logic)
6. [API Endpoints Detailed](#6-api-endpoints-detailed)
7. [Authentication System](#7-authentication-system)
8. [Caching Strategy](#8-caching-strategy)
9. [Scalability Features](#9-scalability-features)
10. [File Structure](#10-file-structure)
11. [Configuration](#11-configuration)
12. [Error Handling](#12-error-handling)

---

## 1. System Overview

### What is LogosReach?

LogosReach is an AI-powered spiritual pathway recommendation system designed to guide users on their spiritual journey. The system analyzes user responses to a questionnaire and uses artificial intelligence (Mistral 7B via OpenRouter) to recommend personalized spiritual growth pathways.

### Core Purpose

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER JOURNEY                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   User Answers Questions  →  AI Analyzes Responses  →  Gets    │
│   About Their Spiritual      Spiritual Stage,          Personalized
│   Background & Needs         Emotional State,          Pathway   │
│                              Primary Need              Recommendation
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Key Features

| Feature | Description |
|---------|-------------|
| AI-Powered Analysis | Uses Mistral 7B to understand user's spiritual state |
| Personalized Recommendations | Matches users to 1 of 12 spiritual pathways |
| Dual Question Flows | Different questions for new vs. existing believers |
| Progress Tracking | Stores all responses and recommendations |
| Scalable Architecture | Async operations, caching, connection pooling |
| Secure API | API key authentication for all protected endpoints |

---

## 2. Architecture

### High-Level Architecture

```
┌──────────────────────────────────────────────────────────────────────────┐
│                           CLIENT (Your Backend)                          │
│                                                                          │
│   ┌─────────────┐    ┌─────────────┐    ┌─────────────┐                 │
│   │   Mobile    │    │     Web     │    │   Other     │                 │
│   │    App      │    │    App      │    │  Services   │                 │
│   └──────┬──────┘    └──────┬──────┘    └──────┬──────┘                 │
│          │                  │                   │                        │
│          └──────────────────┼───────────────────┘                        │
│                             │                                            │
│                             ▼                                            │
│                    ┌────────────────┐                                    │
│                    │  Your Backend  │                                    │
│                    │    Server      │                                    │
│                    └────────┬───────┘                                    │
└─────────────────────────────┼────────────────────────────────────────────┘
                              │
                              │ HTTP Request with X-API-Key
                              ▼
┌──────────────────────────────────────────────────────────────────────────┐
│                        LOGOSREACH API SERVER                             │
│                                                                          │
│   ┌─────────────────────────────────────────────────────────────────┐   │
│   │                      FastAPI Application                         │   │
│   │                                                                  │   │
│   │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │   │
│   │  │    Auth      │  │   Routing    │  │   CORS       │          │   │
│   │  │  Middleware  │  │   Layer      │  │  Middleware  │          │   │
│   │  └──────┬───────┘  └──────┬───────┘  └──────────────┘          │   │
│   │         │                 │                                      │   │
│   │         ▼                 ▼                                      │   │
│   │  ┌─────────────────────────────────────────────────────────┐   │   │
│   │  │              Recommendation Service                      │   │   │
│   │  │                                                          │   │   │
│   │  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐     │   │   │
│   │  │  │   Cache     │  │    AI       │  │  Database   │     │   │   │
│   │  │  │   Layer     │  │  Client     │  │  Operations │     │   │   │
│   │  │  └─────────────┘  └──────┬──────┘  └──────┬──────┘     │   │   │
│   │  └───────────────────────────┼───────────────┼──────────────┘   │   │
│   └──────────────────────────────┼───────────────┼──────────────────┘   │
│                                  │               │                       │
└──────────────────────────────────┼───────────────┼───────────────────────┘
                                   │               │
                    ┌──────────────┘               └──────────────┐
                    │                                             │
                    ▼                                             ▼
        ┌───────────────────┐                         ┌───────────────────┐
        │   OpenRouter AI   │                         │    PostgreSQL     │
        │   (Mistral 7B)    │                         │     Database      │
        │                   │                         │                   │
        │  Analyzes user    │                         │  Stores:          │
        │  responses and    │                         │  - Users          │
        │  returns pathway  │                         │  - Responses      │
        │  recommendation   │                         │  - Recommendations│
        └───────────────────┘                         └───────────────────┘
```

### Technology Stack

| Layer | Technology | Purpose |
|-------|------------|---------|
| Web Framework | FastAPI | Async API endpoints |
| Database | PostgreSQL | Data persistence |
| ORM | SQLAlchemy (Async) | Database operations |
| AI Provider | OpenRouter | AI model access |
| AI Model | Mistral 7B Instruct | Text analysis |
| HTTP Client | httpx | Async HTTP requests |
| Caching | cachetools (TTLCache) | Response caching |
| Authentication | API Key Header | Security |

---

## 3. Data Flow

### Complete Request-Response Flow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    COMPLETE DATA FLOW: /recommend ENDPOINT                   │
└─────────────────────────────────────────────────────────────────────────────┘

STEP 1: REQUEST RECEIVED
═══════════════════════════════════════════════════════════════════════════════

    Your Backend                          LogosReach API
         │                                      │
         │  POST /recommend                     │
         │  Headers: X-API-Key: xxx             │
         │  Body: {                             │
         │    "user_id": "user-123",            │
         │    "entry_type": "no_im_new",        │
         │    "answers": {...}                  │
         │  }                                   │
         │─────────────────────────────────────►│
         │                                      │


STEP 2: AUTHENTICATION CHECK
═══════════════════════════════════════════════════════════════════════════════

                    ┌─────────────────────────────────┐
                    │        auth.py                  │
                    │   verify_api_key()              │
                    ├─────────────────────────────────┤
                    │                                 │
                    │  1. Check if API key exists     │
                    │     in X-API-Key header         │
                    │                                 │
                    │  2. Compare with stored         │
                    │     API_KEY in settings         │
                    │                                 │
                    │  3. If valid → Continue         │
                    │     If invalid → 401/403 Error  │
                    │                                 │
                    └─────────────────────────────────┘


STEP 3: USER MANAGEMENT
═══════════════════════════════════════════════════════════════════════════════

                    ┌─────────────────────────────────┐
                    │  _get_or_create_user()          │
                    ├─────────────────────────────────┤
                    │                                 │
                    │  Input: external_user_id        │
                    │         (e.g., "user-123")      │
                    │                                 │
                    │         ┌───────────────┐       │
                    │         │ Query DB for  │       │
                    │         │ existing user │       │
                    │         └───────┬───────┘       │
                    │                 │               │
                    │         ┌───────▼───────┐       │
                    │         │  User Found?  │       │
                    │         └───────┬───────┘       │
                    │                 │               │
                    │     ┌───────────┼───────────┐   │
                    │     │ YES       │       NO  │   │
                    │     ▼           │           ▼   │
                    │  ┌──────┐       │      ┌──────┐ │
                    │  │Return│       │      │Create│ │
                    │  │User  │       │      │ New  │ │
                    │  └──────┘       │      │User  │ │
                    │                 │      └──────┘ │
                    │                                 │
                    │  Output: User object with UUID  │
                    │                                 │
                    └─────────────────────────────────┘

                              │
                              ▼
                    ┌─────────────────────────────────┐
                    │      PostgreSQL: users          │
                    ├─────────────────────────────────┤
                    │  id: UUID (auto-generated)      │
                    │  external_user_id: "user-123"   │
                    │  created_at: timestamp          │
                    │  updated_at: timestamp          │
                    └─────────────────────────────────┘


STEP 4: STORE QUESTIONNAIRE RESPONSES
═══════════════════════════════════════════════════════════════════════════════

                    ┌─────────────────────────────────┐
                    │  _store_questionnaire_response()│
                    ├─────────────────────────────────┤
                    │                                 │
                    │  Input:                         │
                    │    - user (User object)         │
                    │    - entry_type: "no_im_new"    │
                    │    - answers: {                 │
                    │        "Q1": "Very interested", │
                    │        "Q2": "Personal exp...", │
                    │        ...                      │
                    │      }                          │
                    │                                 │
                    │  Action: INSERT into database   │
                    │                                 │
                    │  Output: QuestionnaireResponse  │
                    │          object with UUID       │
                    │                                 │
                    └─────────────────────────────────┘

                              │
                              ▼
                    ┌─────────────────────────────────┐
                    │ PostgreSQL: questionnaire_      │
                    │             responses           │
                    ├─────────────────────────────────┤
                    │  id: UUID                       │
                    │  user_id: UUID (FK → users)     │
                    │  entry_type: "no_im_new"        │
                    │  answers: JSON {                │
                    │    "Q1": "Very interested",     │
                    │    "Q2": "Personal experiences",│
                    │    ...                          │
                    │  }                              │
                    │  created_at: timestamp          │
                    └─────────────────────────────────┘


STEP 5: CHECK CACHE
═══════════════════════════════════════════════════════════════════════════════

                    ┌─────────────────────────────────┐
                    │      Cache Lookup               │
                    ├─────────────────────────────────┤
                    │                                 │
                    │  1. Generate cache key:         │
                    │     MD5 hash of:                │
                    │     - entry_type                │
                    │     - sorted answers dict       │
                    │                                 │
                    │  2. Check TTLCache:             │
                    │     - Max 1000 entries          │
                    │     - TTL: 1 hour               │
                    │                                 │
                    │         ┌───────────────┐       │
                    │         │ Cache Hit?    │       │
                    │         └───────┬───────┘       │
                    │                 │               │
                    │     ┌───────────┼───────────┐   │
                    │     │ YES       │       NO  │   │
                    │     ▼           │           ▼   │
                    │  ┌──────────┐   │   ┌──────────┐│
                    │  │ Return   │   │   │ Call AI  ││
                    │  │ Cached   │   │   │ API      ││
                    │  │ Response │   │   │ (Step 6) ││
                    │  │ (~50ms)  │   │   │ (2-5sec) ││
                    │  └──────────┘   │   └──────────┘│
                    │                                 │
                    └─────────────────────────────────┘


STEP 6: AI PROCESSING (If Cache Miss)
═══════════════════════════════════════════════════════════════════════════════

                    ┌─────────────────────────────────┐
                    │      _call_ai_api()             │
                    ├─────────────────────────────────┤
                    │                                 │
                    │  1. Format User Prompt:         │
                    │     ┌─────────────────────────┐ │
                    │     │ User Entry Type:        │ │
                    │     │ No, I'm New             │ │
                    │     │                         │ │
                    │     │ Answers:                │ │
                    │     │ Q1: Very interested     │ │
                    │     │ Q2: Personal experiences│ │
                    │     │ Q3: No, not really      │ │
                    │     │ ...                     │ │
                    │     └─────────────────────────┘ │
                    │                                 │
                    │  2. Create API Request:         │
                    │     - Model: mistral-7b-instruct│
                    │     - System Prompt: (see below)│
                    │     - User Prompt: (formatted)  │
                    │     - Temperature: 0.3          │
                    │     - Max Tokens: 500           │
                    │                                 │
                    └─────────────────────────────────┘

                              │
                              ▼
                    ┌─────────────────────────────────────────────────────┐
                    │                  OPENROUTER AI                       │
                    │                  (Mistral 7B)                        │
                    ├─────────────────────────────────────────────────────┤
                    │                                                      │
                    │  SYSTEM PROMPT (What AI knows):                      │
                    │  ════════════════════════════════                    │
                    │  "You are LogosReach Pathway Recommendation AI.      │
                    │                                                      │
                    │   Your role: Analyze questionnaire answers and       │
                    │   recommend ONE pathway from:                        │
                    │                                                      │
                    │   1. Discovering Jesus (7-10 days)                   │
                    │   2. New Believer Foundations (14 days)              │
                    │   3. Water Baptism (7 days)                          │
                    │   4. Growing in Prayer (7 days)                      │
                    │   5. Understanding the Bible (10-14 days)            │
                    │   6. Finding Purpose & Calling (14-21 days)          │
                    │   7. Marriage & Relationships (14-21 days)           │
                    │   8. Parenting with Faith (14 days)                  │
                    │   9. Overcoming Anxiety (10-14 days)                 │
                    │   10. Healing from Grief (21-30 days)                │
                    │   11. Financial Stewardship (14-21 days)             │
                    │   12. Crisis Support (Variable)                      │
                    │                                                      │
                    │   Analyze:                                           │
                    │   - Spiritual Stage (seeker/new/growing/struggling)  │
                    │   - Emotional State (anxious/curious/open/etc.)      │
                    │   - Primary Need (salvation/peace/purpose/etc.)      │
                    │                                                      │
                    │   Return JSON only."                                 │
                    │                                                      │
                    │  AI PROCESSING:                                      │
                    │  ════════════════                                    │
                    │  The AI analyzes patterns in answers:                │
                    │                                                      │
                    │  • "Not familiar at all" with Jesus                  │
                    │    → Spiritual Stage: SEEKER                         │
                    │                                                      │
                    │  • "Very open" to learning                           │
                    │    → Emotional State: CURIOUS/OPEN                   │
                    │                                                      │
                    │  • "Seeking meaning or purpose"                      │
                    │    → Primary Need: SALVATION (for seekers)           │
                    │                                                      │
                    │  • Pattern Match → "Discovering Jesus" pathway       │
                    │                                                      │
                    └─────────────────────────────────────────────────────┘

                              │
                              ▼
                    ┌─────────────────────────────────┐
                    │      AI Response (JSON)         │
                    ├─────────────────────────────────┤
                    │  {                              │
                    │    "recommended_pathway":       │
                    │      "Discovering Jesus         │
                    │       (7-10 days)",             │
                    │                                 │
                    │    "confidence": 0.92,          │
                    │                                 │
                    │    "detected_profile": {        │
                    │      "spiritual_stage":         │
                    │        "seeker",                │
                    │      "primary_need":            │
                    │        "salvation",             │
                    │      "emotional_state":         │
                    │        "curious"                │
                    │    },                           │
                    │                                 │
                    │    "reasoning":                 │
                    │      "Based on the user's       │
                    │       responses indicating no   │
                    │       prior familiarity with    │
                    │       Jesus, high openness to   │
                    │       learning, and seeking     │
                    │       meaning and peace...",    │
                    │                                 │
                    │    "next_step_message":         │
                    │      "Welcome to your spiritual │
                    │       journey! The Discovering  │
                    │       Jesus pathway will..."    │
                    │  }                              │
                    └─────────────────────────────────┘


STEP 7: STORE RECOMMENDATION
═══════════════════════════════════════════════════════════════════════════════

                    ┌─────────────────────────────────┐
                    │  _store_recommendation()        │
                    ├─────────────────────────────────┤
                    │                                 │
                    │  Store AI response in database  │
                    │  for tracking and analytics     │
                    │                                 │
                    └─────────────────────────────────┘

                              │
                              ▼
                    ┌─────────────────────────────────┐
                    │ PostgreSQL: pathway_            │
                    │             recommendations     │
                    ├─────────────────────────────────┤
                    │  id: UUID                       │
                    │  user_id: UUID (FK)             │
                    │  questionnaire_response_id: UUID│
                    │  recommended_pathway: string    │
                    │  confidence: 0.92               │
                    │  spiritual_stage: "seeker"      │
                    │  primary_need: "salvation"      │
                    │  emotional_state: "curious"     │
                    │  reasoning: text                │
                    │  next_step_message: text        │
                    │  raw_ai_response: JSON          │
                    │  created_at: timestamp          │
                    └─────────────────────────────────┘


STEP 8: RETURN RESPONSE
═══════════════════════════════════════════════════════════════════════════════

    LogosReach API                         Your Backend
         │                                      │
         │  HTTP 200 OK                         │
         │  {                                   │
         │    "success": true,                  │
         │    "data": {                         │
         │      "recommended_pathway":          │
         │        "Discovering Jesus...",       │
         │      "confidence": 0.92,             │
         │      "detected_profile": {...},      │
         │      "reasoning": "...",             │
         │      "next_step_message": "..."      │
         │    },                                │
         │    "user_id": "uuid-...",            │
         │    "recommendation_id": "uuid-..."   │
         │  }                                   │
         │◄─────────────────────────────────────│
         │                                      │
```

---

## 4. Database Schema

### Entity Relationship Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          DATABASE SCHEMA                                     │
└─────────────────────────────────────────────────────────────────────────────┘

    ┌─────────────────────┐
    │       USERS         │
    ├─────────────────────┤
    │ PK  id: UUID        │
    │     external_user_id│───────────────────────────────┐
    │     created_at      │                               │
    │     updated_at      │                               │
    └──────────┬──────────┘                               │
               │                                          │
               │ 1:N                                      │
               │                                          │
    ┌──────────▼──────────┐                               │
    │ QUESTIONNAIRE_      │                               │
    │ RESPONSES           │                               │
    ├─────────────────────┤                               │
    │ PK  id: UUID        │                               │
    │ FK  user_id: UUID   │◄──────────────────────────────┤
    │     entry_type      │                               │
    │     answers: JSON   │                               │
    │     created_at      │                               │
    └──────────┬──────────┘                               │
               │                                          │
               │ 1:1                                      │
               │                                          │
    ┌──────────▼──────────┐                               │
    │ PATHWAY_            │                               │
    │ RECOMMENDATIONS     │                               │
    ├─────────────────────┤                               │
    │ PK  id: UUID        │                               │
    │ FK  user_id: UUID   │◄──────────────────────────────┤
    │ FK  questionnaire_  │                               │
    │     response_id     │                               │
    │     recommended_    │                               │
    │       pathway       │                               │
    │     confidence      │                               │
    │     spiritual_stage │                               │
    │     primary_need    │                               │
    │     emotional_state │                               │
    │     reasoning       │                               │
    │     next_step_msg   │                               │
    │     raw_ai_response │                               │
    │     created_at      │                               │
    └──────────┬──────────┘                               │
               │                                          │
```

### Table Details

#### users
| Column | Type | Description |
|--------|------|-------------|
| id | UUID | Primary key, auto-generated |
| external_user_id | VARCHAR(255) | Your backend's user ID (unique) |
| created_at | TIMESTAMP | When user was created |
| updated_at | TIMESTAMP | Last update time |

#### questionnaire_responses
| Column | Type | Description |
|--------|------|-------------|
| id | UUID | Primary key |
| user_id | UUID | Foreign key to users |
| entry_type | VARCHAR(50) | "yes_i_know" or "no_im_new" |
| answers | JSON | All Q&A pairs stored as JSON |
| created_at | TIMESTAMP | When submitted |

#### pathway_recommendations
| Column | Type | Description |
|--------|------|-------------|
| id | UUID | Primary key |
| user_id | UUID | Foreign key to users |
| questionnaire_response_id | UUID | Foreign key to responses |
| recommended_pathway | VARCHAR(255) | e.g., "Discovering Jesus (7-10 days)" |
| confidence | FLOAT | AI confidence score (0.0 - 1.0) |
| spiritual_stage | VARCHAR(100) | seeker/new_believer/growing/struggling |
| primary_need | VARCHAR(100) | salvation/peace/purpose/healing/etc. |
| emotional_state | VARCHAR(100) | curious/anxious/open/hopeful/etc. |
| reasoning | TEXT | AI's explanation |
| next_step_message | TEXT | Encouraging message for user |
| raw_ai_response | JSON | Complete AI response for audit |
| created_at | TIMESTAMP | When generated |

---

## 5. AI Processing Logic

### The RELATE Framework

Before recommending any pathway, the AI processes through the **RELATE Framework** - a compassionate, human-centered approach that ensures users feel seen, heard, and understood.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        THE RELATE FRAMEWORK                                  │
│                  (Relationship-First Recommendation)                         │
└─────────────────────────────────────────────────────────────────────────────┘

    The AI acts as a compassionate spiritual companion, NOT a cold algorithm.
    Before any recommendation, the AI internally processes through ALL stages:

    ┌─────────────────────────────────────────────────────────────────────────┐
    │                                                                          │
    │   R ─ RECOGNIZE                                                          │
    │   ════════════════════════════════════════════════════════════════════   │
    │   • Who is this person based on their answers?                           │
    │   • What is their life situation right now?                              │
    │   • Are they new to faith or experienced?                                │
    │   • What context surrounds their spiritual journey?                      │
    │                                                                          │
    │   Example: "This person is a working mother struggling with anxiety,     │
    │            new to exploring faith after a difficult season."             │
    │                                                                          │
    └─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
    ┌─────────────────────────────────────────────────────────────────────────┐
    │                                                                          │
    │   E ─ EMPATHIZE                                                          │
    │   ════════════════════════════════════════════════════════════════════   │
    │   • What emotions are they experiencing?                                 │
    │     (anxiety, grief, confusion, hope, fear, curiosity, pain)             │
    │   • Put yourself in their shoes - feel what they're feeling              │
    │   • Understand the weight of what they're carrying                       │
    │   • No judgment, only compassion                                         │
    │                                                                          │
    │   Example: "I can sense the exhaustion and worry in their answers.       │
    │            They're carrying a heavy burden and seeking relief."          │
    │                                                                          │
    └─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
    ┌─────────────────────────────────────────────────────────────────────────┐
    │                                                                          │
    │   L ─ LISTEN                                                             │
    │   ════════════════════════════════════════════════════════════════════   │
    │   • What are they REALLY saying beneath the surface answers?             │
    │   • What's the deeper need they may not have explicitly stated?          │
    │   • Read between the lines with compassion                               │
    │   • Hear the unspoken cries in their responses                           │
    │                                                                          │
    │   Example: "They said they want 'peace' but what they really need        │
    │            is to know they're not alone and that God sees them."         │
    │                                                                          │
    └─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
    ┌─────────────────────────────────────────────────────────────────────────┐
    │                                                                          │
    │   A ─ AFFIRM                                                             │
    │   ════════════════════════════════════════════════════════════════════   │
    │   • What courage did it take for them to answer honestly?                │
    │   • What strengths do you see in them?                                   │
    │   • Seeking help IS strength - acknowledge this                          │
    │   • They are brave for taking this step                                  │
    │                                                                          │
    │   Example: "It takes real courage to admit you're struggling.            │
    │            Their willingness to seek help shows inner strength."         │
    │                                                                          │
    └─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
    ┌─────────────────────────────────────────────────────────────────────────┐
    │                                                                          │
    │   T ─ TRUST                                                              │
    │   ════════════════════════════════════════════════════════════════════   │
    │   • How can the response make them feel safe and understood?             │
    │   • They need to know someone cares before receiving guidance            │
    │   • Build connection through words                                       │
    │   • Create a sense of safety and being seen                              │
    │                                                                          │
    │   Example: "The response should feel like a warm embrace,                │
    │            letting them know they're not alone in this."                 │
    │                                                                          │
    └─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
    ┌─────────────────────────────────────────────────────────────────────────┐
    │                                                                          │
    │   E ─ ENGAGE                                                             │
    │   ════════════════════════════════════════════════════════════════════   │
    │   • NOW and ONLY NOW, recommend the pathway                              │
    │   • The recommendation should feel like advice from a caring friend      │
    │   • Not a cold algorithm match - a thoughtful, personal suggestion       │
    │   • Explain WHY this pathway fits THEIR unique journey                   │
    │                                                                          │
    │   Example: "Based on everything you've shared, I believe the             │
    │            'Overcoming Anxiety' pathway will meet you right where        │
    │            you are and walk with you toward the peace you're seeking."   │
    │                                                                          │
    └─────────────────────────────────────────────────────────────────────────┘
```

### Crisis Detection (Highest Priority)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                      ⚠️  CRISIS DETECTION  ⚠️                                │
└─────────────────────────────────────────────────────────────────────────────┘

    If ANY answer indicates:
    ┌─────────────────────────────────────────────────────────────────────────┐
    │  • Self-harm or suicidal thoughts                                        │
    │    ("end my life", "no point", "want to die", "give up")                │
    │  • Severe hopelessness or despair                                        │
    │  • Immediate danger or abuse                                             │
    │  • Expressions of complete hopelessness                                  │
    └─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
    ┌─────────────────────────────────────────────────────────────────────────┐
    │  IMMEDIATE RESPONSE:                                                     │
    │  ════════════════════════════════════════════════════════════════════   │
    │  • ALWAYS recommend "Crisis Support" pathway                             │
    │  • next_step_message MUST include:                                       │
    │    - Caring urgency                                                      │
    │    - "You're not alone"                                                  │
    │    - Help is available                                                   │
    │    - They matter and are valued                                          │
    │  • Be gentle but clear that help exists                                  │
    └─────────────────────────────────────────────────────────────────────────┘
```

### Response Style Guidelines

| Aspect | Guideline |
|--------|-----------|
| **Tone** | Warm, human, deeply caring - like a wise friend |
| **Reasoning** | Shows understanding of the PERSON, not just keywords |
| **Next Step Message** | Feels like a warm hug in words - personal, encouraging |
| **Avoid** | Being preachy, robotic, or generic |
| **Include** | Acknowledgment of their specific situation and feelings |

### How AI Analyzes Responses

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                     AI DECISION MAKING PROCESS                               │
│                    (After RELATE Framework Processing)                       │
└─────────────────────────────────────────────────────────────────────────────┘

                        USER ANSWERS
                             │
                             ▼
              ┌──────────────────────────────┐
              │   RELATE FRAMEWORK APPLIED   │
              │   (See above for details)    │
              └──────────────────────────────┘
                             │
                             ▼
              ┌──────────────────────────────┐
              │     PATTERN RECOGNITION      │
              └──────────────────────────────┘
                             │
           ┌─────────────────┼─────────────────┐
           │                 │                 │
           ▼                 ▼                 ▼
    ┌─────────────┐   ┌─────────────┐   ┌─────────────┐
    │  SPIRITUAL  │   │  EMOTIONAL  │   │   PRIMARY   │
    │    STAGE    │   │    STATE    │   │    NEED     │
    └──────┬──────┘   └──────┬──────┘   └──────┬──────┘
           │                 │                 │
           ▼                 ▼                 ▼

    ┌─────────────────────────────────────────────────────────────────┐
    │                    SPIRITUAL STAGE                               │
    ├─────────────────────────────────────────────────────────────────┤
    │                                                                  │
    │  SEEKER                                                          │
    │  ├─ Not familiar with Jesus                                      │
    │  ├─ Haven't read religious texts                                 │
    │  ├─ New to Christianity (entry_type: no_im_new)                  │
    │  └─ Curious about spirituality                                   │
    │                                                                  │
    │  NEW_BELIEVER                                                    │
    │  ├─ Recently started believing                                   │
    │  ├─ Some familiarity with Jesus                                  │
    │  ├─ Learning basic concepts                                      │
    │  └─ Needs foundation building                                    │
    │                                                                  │
    │  GROWING_BELIEVER                                                │
    │  ├─ Regularly reads Bible                                        │
    │  ├─ Prays frequently                                             │
    │  ├─ Deep relationship with Jesus                                 │
    │  └─ Actively involved in church                                  │
    │                                                                  │
    │  STRUGGLING_BELIEVER                                             │
    │  ├─ Knows Christianity but distant                               │
    │  ├─ Inconsistent prayer/Bible reading                            │
    │  ├─ Facing challenges                                            │
    │  └─ Needs reconnection                                           │
    │                                                                  │
    └─────────────────────────────────────────────────────────────────┘

    ┌─────────────────────────────────────────────────────────────────┐
    │                    EMOTIONAL STATE                               │
    ├─────────────────────────────────────────────────────────────────┤
    │                                                                  │
    │  CURIOUS    - Open to learning, asking questions                 │
    │  ANXIOUS    - Worried, fearful, stressed                         │
    │  CONFUSED   - Uncertain, needs clarity                           │
    │  OPEN       - Receptive, willing to explore                      │
    │  HOPEFUL    - Positive outlook, seeking growth                   │
    │  PAINFUL    - Hurting, grieving, in crisis                       │
    │  DISTRESSED - Urgent need, crisis situation                      │
    │                                                                  │
    └─────────────────────────────────────────────────────────────────┘

    ┌─────────────────────────────────────────────────────────────────┐
    │                    PRIMARY NEED                                  │
    ├─────────────────────────────────────────────────────────────────┤
    │                                                                  │
    │  SALVATION     - Needs to know Jesus, gospel                     │
    │  PEACE         - Needs calm, anxiety relief                      │
    │  UNDERSTANDING - Needs Bible knowledge, clarity                  │
    │  PURPOSE       - Needs direction, calling                        │
    │  HEALING       - Needs emotional/spiritual healing               │
    │  GROWTH        - Needs to deepen faith                           │
    │  GUIDANCE      - Needs wisdom for decisions                      │
    │                                                                  │
    └─────────────────────────────────────────────────────────────────┘

                             │
                             ▼
              ┌──────────────────────────────┐
              │     PATHWAY MATCHING         │
              └──────────────────────────────┘
                             │
                             ▼

    ┌─────────────────────────────────────────────────────────────────┐
    │                 PATHWAY SELECTION LOGIC                          │
    ├─────────────────────────────────────────────────────────────────┤
    │                                                                  │
    │  IF spiritual_stage = SEEKER:                                    │
    │     → Discovering Jesus (7-10 days)                              │
    │                                                                  │
    │  IF spiritual_stage = NEW_BELIEVER:                              │
    │     → New Believer Foundations (14 days)                         │
    │                                                                  │
    │  IF emotional_state = ANXIOUS or primary_need = PEACE:           │
    │     → Overcoming Anxiety (10-14 days)                            │
    │     OR Growing in Prayer (7 days)                                │
    │                                                                  │
    │  IF primary_need = PURPOSE:                                      │
    │     → Finding Purpose & Calling (14-21 days)                     │
    │                                                                  │
    │  IF primary_need = UNDERSTANDING:                                │
    │     → Understanding the Bible (10-14 days)                       │
    │                                                                  │
    │  IF emotional_state = PAINFUL + grief indicators:                │
    │     → Healing from Grief (21-30 days)                            │
    │                                                                  │
    │  IF financial concerns detected:                                 │
    │     → Financial Stewardship (14-21 days)                         │
    │                                                                  │
    │  IF relationship/marriage concerns:                              │
    │     → Marriage & Relationships (14-21 days)                      │
    │                                                                  │
    │  IF parenting concerns:                                          │
    │     → Parenting with Faith (14 days)                             │
    │                                                                  │
    │  IF emotional_state = DISTRESSED or crisis keywords:             │
    │     → Crisis Support (Variable) [HIGH PRIORITY]                  │
    │                                                                  │
    └─────────────────────────────────────────────────────────────────┘
```

### Confidence Score Meaning

| Confidence | Meaning |
|------------|---------|
| 0.90 - 1.00 | Very confident - Clear pattern match |
| 0.75 - 0.89 | Confident - Strong indicators |
| 0.60 - 0.74 | Moderate - Some ambiguity |
| 0.40 - 0.59 | Low - Multiple possible pathways |
| < 0.40 | Very low - Consider alternatives |

---

## 6. API Endpoints Detailed

### Endpoint Summary

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          API ENDPOINTS                                       │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  PUBLIC (No Auth Required)                                                   │
│  ═════════════════════════                                                   │
│                                                                              │
│  GET  /           → API information and endpoint list                        │
│  GET  /health     → Server health and configuration status                   │
│                                                                              │
│  PROTECTED (X-API-Key Required)                                              │
│  ══════════════════════════════                                              │
│                                                                              │
│  GET  /questions/{entry_type}  → Get questionnaire questions                 │
│  GET  /pathways                → List all available pathways                 │
│  POST /recommend               → Get AI pathway recommendation               │
│  GET  /users/{user_id}/history → Get user's recommendation history           │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Request/Response Flow for Each Endpoint

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  GET /questions/{entry_type}                                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  Purpose: Retrieve questions to display to user                              │
│                                                                              │
│  Flow:                                                                       │
│  1. Verify API key                                                           │
│  2. Read questions.json file                                                 │
│  3. Return questions for specified entry_type                                │
│                                                                              │
│  entry_type = "no_im_new":                                                   │
│  └─ 10 questions for people new to Christianity                              │
│     • Interest in spirituality                                               │
│     • Background in spiritual learning                                       │
│     • Familiarity with Jesus                                                 │
│     • Motivation for exploring                                               │
│     • Learning style preference                                              │
│     • Openness to new beliefs                                                │
│                                                                              │
│  entry_type = "yes_i_know":                                                  │
│  └─ 10 questions for existing believers                                      │
│     • Bible reading frequency                                                │
│     • Prayer life description                                                │
│     • Relationship with Jesus                                                │
│     • Areas needing growth                                                   │
│     • Church involvement                                                     │
│     • Spiritual goals                                                        │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│  POST /recommend                                                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  Purpose: Main API - Process answers and get AI recommendation               │
│                                                                              │
│  Flow:                                                                       │
│  ┌────────────────────────────────────────────────────────────────────┐     │
│  │ 1. AUTHENTICATE                                                     │     │
│  │    └─ Verify X-API-Key header                                       │     │
│  ├────────────────────────────────────────────────────────────────────┤     │
│  │ 2. GET/CREATE USER                                                  │     │
│  │    └─ Find existing user by external_user_id OR create new          │     │
│  ├────────────────────────────────────────────────────────────────────┤     │
│  │ 3. STORE ANSWERS                                                    │     │
│  │    └─ Save questionnaire response to database                       │     │
│  ├────────────────────────────────────────────────────────────────────┤     │
│  │ 4. CHECK CACHE                                                      │     │
│  │    ├─ Generate cache key from answers                               │     │
│  │    └─ If cached → return cached result                              │     │
│  ├────────────────────────────────────────────────────────────────────┤     │
│  │ 5. CALL AI (if not cached)                                          │     │
│  │    ├─ Format prompt with user answers                               │     │
│  │    ├─ Send to OpenRouter (Mistral 7B)                               │     │
│  │    ├─ Parse JSON response                                           │     │
│  │    └─ Store in cache                                                │     │
│  ├────────────────────────────────────────────────────────────────────┤     │
│  │ 6. STORE RECOMMENDATION                                             │     │
│  │    └─ Save AI recommendation to database                            │     │
│  ├────────────────────────────────────────────────────────────────────┤     │
│  │ 7. RETURN RESPONSE                                                  │     │
│  │    └─ Return recommendation + user_id + recommendation_id           │     │
│  └────────────────────────────────────────────────────────────────────┘     │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 7. Authentication System

### How Authentication Works

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                      AUTHENTICATION FLOW                                     │
└─────────────────────────────────────────────────────────────────────────────┘

    Client Request                              Server Processing
         │                                            │
         │  Headers:                                  │
         │  X-API-Key: logosreach-api-xxx...          │
         │                                            │
         └────────────────────┬───────────────────────┘
                              │
                              ▼
                    ┌─────────────────────┐
                    │  auth.py            │
                    │  verify_api_key()   │
                    └──────────┬──────────┘
                               │
                    ┌──────────▼──────────┐
                    │  Is X-API-Key       │
                    │  header present?    │
                    └──────────┬──────────┘
                               │
              ┌────────────────┼────────────────┐
              │ NO             │            YES │
              ▼                │                ▼
    ┌─────────────────┐        │      ┌─────────────────┐
    │ Return 401      │        │      │ Does key match  │
    │ "Missing API    │        │      │ settings.API_KEY│
    │  key"           │        │      └────────┬────────┘
    └─────────────────┘        │               │
                               │    ┌──────────┼──────────┐
                               │    │ NO       │      YES │
                               │    ▼          │          ▼
                               │ ┌─────────┐   │   ┌─────────────┐
                               │ │Return   │   │   │ ALLOW       │
                               │ │403      │   │   │ Request to  │
                               │ │"Invalid │   │   │ proceed     │
                               │ │API key" │   │   └─────────────┘
                               │ └─────────┘   │
                               │               │
                               └───────────────┘


    Code Location: auth.py
    ════════════════════════════════════════════════════════════════

    async def verify_api_key(api_key: str = Security(API_KEY_HEADER)) -> str:

        if not settings.API_KEY:
            raise HTTPException(500, "API key not configured on server")

        if not api_key:
            raise HTTPException(401, "Missing API key")

        if api_key != settings.API_KEY:
            raise HTTPException(403, "Invalid API key")

        return api_key
```

### Security Best Practices

| Practice | Implementation |
|----------|----------------|
| API Key in Header | X-API-Key header (not URL parameter) |
| Environment Variable | API_KEY stored in .env file |
| Secure Key Generation | `openssl rand -hex 32` |
| HTTPS | Use HTTPS in production |
| Key Rotation | Change API key periodically |

---

## 8. Caching Strategy

### Cache Implementation

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         CACHING SYSTEM                                       │
└─────────────────────────────────────────────────────────────────────────────┘

    Purpose: Reduce AI API calls for identical answer patterns

    Library: cachetools.TTLCache

    Configuration:
    ┌─────────────────────────────────────┐
    │  maxsize = 1000 entries             │
    │  ttl = 3600 seconds (1 hour)        │
    └─────────────────────────────────────┘

    Cache Key Generation:
    ════════════════════════════════════════════════════════════════

    Input:
    {
        "entry_type": "no_im_new",
        "answers": {
            "Q1": "Very interested",
            "Q2": "Personal experiences",
            ...
        }
    }

    Process:
    1. Sort answers dictionary
    2. Convert to JSON string
    3. Generate MD5 hash

    Output: "a1b2c3d4e5f6..." (32 character hash)


    Cache Flow:
    ════════════════════════════════════════════════════════════════

              ┌─────────────────┐
              │  New Request    │
              └────────┬────────┘
                       │
                       ▼
              ┌─────────────────┐
              │ Generate cache  │
              │ key from answers│
              └────────┬────────┘
                       │
              ┌────────▼────────┐
              │ Key in cache?   │
              └────────┬────────┘
                       │
           ┌───────────┼───────────┐
           │ YES       │       NO  │
           ▼           │           ▼
    ┌─────────────┐    │    ┌─────────────┐
    │ CACHE HIT   │    │    │ CACHE MISS  │
    │             │    │    │             │
    │ Return      │    │    │ Call AI API │
    │ cached      │    │    │ (2-5 sec)   │
    │ response    │    │    │             │
    │ (~50ms)     │    │    │ Store in    │
    │             │    │    │ cache       │
    └─────────────┘    │    └─────────────┘
                       │
                       │

    Benefits:
    ════════════════════════════════════════════════════════════════

    • Same answers = instant response (no AI call)
    • Reduces OpenRouter API costs
    • Improves response time from 2-5s to ~50ms
    • Automatic expiry after 1 hour (fresh recommendations)
```

---

## 9. Scalability Features

### Async Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                      SCALABILITY FEATURES                                    │
└─────────────────────────────────────────────────────────────────────────────┘

    1. ASYNC DATABASE OPERATIONS
    ════════════════════════════════════════════════════════════════

    Before (Sync - Blocking):
    ┌─────────────────────────────────────────────────────────────┐
    │ Request 1 ───────[DB Query]───────────────────────────────► │
    │ Request 2         (waiting)      ───[DB Query]────────────► │
    │ Request 3                        (waiting)    ──[DB Query]► │
    └─────────────────────────────────────────────────────────────┘

    After (Async - Non-blocking):
    ┌─────────────────────────────────────────────────────────────┐
    │ Request 1 ───────[DB Query]─────────────────────────────►   │
    │ Request 2 ───────[DB Query]─────────────────────────────►   │
    │ Request 3 ───────[DB Query]─────────────────────────────►   │
    └─────────────────────────────────────────────────────────────┘

    Implementation: SQLAlchemy AsyncSession + asyncpg


    2. CONNECTION POOLING
    ════════════════════════════════════════════════════════════════

    Database Pool:
    ┌─────────────────────────────────────┐
    │  pool_size = 20 connections         │
    │  max_overflow = 40 extra            │
    │  Total possible = 60 connections    │
    │  pool_timeout = 30 seconds          │
    │  pool_recycle = 1800 seconds        │
    └─────────────────────────────────────┘

    HTTP Client Pool (for AI API):
    ┌─────────────────────────────────────┐
    │  max_keepalive_connections = 20     │
    │  max_connections = 100              │
    │  keepalive_expiry = 30 seconds      │
    └─────────────────────────────────────┘


    3. MULTI-WORKER DEPLOYMENT
    ════════════════════════════════════════════════════════════════

    Single Worker:
    ┌─────────────────┐
    │    Worker 1     │ ← All requests
    └─────────────────┘

    Multi-Worker (Production):
    ┌─────────────────┐
    │    Worker 1     │ ← 25% requests
    ├─────────────────┤
    │    Worker 2     │ ← 25% requests
    ├─────────────────┤
    │    Worker 3     │ ← 25% requests
    ├─────────────────┤
    │    Worker 4     │ ← 25% requests
    └─────────────────┘

    Command: uvicorn main:app --workers 4


    4. PERFORMANCE COMPARISON
    ════════════════════════════════════════════════════════════════

    ┌──────────────────────┬─────────────┬─────────────┐
    │ Scenario             │ Before      │ After       │
    ├──────────────────────┼─────────────┼─────────────┤
    │ Cache hit            │ N/A         │ ~50ms       │
    │ Cache miss (AI call) │ 2-5s        │ 2-5s        │
    │ DB operations        │ Blocking    │ Non-blocking│
    │ Concurrent users     │ ~10         │ ~500+       │
    │ Workers              │ 1           │ 4           │
    └──────────────────────┴─────────────┴─────────────┘
```

---

## 10. File Structure

```
LogosReach/
│
├── main.py                    # FastAPI application entry point
│   └── Endpoints, lifespan, CORS configuration
│
├── config.py                  # Application settings
│   └── API keys, database URL, pathways list
│
├── auth.py                    # Authentication module
│   └── API key verification function
│
├── database.py                # Database configuration
│   └── Async engine, session factory, init functions
│
├── db_models.py               # SQLAlchemy ORM models
│   └── User, QuestionnaireResponse, PathwayRecommendation
│
├── models.py                  # Pydantic request/response models
│   └── RecommendationRequest, RecommendationResponse, etc.
│
├── services/
│   ├── __init__.py
│   └── recommendation_service.py   # Core business logic
│       └── AI calls, caching, database operations
│
├── questions.json             # Questionnaire configuration
│   └── Questions for both entry types
│
├── .env                       # Environment variables (not in git)
│   └── API_KEY, OPENROUTER_API_KEY, DATABASE_URL
│
├── .env.example               # Environment template
│
├── requirements.txt           # Python dependencies
│
├── reset_tables.sql           # Database reset script
│
├── API_TESTING_GUIDE.md       # API testing documentation
│
└── SYSTEM_DOCUMENTATION.md    # This file
```

---

## 11. Configuration

### Environment Variables

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                      ENVIRONMENT CONFIGURATION                               │
└─────────────────────────────────────────────────────────────────────────────┘

    File: .env
    ════════════════════════════════════════════════════════════════

    # OpenRouter AI Configuration
    OPENROUTER_API_KEY=sk-or-v1-xxxxxxxxxxxx

    # API Authentication
    API_KEY=logosreach-api-xxxxxxxxxxxx

    # Database
    DATABASE_URL=postgresql://user:pass@localhost:5432/logosreach

    # Debug Mode
    DEBUG=false


    Variable Details:
    ════════════════════════════════════════════════════════════════

    ┌─────────────────────┬─────────────────────────────────────────┐
    │ Variable            │ Description                             │
    ├─────────────────────┼─────────────────────────────────────────┤
    │ OPENROUTER_API_KEY  │ API key for OpenRouter.ai               │
    │                     │ Get from: https://openrouter.ai/keys    │
    ├─────────────────────┼─────────────────────────────────────────┤
    │ API_KEY             │ Your API key for authenticating         │
    │                     │ requests to LogosReach                  │
    │                     │ Generate: openssl rand -hex 32          │
    ├─────────────────────┼─────────────────────────────────────────┤
    │ DATABASE_URL        │ PostgreSQL connection string            │
    │                     │ Format: postgresql://user:pass@host/db  │
    ├─────────────────────┼─────────────────────────────────────────┤
    │ DEBUG               │ Enable debug mode (true/false)          │
    │                     │ Enables: SQL logging, hot reload        │
    └─────────────────────┴─────────────────────────────────────────┘
```

---

## 12. Error Handling

### Error Response Format

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         ERROR HANDLING                                       │
└─────────────────────────────────────────────────────────────────────────────┘

    Standard Error Response:
    ════════════════════════════════════════════════════════════════

    {
        "success": false,
        "error": "Error description here",
        "data": null
    }

    OR (for HTTP exceptions):

    {
        "detail": "Error description here"
    }


    Error Types and Codes:
    ════════════════════════════════════════════════════════════════

    ┌──────┬─────────────────────────────────────────────────────────┐
    │ Code │ Meaning                                                 │
    ├──────┼─────────────────────────────────────────────────────────┤
    │ 400  │ Bad Request - Invalid input data                        │
    │      │ Example: Invalid entry_type, missing required fields    │
    ├──────┼─────────────────────────────────────────────────────────┤
    │ 401  │ Unauthorized - Missing API key                          │
    │      │ Example: No X-API-Key header provided                   │
    ├──────┼─────────────────────────────────────────────────────────┤
    │ 403  │ Forbidden - Invalid API key                             │
    │      │ Example: Wrong API key provided                         │
    ├──────┼─────────────────────────────────────────────────────────┤
    │ 404  │ Not Found - Resource doesn't exist                      │
    │      │ Example: User or recommendation not found               │
    ├──────┼─────────────────────────────────────────────────────────┤
    │ 500  │ Internal Server Error - Server-side issue               │
    │      │ Example: Database error, AI API failure                 │
    └──────┴─────────────────────────────────────────────────────────┘


    Error Handling Flow:
    ════════════════════════════════════════════════════════════════

              ┌─────────────────┐
              │    Request      │
              └────────┬────────┘
                       │
                       ▼
              ┌─────────────────┐
              │   Try Block     │
              └────────┬────────┘
                       │
              ┌────────▼────────┐
              │  Error Occurs?  │
              └────────┬────────┘
                       │
           ┌───────────┼───────────┐
           │ NO        │       YES │
           ▼           │           ▼
    ┌─────────────┐    │    ┌─────────────────────┐
    │ Return      │    │    │ Catch Exception     │
    │ Success     │    │    │                     │
    │ Response    │    │    │ ValueError → 400    │
    │             │    │    │ HTTPException → xxx │
    │             │    │    │ Other → 500         │
    └─────────────┘    │    └─────────────────────┘
                       │
                       │

    Common Error Scenarios:
    ════════════════════════════════════════════════════════════════

    1. Missing API Key:
       Request without X-API-Key header
       → 401: {"detail": "Missing API key. Please provide X-API-Key header."}

    2. Invalid API Key:
       Request with wrong X-API-Key
       → 403: {"detail": "Invalid API key"}

    3. Invalid Entry Type:
       entry_type not "yes_i_know" or "no_im_new"
       → 422: {"detail": "Invalid entry_type"}

    4. OpenRouter API Key Missing:
       OPENROUTER_API_KEY not set
       → 400: {"detail": "OPENROUTER_API_KEY is not set"}

    5. AI Response Parse Error:
       AI returns invalid JSON
       → 500: {"success": false, "error": "Failed to parse AI response"}

    6. Database Connection Error:
       PostgreSQL not reachable
       → 500: {"success": false, "error": "Database connection failed"}
```

---

## Summary

LogosReach is a complete AI-powered **recommendation-only** system that:

1. **Receives** questionnaire answers from your backend
2. **Authenticates** requests using API key
3. **Stores** user data and responses in PostgreSQL
4. **Analyzes** responses using Mistral 7B AI
5. **Recommends** personalized spiritual pathways

The system is designed for **scalability** (async operations, caching, connection pooling) and **security** (API key authentication).

**Note:** This system is focused on pathway **recommendation only**. Enrollment tracking and pathway progress management should be handled by your own backend system using the `recommendation_id` returned from the `/recommend` endpoint.
