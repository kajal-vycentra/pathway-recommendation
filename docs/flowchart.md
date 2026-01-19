# LogosReach Pathway Recommendation Flowchart

## The RELATE Framework Flow

```mermaid
graph TB
    Start([User Submits Questionnaire]) --> ReceiveInput[Receive User Answers]

    ReceiveInput --> RELATEFramework[RELATE Framework Processing]

    %% RELATE Framework Stages
    RELATEFramework --> R[R - RECOGNIZE<br/>Who is this person?<br/>What is their situation?]
    R --> E1[E - EMPATHIZE<br/>What emotions are they feeling?<br/>Feel what they're feeling]
    E1 --> L[L - LISTEN<br/>What are they REALLY saying?<br/>Deeper needs beneath surface]
    L --> A[A - AFFIRM<br/>Acknowledge their courage<br/>See their strengths]
    A --> T[T - TRUST<br/>Make them feel safe<br/>Build connection]
    T --> E2[E - ENGAGE<br/>NOW recommend pathway<br/>Like a caring friend]

    %% Crisis Check (Parallel to RELATE)
    ReceiveInput --> CrisisCheck{Crisis Keywords<br/>Detected?}

    CrisisCheck -->|Yes - Self-harm<br/>Hopelessness<br/>Danger| CrisisPath[🚨 CRISIS SUPPORT<br/>Variable Duration<br/>IMMEDIATE PRIORITY]

    CrisisCheck -->|No| RELATEFramework

    E2 --> AIAnalysis[AI Analysis Engine]

    AIAnalysis --> Extract[Extract Key Information]

    Extract --> Keywords[Identify Keywords]
    Extract --> Topics[Identify Topics]
    Extract --> Intent[Determine User Intent]
    Extract --> Sentiment[Analyze Sentiment/Emotions]

    Keywords --> Classify{Classify Based on<br/>RELATE Understanding}
    Topics --> Classify
    Intent --> Classify
    Sentiment --> Classify

    %% Main Classification Branches
    Classify -->|Seeker/New to Faith| SalvationBranch{Spiritual Stage?}
    Classify -->|Ready for Baptism| BaptismPath[Pathway 3:<br/>Water Baptism<br/>7 days]
    Classify -->|Prayer Needs| PrayerBranch{Type of<br/>Prayer Need?}
    Classify -->|Bible Understanding| BiblePath[Pathway 5:<br/>Understanding the Bible<br/>10-14 days]
    Classify -->|Purpose/Direction| PurposePath[Pathway 6:<br/>Finding Purpose & Calling<br/>14-21 days]
    Classify -->|Relationship Issues| RelationshipBranch{Marriage or<br/>General?}
    Classify -->|Parenting Challenges| ParentingPath[Pathway 8:<br/>Parenting with Faith<br/>14 days]
    Classify -->|Anxiety/Fear/Worry| AnxietyPath[Pathway 9:<br/>Overcoming Anxiety<br/>10-14 days]
    Classify -->|Grief/Loss| GriefPath[Pathway 10:<br/>Healing from Grief<br/>21-30 days]
    Classify -->|Financial Concerns| FinancePath[Pathway 11:<br/>Financial Stewardship<br/>14-21 days]

    %% Salvation Branch
    SalvationBranch -->|Not a Believer/Seeker| SalvationPath[Pathway 1:<br/>Discovering Jesus<br/>7-10 days]
    SalvationBranch -->|New Believer| NewBelieverPath[Pathway 2:<br/>New Believer Foundations<br/>14 days]

    %% Prayer Branch
    PrayerBranch -->|Learning to Pray| PrayerPath1[Pathway 4:<br/>Growing in Prayer<br/>7 days]
    PrayerBranch -->|Peace/Anxiety Related| AnxietyPath

    %% Relationship Branch
    RelationshipBranch -->|Marriage Issues| MarriagePath[Pathway 7:<br/>Marriage & Relationships<br/>14-21 days]
    RelationshipBranch -->|General Relationships| MarriagePath

    %% All Pathways Lead to Response Generation
    SalvationPath --> GenerateResponse
    NewBelieverPath --> GenerateResponse
    BaptismPath --> GenerateResponse
    PrayerPath1 --> GenerateResponse
    BiblePath --> GenerateResponse
    PurposePath --> GenerateResponse
    MarriagePath --> GenerateResponse
    ParentingPath --> GenerateResponse
    AnxietyPath --> GenerateResponse
    GriefPath --> GenerateResponse
    FinancePath --> GenerateResponse
    CrisisPath --> GenerateResponse

    %% Response Generation with RELATE Principles
    GenerateResponse[Generate RELATE-Style Response]

    GenerateResponse --> Reasoning[Craft Reasoning<br/>Show understanding of PERSON<br/>Not just keyword matching]

    Reasoning --> NextStep[Craft Next Step Message<br/>Warm, personal, encouraging<br/>Like advice from a caring friend]

    NextStep --> FinalResponse[Return Recommendation<br/>with Empathy & Care]

    FinalResponse --> Complete([Pathway Recommendation<br/>Delivered with Compassion])

    %% Styling
    classDef relateStyle fill:#e8f5e9,stroke:#2e7d32,stroke-width:3px
    classDef crisisStyle fill:#ffebee,stroke:#c62828,stroke-width:3px
    classDef pathwayStyle fill:#e3f2fd,stroke:#1565c0,stroke-width:2px
    classDef decisionStyle fill:#fff3e0,stroke:#ef6c00,stroke-width:2px
    classDef responseStyle fill:#f3e5f5,stroke:#7b1fa2,stroke-width:2px

    class R,E1,L,A,T,E2,RELATEFramework relateStyle
    class CrisisPath,CrisisCheck crisisStyle
    class SalvationPath,NewBelieverPath,BaptismPath,PrayerPath1,BiblePath,PurposePath,MarriagePath,ParentingPath,AnxietyPath,GriefPath,FinancePath pathwayStyle
    class Classify,SalvationBranch,PrayerBranch,RelationshipBranch decisionStyle
    class GenerateResponse,Reasoning,NextStep,FinalResponse responseStyle
```

