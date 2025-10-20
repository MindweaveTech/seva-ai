# Smart AI - Database Setup & Reference

Complete database initialization and management scripts for the Smart AI system.

---

## PostgreSQL Initialization Script

### Complete Schema Setup

```sql
-- =================================================================
-- Smart AI Database Initialization Script
-- PostgreSQL 15+
-- =================================================================

-- Create extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- =================================================================
-- USERS AND AUTHENTICATION
-- =================================================================

CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    phone_number VARCHAR(20),
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    date_of_birth DATE,
    gender VARCHAR(10),
    preferred_language VARCHAR(5) DEFAULT 'en',
    timezone VARCHAR(50) DEFAULT 'UTC',

    -- Health Context
    medical_conditions JSONB DEFAULT '[]'::jsonb,
    medications JSONB DEFAULT '[]'::jsonb,
    allergies TEXT[] DEFAULT ARRAY[]::TEXT[],
    emergency_contacts JSONB DEFAULT '[]'::jsonb,
    primary_physician JSONB,

    -- Preferences
    communication_style VARCHAR(50) DEFAULT 'formal',
    voice_preference VARCHAR(50) DEFAULT 'female',
    conversation_frequency VARCHAR(50),
    topics_of_interest TEXT[] DEFAULT ARRAY[]::TEXT[],

    -- Privacy & Compliance
    consents JSONB DEFAULT '{}'::jsonb,
    hipaa_acknowledged BOOLEAN DEFAULT FALSE,
    hipaa_acknowledged_at TIMESTAMP,

    -- Account Status
    account_status VARCHAR(50) DEFAULT 'active',
    last_login TIMESTAMP,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP
);

CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_deleted_at ON users(deleted_at);
CREATE INDEX idx_users_created_at ON users(created_at);
CREATE INDEX idx_users_account_status ON users(account_status);

-- =================================================================
-- DEVICES & SESSIONS
-- =================================================================

CREATE TABLE devices (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    device_identifier VARCHAR(255) UNIQUE NOT NULL,
    device_type VARCHAR(50) NOT NULL,
    app_version VARCHAR(20),
    os_version VARCHAR(20),
    last_activity TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,

    -- Offline Sync
    local_sync_version INT DEFAULT 0,
    last_sync_at TIMESTAMP,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_devices_user_id ON devices(user_id);
CREATE INDEX idx_devices_identifier ON devices(device_identifier);

-- =================================================================
-- CONVERSATIONS & MESSAGES
-- =================================================================

CREATE TABLE conversation_sessions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    device_id UUID REFERENCES devices(id),

    session_start TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    session_end TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,

    context_type VARCHAR(50),
    initiated_by VARCHAR(50) DEFAULT 'user',

    total_messages INT DEFAULT 0,
    total_duration_seconds INT DEFAULT 0,
    average_response_time_ms NUMERIC,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_conversations_user_id ON conversation_sessions(user_id);
CREATE INDEX idx_conversations_active ON conversation_sessions(is_active, user_id);
CREATE INDEX idx_conversations_date ON conversation_sessions(session_start);

-- Chat Messages
CREATE TABLE chat_messages (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    conversation_id UUID NOT NULL REFERENCES conversation_sessions(id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,

    message_type VARCHAR(50) NOT NULL,
    content TEXT NOT NULL,
    voice_transcript TEXT,

    sender_type VARCHAR(50) NOT NULL,
    message_class VARCHAR(50),
    sentiment VARCHAR(50),

    llm_model_used VARCHAR(100),
    tokens_used INT,
    response_latency_ms INT,

    health_signals JSONB,
    mentioned_symptoms TEXT[],
    mentioned_medications TEXT[],

    embedding_id VARCHAR(255),

    is_encrypted BOOLEAN DEFAULT TRUE,
    encryption_key_version INT,

    sync_status VARCHAR(50) DEFAULT 'pending',
    local_id VARCHAR(255),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_messages_conversation ON chat_messages(conversation_id);
CREATE INDEX idx_messages_user ON chat_messages(user_id);
CREATE INDEX idx_messages_timestamp ON chat_messages(created_at);
CREATE INDEX idx_messages_sentiment ON chat_messages(sentiment);
CREATE INDEX idx_messages_sync_status ON chat_messages(sync_status);

-- Full-text search index
CREATE INDEX idx_messages_content_search ON chat_messages USING GIN(to_tsvector('english', content));

-- =================================================================
-- HEALTH METRICS & MONITORING
-- =================================================================

CREATE TABLE health_metrics (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    conversation_id UUID REFERENCES conversation_sessions(id) ON DELETE SET NULL,

    -- Vital Signs
    heart_rate INT,
    blood_pressure JSONB,
    temperature NUMERIC,
    sleep_hours NUMERIC,
    steps_count INT,

    -- Self-Reported
    mood_level INT,
    pain_level INT,
    energy_level INT,
    anxiety_level INT,

    observations TEXT,
    medication_adherence BOOLEAN,
    nutrition_quality VARCHAR(50),

    -- Alerts
    requires_attention BOOLEAN DEFAULT FALSE,
    anomaly_detected BOOLEAN DEFAULT FALSE,
    alert_reason TEXT,

    recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_health_metrics_user ON health_metrics(user_id);
CREATE INDEX idx_health_metrics_date ON health_metrics(recorded_at);
CREATE INDEX idx_health_metrics_alerts ON health_metrics(requires_attention);

-- =================================================================
-- BEHAVIORAL PATTERNS & ALERTS
-- =================================================================

CREATE TABLE behavioral_patterns (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,

    pattern_type VARCHAR(100) NOT NULL,
    pattern_description TEXT,
    confidence_score NUMERIC(3,2),

    pattern_data JSONB,

    observed_start_date DATE,
    observed_end_date DATE,

    status VARCHAR(50) DEFAULT 'active',
    alert_threshold_exceeded BOOLEAN DEFAULT FALSE,
    alert_severity VARCHAR(50),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_patterns_user ON behavioral_patterns(user_id);
CREATE INDEX idx_patterns_type ON behavioral_patterns(pattern_type);
CREATE INDEX idx_patterns_alert ON behavioral_patterns(alert_threshold_exceeded);

-- =================================================================
-- ALERTS & NOTIFICATIONS
-- =================================================================

CREATE TABLE alerts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,

    alert_type VARCHAR(100) NOT NULL,
    severity VARCHAR(50) NOT NULL,
    title VARCHAR(255),
    description TEXT,

    source_table VARCHAR(100),
    source_id UUID,
    related_data JSONB,

    recipient_type VARCHAR(50),
    recipient_id UUID,

    is_acknowledged BOOLEAN DEFAULT FALSE,
    acknowledged_by UUID REFERENCES users(id),
    acknowledged_at TIMESTAMP,
    action_taken TEXT,

    escalation_level INT DEFAULT 1,
    escalation_time TIMESTAMP,
    escalated_to UUID REFERENCES users(id),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP
);

CREATE INDEX idx_alerts_user ON alerts(user_id);
CREATE INDEX idx_alerts_severity ON alerts(severity);
CREATE INDEX idx_alerts_acknowledged ON alerts(is_acknowledged);
CREATE INDEX idx_alerts_created ON alerts(created_at);

-- =================================================================
-- CAREGIVER RELATIONSHIPS
-- =================================================================

CREATE TABLE caregiver_relationships (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    elderly_user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    caregiver_user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,

    relationship_type VARCHAR(100),
    is_primary_caregiver BOOLEAN DEFAULT FALSE,

    can_view_health_data BOOLEAN DEFAULT FALSE,
    can_receive_alerts BOOLEAN DEFAULT TRUE,
    can_communicate BOOLEAN DEFAULT FALSE,
    alert_severity_threshold VARCHAR(50),

    status VARCHAR(50) DEFAULT 'pending',
    approved_at TIMESTAMP,
    approved_by UUID REFERENCES users(id),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT no_self_caregiver CHECK (elderly_user_id != caregiver_user_id)
);

CREATE INDEX idx_caregiver_elderly ON caregiver_relationships(elderly_user_id);
CREATE INDEX idx_caregiver_caregiver ON caregiver_relationships(caregiver_user_id);

-- =================================================================
-- AUDIT & COMPLIANCE
-- =================================================================

CREATE TABLE audit_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),

    action VARCHAR(255) NOT NULL,
    entity_type VARCHAR(100),
    entity_id UUID,

    actor_user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    actor_role VARCHAR(50),
    ip_address INET,
    user_agent TEXT,

    old_values JSONB,
    new_values JSONB,

    status VARCHAR(50),
    error_message TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_audit_logs_timestamp ON audit_logs(created_at);
CREATE INDEX idx_audit_logs_user ON audit_logs(actor_user_id);
CREATE INDEX idx_audit_logs_entity ON audit_logs(entity_type, entity_id);
CREATE INDEX idx_audit_logs_action ON audit_logs(action);

-- =================================================================
-- TOKEN BLACKLIST (For logout)
-- =================================================================

CREATE TABLE token_blacklist (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    token_jti VARCHAR(255) UNIQUE NOT NULL,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    revoked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP NOT NULL
);

CREATE INDEX idx_token_blacklist_expires ON token_blacklist(expires_at);

-- =================================================================
-- OFFLINE SYNC QUEUE
-- =================================================================

CREATE TABLE sync_queue (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    device_id UUID NOT NULL REFERENCES devices(id) ON DELETE CASCADE,

    operation_type VARCHAR(50) NOT NULL,
    entity_type VARCHAR(100) NOT NULL,
    entity_id UUID,

    payload JSONB NOT NULL,

    status VARCHAR(50) DEFAULT 'pending',
    retry_count INT DEFAULT 0,
    last_retry_at TIMESTAMP,

    conflict_detected BOOLEAN DEFAULT FALSE,
    conflict_resolution_strategy VARCHAR(50),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_sync_queue_user ON sync_queue(user_id);
CREATE INDEX idx_sync_queue_device ON sync_queue(device_id);
CREATE INDEX idx_sync_queue_status ON sync_queue(status);

-- =================================================================
-- FUNCTIONS
-- =================================================================

-- Auto-update timestamp
CREATE OR REPLACE FUNCTION update_timestamp()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Create triggers
CREATE TRIGGER users_update_timestamp
BEFORE UPDATE ON users FOR EACH ROW
EXECUTE FUNCTION update_timestamp();

CREATE TRIGGER conversation_sessions_update_timestamp
BEFORE UPDATE ON conversation_sessions FOR EACH ROW
EXECUTE FUNCTION update_timestamp();

CREATE TRIGGER chat_messages_update_timestamp
BEFORE UPDATE ON chat_messages FOR EACH ROW
EXECUTE FUNCTION update_timestamp();

CREATE TRIGGER devices_update_timestamp
BEFORE UPDATE ON devices FOR EACH ROW
EXECUTE FUNCTION update_timestamp();

CREATE TRIGGER sync_queue_update_timestamp
BEFORE UPDATE ON sync_queue FOR EACH ROW
EXECUTE FUNCTION update_timestamp();

-- Health anomaly detection function
CREATE OR REPLACE FUNCTION detect_health_anomaly()
RETURNS TRIGGER AS $$
DECLARE
    v_avg_mood NUMERIC;
    v_avg_pain NUMERIC;
    v_std_mood NUMERIC;
BEGIN
    -- Calculate 7-day baseline
    SELECT
        AVG(mood_level) INTO v_avg_mood,
        AVG(pain_level) INTO v_avg_pain,
        STDDEV(mood_level) INTO v_std_mood
    FROM health_metrics
    WHERE user_id = NEW.user_id
        AND recorded_at >= CURRENT_TIMESTAMP - INTERVAL '7 days'
        AND id != NEW.id;

    -- Detect anomalies (deviation > 1.5 standard deviations)
    IF v_avg_mood IS NOT NULL AND v_std_mood IS NOT NULL THEN
        IF ABS(NEW.mood_level - v_avg_mood) > (1.5 * v_std_mood) THEN
            NEW.anomaly_detected := TRUE;
            NEW.alert_reason := 'Mood deviation detected';
        END IF;
    END IF;

    -- Simple threshold checks
    IF v_avg_pain IS NOT NULL AND NEW.pain_level > (v_avg_pain * 1.5) THEN
        NEW.anomaly_detected := TRUE;
        NEW.alert_reason := 'Pain level elevated';
    END IF;

    NEW.requires_attention := NEW.anomaly_detected;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER health_metrics_anomaly_detection
BEFORE INSERT ON health_metrics
FOR EACH ROW
EXECUTE FUNCTION detect_health_anomaly();

-- Function to get user memory context
CREATE OR REPLACE FUNCTION get_user_memory_context(
    p_user_id UUID,
    p_days_back INT DEFAULT 30
)
RETURNS TABLE (
    message_id UUID,
    message_content TEXT,
    message_timestamp TIMESTAMP,
    sentiment VARCHAR,
    health_signals JSONB
) AS $$
BEGIN
    RETURN QUERY
    SELECT
        cm.id,
        cm.content,
        cm.created_at,
        cm.sentiment,
        cm.health_signals
    FROM chat_messages cm
    WHERE cm.user_id = p_user_id
        AND cm.sender_type = 'user'
        AND cm.created_at >= CURRENT_TIMESTAMP - (p_days_back || ' days')::INTERVAL
    ORDER BY cm.created_at DESC;
END;
$$ LANGUAGE plpgsql;

-- Function to create alert for anomaly
CREATE OR REPLACE FUNCTION create_health_alert()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.anomaly_detected AND NOT OLD.anomaly_detected THEN
        INSERT INTO alerts (
            user_id,
            alert_type,
            severity,
            title,
            description,
            source_table,
            source_id
        ) VALUES (
            NEW.user_id,
            'health_anomaly',
            CASE
                WHEN NEW.mood_level < 3 THEN 'critical'
                WHEN NEW.pain_level > 8 THEN 'high'
                ELSE 'warning'
            END,
            'Health metric anomaly detected',
            NEW.alert_reason,
            'health_metrics',
            NEW.id
        );
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER health_metrics_create_alert
AFTER INSERT ON health_metrics
FOR EACH ROW
EXECUTE FUNCTION create_health_alert();

-- =================================================================
-- VIEWS FOR ANALYTICS
-- =================================================================

-- User Activity Summary
CREATE OR REPLACE VIEW user_activity_summary AS
SELECT
    u.id,
    u.email,
    u.first_name,
    COUNT(DISTINCT cs.id) as total_conversations,
    COUNT(DISTINCT cm.id) as total_messages,
    MAX(cs.session_start) as last_activity,
    AVG(cm.response_latency_ms) as avg_response_time,
    COUNT(CASE WHEN cm.sentiment = 'concerning' THEN 1 END) as concerning_messages
FROM users u
LEFT JOIN conversation_sessions cs ON u.id = cs.user_id
LEFT JOIN chat_messages cm ON cs.id = cm.conversation_id
WHERE u.deleted_at IS NULL
GROUP BY u.id, u.email, u.first_name;

-- Health Metrics Trend
CREATE OR REPLACE VIEW health_metrics_trend AS
SELECT
    user_id,
    DATE(recorded_at) as metric_date,
    AVG(mood_level) as avg_mood,
    AVG(pain_level) as avg_pain,
    AVG(energy_level) as avg_energy,
    AVG(sleep_hours) as avg_sleep,
    COUNT(*) as metric_count
FROM health_metrics
GROUP BY user_id, DATE(recorded_at)
ORDER BY user_id, metric_date DESC;

-- Alert Summary
CREATE OR REPLACE VIEW alert_summary AS
SELECT
    a.user_id,
    a.severity,
    COUNT(*) as alert_count,
    COUNT(CASE WHEN a.is_acknowledged THEN 1 END) as acknowledged_count
FROM alerts a
WHERE EXTRACT(DAY FROM (NOW() - a.created_at)) <= 30
GROUP BY a.user_id, a.severity
ORDER BY a.user_id, a.severity;

-- =================================================================
-- PERMISSIONS & ROLES (RBAC)
-- =================================================================

-- Create roles
CREATE ROLE app_user WITH LOGIN PASSWORD 'secure_password';
CREATE ROLE app_admin WITH SUPERUSER;
CREATE ROLE data_analyst WITH LOGIN PASSWORD 'analyst_password';

-- Grant permissions to app_user (limited access)
GRANT USAGE ON SCHEMA public TO app_user;
GRANT SELECT, INSERT, UPDATE ON ALL TABLES IN SCHEMA public TO app_user;
GRANT USAGE ON ALL SEQUENCES IN SCHEMA public TO app_user;

-- Grant to data_analyst (read-only)
GRANT USAGE ON SCHEMA public TO data_analyst;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO data_analyst;

-- =================================================================
-- DATA RETENTION POLICIES
-- =================================================================

-- Archive old conversations (older than 3 years)
-- To be run periodically:
-- DELETE FROM chat_messages WHERE created_at < NOW() - INTERVAL '3 years' AND sender_type = 'user';
-- DELETE FROM conversation_sessions WHERE session_end < NOW() - INTERVAL '3 years';

-- Clean up old sync queue entries (older than 30 days)
-- DELETE FROM sync_queue WHERE status = 'synced' AND updated_at < NOW() - INTERVAL '30 days';

-- Clean up expired tokens
-- DELETE FROM token_blacklist WHERE expires_at < NOW();

COMMIT;

-- Verify all tables were created
SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'public'
ORDER BY table_name;
```

