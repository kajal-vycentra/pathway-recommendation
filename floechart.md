graph TB
Start([Asks Question]) --> ReceiveInput[Receive User Input]

    ReceiveInput --> AIAnalysis[AI Analysis Engine]

    AIAnalysis --> Extract[Extract Key Information]

    Extract --> Keywords[Identify Keywords]
    Extract --> Topics[Identify Topics]
    Extract --> Intent[Determine User Intent]
    Extract --> Sentiment[Analyze Sentiment]

    Keywords --> Classify{Classify Question Category}
    Topics --> Classify
    Intent --> Classify
    Sentiment --> Classify

    %% Main Classification Branches
    Classify -->|Salvation/Gospel Keywords| SalvationBranch{Is User a Believer?}
    Classify -->|Baptism Keywords| BaptismPath[Pathway 3:<br/>Water Baptism<br/>7 days]
    Classify -->|Prayer Keywords| PrayerBranch{What Type of<br/>Prayer Need?}
    Classify -->|Bible Study Keywords| BiblePath[Pathway 5:<br/>Understanding the Bible<br/>10-14 days]
    Classify -->|Purpose/Calling Keywords| PurposePath[Pathway 6:<br/>Finding Purpose & Calling<br/>14-21 days]
    Classify -->|Marriage/Relationship Keywords| RelationshipBranch{Marriage or<br/>General Relationship?}
    Classify -->|Parenting Keywords| ParentingPath[Pathway 8:<br/>Parenting with Faith<br/>14 days]
    Classify -->|Anxiety/Fear/Worry Keywords| AnxietyPath[Pathway 9:<br/>Overcoming Anxiety<br/>10-14 days]
    Classify -->|Grief/Loss Keywords| GriefPath[Pathway 10:<br/>Healing from Grief<br/>21-30 days]
    Classify -->|Financial Keywords| FinancePath[Pathway 11:<br/>Financial Stewardship<br/>14-21 days]
    Classify -->|Crisis Keywords| CrisisPath[Pathway 12:<br/>Crisis Support<br/>Variable Duration]

    %% Salvation Branch
    SalvationBranch -->|Not a Believer/Seeker| SalvationPath[Pathway 1:<br/>Discovering Jesus<br/>7-10 days]
    SalvationBranch -->|New Believer| NewBelieverPath[Pathway 2:<br/>New Believer Foundations<br/>14 days]

    %% Prayer Branch
    PrayerBranch -->|Learning to Pray| PrayerPath1[Pathway 4:<br/>Growing in Prayer<br/>7 days]
    PrayerBranch -->|Spiritual Breakthrough| PrayerPath2[Prayer Pathway:<br/>Deeper Walk with God<br/>14 days]
    PrayerBranch -->|Anxiety/Worry Related| PrayerPath3[Prayer Pathway:<br/>Finding Peace<br/>10 days]
    PrayerBranch -->|Unanswered Prayer| PrayerPath4[Prayer Pathway:<br/>Trusting God's Timing<br/>7 days]
    PrayerBranch -->|Intercessory Prayer| PrayerPath5[Prayer Pathway:<br/>Intercessory Prayer<br/>10 days]

    %% Relationship Branch
    RelationshipBranch -->|Marriage Issues| MarriagePath[Pathway 7:<br/>Marriage & Relationships<br/>14-21 days]
    RelationshipBranch -->|General Relationships| GeneralRelPath[Pathway:<br/>Healthy Relationships<br/>10 days]

    %% All Pathways Lead to Assignment
    SalvationPath --> AssignPathway[Assign Pathway to User]
    NewBelieverPath --> AssignPathway
    BaptismPath --> AssignPathway
    PrayerPath1 --> AssignPathway
    PrayerPath2 --> AssignPathway
    PrayerPath3 --> AssignPathway
    PrayerPath4 --> AssignPathway
    PrayerPath5 --> AssignPathway
    BiblePath --> AssignPathway
    PurposePath --> AssignPathway
    MarriagePath --> AssignPathway
    GeneralRelPath --> AssignPathway
    ParentingPath --> AssignPathway
    AnxietyPath --> AssignPathway
    GriefPath --> AssignPathway
    FinancePath --> AssignPathway
    CrisisPath --> AssignPathway

    %% Pathway Assignment Steps
    AssignPathway --> SendNotification[Send Pathway Recommendation<br/>to User]

    SendNotification --> ExplainPathway[Explain Pathway Details:<br/>• What it covers<br/>• Duration<br/>• Daily structure<br/>• Expected outcomes]

    ExplainPathway --> UserDecision{User Accepts<br/>Pathway?}

    UserDecision -->|Yes| EnrollUser[Enroll User in Pathway]
    UserDecision -->|No - Want Different| ShowAlternatives[Show Alternative Pathways]
    UserDecision -->|No - Not Ready| SaveRecommendation[Save Recommendation<br/>for Later]

    ShowAlternatives --> UserDecision

    EnrollUser --> SendWelcome[Send Welcome Message<br/>& Day 1 Content]

    SendWelcome --> SetReminders[Set Daily Reminders]

    SetReminders --> TrackProgress[Initialize Progress Tracking]

    TrackProgress --> Complete([Pathway Journey Begins])

    SaveRecommendation --> Complete

    %% Styling
    classDef analysisStyle fill:#4ecdc4,stroke:#087f5b,stroke-width:2px
    classDef pathwayStyle fill:#b8b8ff,stroke:#5f3dc4,stroke-width:2px
    classDef decisionStyle fill:#ffe66d,stroke:#f59f00,stroke-width:2px
    classDef actionStyle fill:#95e1d3,stroke:#087f5b,stroke-width:2px

    class AIAnalysis,Extract,Keywords,Topics,Intent,Sentiment analysisStyle
    class SalvationPath,NewBelieverPath,BaptismPath,PrayerPath1,PrayerPath2,PrayerPath3,PrayerPath4,PrayerPath5,BiblePath,PurposePath,MarriagePath,GeneralRelPath,ParentingPath,AnxietyPath,GriefPath,FinancePath,CrisisPath pathwayStyle
    class Classify,SalvationBranch,PrayerBranch,RelationshipBranch,UserDecision decisionStyle
    class AssignPathway,SendNotification,ExplainPathway,EnrollUser,SendWelcome,SetReminders,TrackProgress actionStyle
