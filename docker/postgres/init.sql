-- Executado automaticamente na primeira inicializacao do container do Postgres

CREATE TABLE IF NOT EXISTS interactions (
    id                  SERIAL PRIMARY KEY,
    session_id          TEXT,
    question            TEXT NOT NULL,
    answer              TEXT NOT NULL,
    retrieved_chunks    JSONB,
    model               TEXT,
    latency_ms          INTEGER,
    prompt_tokens       INTEGER,
    completion_tokens   INTEGER,
    total_tokens        INTEGER,
    estimated_cost_usd  NUMERIC(10, 6),
    created_at          TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS feedback (
    id              SERIAL PRIMARY KEY,
    interaction_id  INTEGER NOT NULL REFERENCES interactions(id) ON DELETE CASCADE,
    rating          SMALLINT NOT NULL CHECK (rating IN (-1, 1)),
    comment         TEXT,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS evaluation_runs (
    id            SERIAL PRIMARY KEY,
    run_name      TEXT NOT NULL,
    metric_name   TEXT NOT NULL,
    metric_value  NUMERIC NOT NULL,
    metadata      JSONB,
    created_at    TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_interactions_created_at ON interactions (created_at);
CREATE INDEX IF NOT EXISTS idx_feedback_interaction_id ON feedback (interaction_id);
