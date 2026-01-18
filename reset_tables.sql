-- Run this SQL in pgAdmin or psql to reset the database tables
-- LogosReach Pathway Recommendation System (Recommendation Only)

-- Drop tables in correct order (respecting foreign keys)
DROP TABLE IF EXISTS pathway_enrollments CASCADE;
DROP TABLE IF EXISTS pathway_recommendations CASCADE;
DROP TABLE IF EXISTS questionnaire_responses CASCADE;
DROP TABLE IF EXISTS users CASCADE;

-- Create users table with UUID
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    external_user_id VARCHAR(255) UNIQUE,
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW()
);

-- Create questionnaire_responses table
CREATE TABLE questionnaire_responses (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id),
    entry_type VARCHAR(50) NOT NULL,
    answers JSON NOT NULL,
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW()
);

-- Create pathway_recommendations table
CREATE TABLE pathway_recommendations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id),
    questionnaire_response_id UUID NOT NULL REFERENCES questionnaire_responses(id),
    recommended_pathway VARCHAR(255) NOT NULL,
    confidence FLOAT NOT NULL,
    spiritual_stage VARCHAR(100) NOT NULL,
    primary_need VARCHAR(100) NOT NULL,
    emotional_state VARCHAR(100) NOT NULL,
    reasoning TEXT NOT NULL,
    next_step_message TEXT NOT NULL,
    raw_ai_response JSON,
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW()
);

-- Create indexes for better query performance
CREATE INDEX idx_users_external_id ON users(external_user_id);
CREATE INDEX idx_questionnaire_user_id ON questionnaire_responses(user_id);
CREATE INDEX idx_recommendations_user_id ON pathway_recommendations(user_id);