---

## Database Initialization in Python (Alembic)

### Alembic Configuration

```python
# backend/alembic/env.py

from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context
from logging.config import fileConfig
import os
from app.db.base import Base
from app.models.database import *

config = context.config
fileConfig(config.config_file_name)
target_metadata = Base.metadata

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = os.getenv("DATABASE_URL")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    configuration = config.get_section(config.config_ini_section)
    configuration["sqlalchemy.url"] = os.getenv("DATABASE_URL")

    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
```

### Database Seeding Script

```python
# backend/scripts/seed_data.py

import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from app.models.database import User, ConversationSession, ChatMessage, HealthMetric
from app.core.security import hash_password
import uuid
from datetime import datetime, timedelta
import os

DATABASE_URL = os.getenv("DATABASE_URL")

async def seed_database():
    """Seed database with test data"""

    engine = create_async_engine(DATABASE_URL, echo=False)
    AsyncSessionLocal = async_sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )

    async with AsyncSessionLocal() as session:
        # Create test users
        test_user = User(
            email="elderly@example.com",
            password_hash=hash_password("TestPassword123!"),
            first_name="John",
            last_name="Doe",
            date_of_birth="1950-05-15",
            timezone="America/New_York",
            medical_conditions=[
                {
                    "name": "Type 2 Diabetes",
                    "diagnosed_date": "2010-03-15",
                    "status": "managed"
                }
            ],
            medications=[
                {
                    "name": "Metformin",
                    "dosage": "500mg",
                    "frequency": "twice daily"
                }
            ],
            hipaa_acknowledged=True,
            hipaa_acknowledged_at=datetime.utcnow()
        )

        session.add(test_user)
        await session.flush()

        # Create test conversation
        conversation = ConversationSession(
            user_id=test_user.id,
            session_start=datetime.utcnow(),
            context_type="health_check"
        )
        session.add(conversation)
        await session.flush()

        # Add sample messages
        user_message = ChatMessage(
            conversation_id=conversation.id,
            user_id=test_user.id,
            message_type="text",
            content="Good morning! How are you today?",
            sender_type="user",
            sentiment="positive",
            health_signals={"mood_level": 7}
        )

        assistant_message = ChatMessage(
            conversation_id=conversation.id,
            user_id=test_user.id,
            message_type="text",
            content="Good morning John! I'm here to check in on you. How are you feeling today?",
            sender_type="assistant",
            llm_model_used="claude-3-5-sonnet-20241022",
            tokens_used=45
        )

        session.add(user_message)
        session.add(assistant_message)

        # Add health metrics
        for i in range(7):
            metric = HealthMetric(
                user_id=test_user.id,
                mood_level=7 - i,
                pain_level=2,
                energy_level=6,
                sleep_hours=7.5,
                medication_adherence=True,
                recorded_at=datetime.utcnow() - timedelta(days=i)
            )
            session.add(metric)

        await session.commit()
        print("Database seeded successfully!")

if __name__ == "__main__":
    asyncio.run(seed_database())
```