---

## RELATE Framework Detail

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        THE RELATE FRAMEWORK                                  │
│              "Build Relationship First, Then Recommend"                      │
└─────────────────────────────────────────────────────────────────────────────┘

    Before ANY pathway recommendation, the AI processes through ALL stages:

    ╔═══════════════════════════════════════════════════════════════════════╗
    ║  R ─ RECOGNIZE                                                         ║
    ╠═══════════════════════════════════════════════════════════════════════╣
    ║  • Who is this person from their answers?                              ║
    ║  • What is their current life situation?                               ║
    ║  • Are they new to faith or experienced?                               ║
    ║  • NO teaching or advice yet - just understanding                      ║
    ╚═══════════════════════════════════════════════════════════════════════╝
                                    │
                                    ▼
    ╔═══════════════════════════════════════════════════════════════════════╗
    ║  E ─ EMPATHIZE                                                         ║
    ╠═══════════════════════════════════════════════════════════════════════╣
    ║  • Reflect their emotions (anxiety, grief, hope, fear, curiosity)      ║
    ║  • Put yourself in their shoes                                         ║
    ║  • Validate feelings without judgment                                  ║
    ║  • NO scripture quotes or solutions yet                                ║
    ╚═══════════════════════════════════════════════════════════════════════╝
                                    │
                                    ▼
    ╔═══════════════════════════════════════════════════════════════════════╗
    ║  L ─ LISTEN                                                            ║
    ╠═══════════════════════════════════════════════════════════════════════╣
    ║  • What are they REALLY saying beneath the surface?                    ║
    ║  • What's the deeper need not explicitly stated?                       ║
    ║  • Read between the lines with compassion                              ║
    ║  • Listen 80%, speak 20%                                               ║
    ╚═══════════════════════════════════════════════════════════════════════╝
                                    │
                                    ▼
    ╔═══════════════════════════════════════════════════════════════════════╗
    ║  A ─ AFFIRM                                                            ║
    ╠═══════════════════════════════════════════════════════════════════════╣
    ║  • Affirm their courage in sharing/seeking help                        ║
    ║  • Highlight strengths you notice in them                              ║
    ║  • Seeking help IS strength - acknowledge this                         ║
    ║  • Still NO theology or pathways                                       ║
    ╚═══════════════════════════════════════════════════════════════════════╝
                                    │
                                    ▼
    ╔═══════════════════════════════════════════════════════════════════════╗
    ║  T ─ TRUST                                                             ║
    ╠═══════════════════════════════════════════════════════════════════════╣
    ║  • Build safety and credibility                                        ║
    ║  • Make them feel seen and understood                                  ║
    ║  • They need to know someone cares                                     ║
    ║  • Create connection through words                                     ║
    ╚═══════════════════════════════════════════════════════════════════════╝
                                    │
                                    ▼
    ╔═══════════════════════════════════════════════════════════════════════╗
    ║  E ─ ENGAGE                                                            ║
    ╠═══════════════════════════════════════════════════════════════════════╣
    ║  • ONLY NOW introduce pathway recommendation                           ║
    ║  • Like advice from a caring friend, not an algorithm                  ║
    ║  • Explain WHY this pathway fits THEIR unique journey                  ║
    ║  • Warm, personal, encouraging message                                 ║
    ╚═══════════════════════════════════════════════════════════════════════╝