---

## Backup & Recovery Procedures

### Automated Backup Script

```bash
#!/bin/bash
# scripts/backup_database.sh

BACKUP_DIR="/backups/postgresql"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
DB_NAME="smartai"
DB_USER="smartai"
DB_HOST="localhost"

# Create backup directory
mkdir -p $BACKUP_DIR

# Perform full backup
pg_dump \
    -h $DB_HOST \
    -U $DB_USER \
    -d $DB_NAME \
    --format=custom \
    --compress=9 \
    -f "$BACKUP_DIR/smartai_backup_${TIMESTAMP}.dump"

# Perform schema backup
pg_dump \
    -h $DB_HOST \
    -U $DB_USER \
    -d $DB_NAME \
    --schema-only \
    -f "$BACKUP_DIR/smartai_schema_${TIMESTAMP}.sql"

# Keep only last 30 days of backups
find $BACKUP_DIR -type f -mtime +30 -delete

echo "Backup completed: $BACKUP_DIR/smartai_backup_${TIMESTAMP}.dump"
```

### Recovery Procedure

```bash
#!/bin/bash
# scripts/restore_database.sh

BACKUP_FILE=$1
DB_NAME="smartai"
DB_USER="smartai"
DB_HOST="localhost"

if [ -z "$BACKUP_FILE" ]; then
    echo "Usage: $0 <backup_file>"
    exit 1
fi

# Restore from backup
pg_restore \
    -h $DB_HOST \
    -U $DB_USER \
    -d $DB_NAME \
    --clean \
    --if-exists \
    "$BACKUP_FILE"

echo "Database restored from $BACKUP_FILE"
```

---

## Performance Optimization Queries

### Index Analysis

```sql
-- Find unused indexes
SELECT schemaname, tablename, indexname
FROM pg_indexes
WHERE schemaname = 'public'
    AND indexname NOT IN (
        SELECT indexrelname
        FROM pg_stat_user_indexes
    );

-- Check index size
SELECT
    schemaname,
    tablename,
    indexname,
    pg_size_pretty(pg_relation_size(indexrelid)) as index_size
FROM pg_indexes
LEFT JOIN pg_stat_user_indexes ON indexrelname = indexname
WHERE schemaname = 'public'
ORDER BY pg_relation_size(indexrelid) DESC;

-- Find slow queries
SELECT
    query,
    calls,
    mean_exec_time,
    max_exec_time,
    total_exec_time
FROM pg_stat_statements
WHERE query NOT LIKE '%pg_stat_statements%'
ORDER BY mean_exec_time DESC
LIMIT 20;
```

### Maintenance Tasks

```sql
-- Vacuum and analyze
VACUUM ANALYZE users;
VACUUM ANALYZE chat_messages;
VACUUM ANALYZE health_metrics;

-- Reindex
REINDEX TABLE chat_messages;
REINDEX TABLE health_metrics;

-- Check table size
SELECT
    schemaname,
    tablename,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS size
FROM pg_tables
WHERE schemaname = 'public'
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;
```