```

---

## Crisis Detection Flow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                      ⚠️  CRISIS DETECTION  ⚠️                                │
│                        (HIGHEST PRIORITY)                                    │
└─────────────────────────────────────────────────────────────────────────────┘

                        USER ANSWERS
                             │
                             ▼
              ┌──────────────────────────────┐
              │     SCAN FOR CRISIS          │
              │     INDICATORS               │
              └──────────────────────────────┘
                             │
            ┌────────────────┴────────────────┐
            │                                 │
            ▼                                 ▼
    ┌───────────────┐                 ┌───────────────┐
    │ CRISIS        │                 │ NO CRISIS     │
    │ DETECTED      │                 │ DETECTED      │
    └───────┬───────┘                 └───────┬───────┘
            │                                 │
            ▼                                 ▼
    ┌───────────────────────┐         ┌───────────────────────┐
    │ INDICATORS:           │         │ Continue with         │
    │ • "end my life"       │         │ normal RELATE         │
    │ • "no point"          │         │ framework             │
    │ • "want to die"       │         │ processing            │
    │ • "give up"           │         │                       │
    │ • severe hopelessness │         │                       │
    │ • abuse/danger        │         │                       │
    └───────┬───────────────┘         └───────────────────────┘
            │
            ▼
    ┌───────────────────────────────────────────────────────────┐
    │  🚨 IMMEDIATE ACTION:                                      │
    │  ─────────────────────────────────────────────────────────│
    │  • ALWAYS recommend "Crisis Support" pathway               │
    │  • Override all other pathway logic                        │
    │                                                            │
    │  next_step_message MUST include:                           │
    │  ─────────────────────────────────────────────────────────│
    │  ✓ Caring urgency                                          │
    │  ✓ "You're not alone"                                      │
    │  ✓ "Help is available"                                     │
    │  ✓ "You matter and are valued"                             │
    │  ✓ Gentle but clear that help exists                       │
    └───────────────────────────────────────────────────────────┘
```

---

## Response Style Comparison

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    BEFORE vs AFTER RELATE FRAMEWORK                          │
└─────────────────────────────────────────────────────────────────────────────┘

    ❌ BEFORE (Cold/Robotic):
    ═══════════════════════════════════════════════════════════════════════════

    {
      "reasoning": "User shows signs of anxiety based on Q2 and Q5 responses.
                    Keyword matching indicates need for peace pathway.",

      "next_step_message": "Start the Overcoming Anxiety pathway to find peace."
    }


    ✅ AFTER (RELATE Framework - Warm/Human):
    ═══════════════════════════════════════════════════════════════════════════

    {
      "reasoning": "I can sense the weight you're carrying - the constant worry
                    and fear that keeps you up at night. It takes real courage
                    to acknowledge this and seek help. You're not weak for
                    feeling anxious; you're brave for taking this step toward
                    peace.",

      "next_step_message": "Friend, I see you. The anxiety you're feeling is
                           real, and you don't have to carry it alone. I'd love
                           for you to start the 'Overcoming Anxiety' journey -
                           it's designed specifically for moments like yours,
                           where peace feels far away but hope is closer than
                           you think. You've already taken the hardest step by
                           being honest about where you are. Let's walk this
                           path together."
    }
```

---

## Available Pathways

| # | Pathway | Duration | Theme |
|---|---------|----------|-------|
| 1 | Discovering Jesus | 7-10 days | Seekers, new to Christianity, curious about faith |
| 2 | New Believer Foundations | 14 days | Recently believed, needs basics of faith |
| 3 | Water Baptism | 7 days | Ready to publicly declare faith |
| 4 | Growing in Prayer | 7 days | Learning to pray, seeking peace, trusting God |
| 5 | Understanding the Bible | 10-14 days | Confused about scripture, wants deeper context |
| 6 | Finding Purpose & Calling | 14-21 days | Seeking direction, meaning, life purpose |
| 7 | Marriage & Relationships | 14-21 days | Marriage struggles, relationship issues |
| 8 | Parenting with Faith | 14 days | Raising children in faith |
| 9 | Overcoming Anxiety | 10-14 days | Worry, fear, stress, need for peace |
| 10 | Healing from Grief | 21-30 days | Loss, mourning, bereavement |
| 11 | Financial Stewardship | 14-21 days | Money struggles, debt, stewardship |
| 12 | Crisis Support | Variable | **PRIORITY** - Urgent help, hopelessness, emergency |

---

## Key Principles

1. **Relationship First** - Build connection before recommendation
2. **Empathy Always** - Feel what they're feeling
3. **Person, Not Keywords** - Understand the human, not just match patterns
4. **Crisis Priority** - Safety always comes first
5. **Warm Responses** - Like a caring friend, never a cold algorithm