---

## Monitoring Queries

### Database Health

```sql
-- Active connections
SELECT datname, count(*) as connection_count
FROM pg_stat_activity
GROUP BY datname;

-- Long-running queries
SELECT
    pid,
    usename,
    query,
    state,
    query_start,
    NOW() - query_start as duration
FROM pg_stat_activity
WHERE state != 'idle'
    AND query NOT LIKE '%pg_stat%'
ORDER BY query_start;

-- Table bloat
SELECT
    schemaname,
    tablename,
    ROUND(100.0 * (pg_total_relation_size(schemaname||'.'||tablename) -
        pg_relation_size(schemaname||'.'||tablename)) /
        pg_total_relation_size(schemaname||'.'||tablename)) as index_ratio
FROM pg_tables
WHERE schemaname = 'public'
ORDER BY index_ratio DESC;

-- Cache hit ratio
SELECT
    sum(heap_blks_read) as heap_read,
    sum(heap_blks_hit) as heap_hit,
    sum(heap_blks_hit) / (sum(heap_blks_hit) + sum(heap_blks_read)) as ratio
FROM pg_statio_user_tables;
```

---

## Migration Scripts

### Adding New Features (Example: Recommendation System)

```sql
-- Add recommendations table
ALTER TABLE users ADD COLUMN recommendation_preferences JSONB DEFAULT '{}';

CREATE TABLE recommendations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    recommendation_type VARCHAR(100) NOT NULL,
    content TEXT NOT NULL,
    embedding_id VARCHAR(255),
    relevance_score NUMERIC(3,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_recommendations_user ON recommendations(user_id);
CREATE INDEX idx_recommendations_type ON recommendations(recommendation_type);

-- Add trigger for recommendations
CREATE OR REPLACE FUNCTION suggest_recommendations()
RETURNS TRIGGER AS $$
BEGIN
    -- Logic to generate recommendations based on new metrics
    INSERT INTO recommendations (user_id, recommendation_type, content)
    VALUES (NEW.user_id, 'health_tip', 'Consider increasing water intake');
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER health_metrics_suggest_recommendations
AFTER INSERT ON health_metrics
FOR EACH ROW
EXECUTE FUNCTION suggest_recommendations();
```

---

This database documentation provides everything needed for setup, maintenance, and optimization of the Smart AI system.
