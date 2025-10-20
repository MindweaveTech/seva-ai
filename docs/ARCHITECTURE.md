# Smart AI - Comprehensive Architecture Document

## Executive Summary

Smart AI is an AI-powered companion system designed specifically for elderly care with a nurse-like persona. The system combines conversational AI, memory management, health monitoring, and voice interfaces to provide empathetic, context-aware companionship while maintaining strict privacy and compliance standards.

This document defines the complete technical architecture, including system design, data models, API specifications, security measures, and implementation roadmap for production deployment.

---

## Table of Contents

1. [System Overview](#system-overview)
2. [Architecture Design](#architecture-design)
3. [Technology Stack Justification](#technology-stack-justification)
4. [Data Models & Database Design](#data-models--database-design)
5. [API Specifications](#api-specifications)
6. [Memory Systems](#memory-systems)
7. [Security & Compliance](#security--compliance)
8. [Voice Integration](#voice-integration)
9. [Offline-First Strategy](#offline-first-strategy)
10. [Implementation Roadmap](#implementation-roadmap)
11. [Deployment & Operations](#deployment--operations)

---

## 1. System Overview

### 1.1 Vision & Goals

**Primary Objectives:**
- Provide empathetic, context-aware companionship for elderly users
- Monitor behavioral patterns and detect health anomalies
- Enable voice-first interaction for accessibility
- Ensure data privacy and HIPAA compliance
- Support offline operation with seamless synchronization

**Key Personas:**
- **Primary User:** Elderly adults (65+) with varying tech comfort
- **Secondary User:** Family members/caregivers (monitoring dashboard)
- **Tertiary User:** Healthcare providers (with consent)

### 1.2 Core Capabilities

```
┌─────────────────────────────────────────────────────────┐
│                    Smart AI System                       │
├─────────────────────────────────────────────────────────┤
│  1. Conversational Interface (Text & Voice)             │
│  2. Contextual Memory Retrieval (3-Layer System)       │
│  3. Health Pattern Detection & Alerts                  │
│  4. Offline Functionality with Sync                    │
│  5. Family/Caregiver Portal                            │
│  6. Privacy-First Data Management                      │
└─────────────────────────────────────────────────────────┘
```

### 1.3 Success Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Response Time | < 2 seconds | API latency (p95) |
| Offline Time | 72 hours | Local cache capacity |
| Memory Recall | > 85% relevant | RAG relevance scoring |
| User Satisfaction | > 4.0/5.0 | App store rating |
| Uptime | 99.5% | Infrastructure monitoring |
| HIPAA Compliance | 100% | Security audits |

---

## 2. Architecture Design

### 2.1 High-Level System Architecture

```
┌────────────────────────────────────────────────────────────────┐
│                     MOBILE APPLICATION LAYER                    │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────┐ │
│  │   Voice Input    │  │  Chat Interface  │  │ Local Storage│ │
│  │  (Speech-to-Text)│  │   (UI/UX Layer)  │  │   (SQLite)   │ │
│  └────────┬─────────┘  └────────┬─────────┘  └──────┬───────┘ │
│           │                      │                    │          │
│           └──────────────────────┼────────────────────┘          │
│                                  │                              │
└──────────────────────────────────┼──────────────────────────────┘
                                   │
                    ┌──────────────▼──────────────┐
                    │     SYNC & OFFLINE ENGINE   │
                    │  - Queue Management         │
                    │  - Conflict Resolution      │
                    │  - Background Sync          │
                    └──────────────┬──────────────┘
                                   │
        ┌──────────────────────────┼──────────────────────────────┐
        │                          │                              │
┌───────▼────────────┐  ┌──────────▼──────────┐  ┌──────────────▼───┐
│   API GATEWAY      │  │  AUTHENTICATION     │  │  RATE LIMITING   │
│   (Load Balancing) │  │  SERVICE (OAuth2)   │  │  & METERING      │
└───────┬────────────┘  └──────────┬──────────┘  └──────────┬───────┘
        │                          │                        │
        └──────────────────────────┼────────────────────────┘
                                   │
        ┌──────────────────────────▼──────────────────────────────┐
        │              BACKEND API LAYER (FastAPI)                │
        │  ┌─────────────────────────────────────────────────┐   │
        │  │  Chat Service    │  Health Service  │ User Svc  │   │
        │  └─────────────────────────────────────────────────┘   │
        └──────────────────────────┬──────────────────────────────┘
                                   │
        ┌──────────────────────────┼──────────────────────────────┐
        │                          │                              │
┌───────▼─────────────┐  ┌────────▼──────────┐  ┌──────────────▼───┐
│  LLM SERVICE        │  │ MEMORY SYSTEM     │  │  PATTERN DETECT  │
│  (Claude API)       │  │  (RAG Pipeline)   │  │  (Analytics)     │
├─────────────────────┤  ├──────────────────┤  ├──────────────────┤
│ - Prompt Eng.       │  │ - Vector Store    │  │ - Health Anomaly │
│ - Response Gen.     │  │ - Semantic Search │  │ - Behavioral     │
│ - Context Mgmt.     │  │ - Embeddings      │  │   Patterns       │
└─────────────────────┘  └──────────────────┘  └──────────────────┘
                                   │
        ┌──────────────────────────┼──────────────────────────────┐
        │                          │                              │
┌───────▼─────────────┐  ┌────────▼──────────┐  ┌──────────────▼───┐
│   PostgreSQL        │  │  VECTOR DB        │  │  MESSAGE QUEUE   │
│   (Primary Data)    │  │  (Pinecone)       │  │  (Redis/RabbitMQ)│
├─────────────────────┤  ├──────────────────┤  ├──────────────────┤
│ - Users             │  │ - Embeddings      │  │ - Async Tasks    │
│ - Chat History      │  │ - Semantic Index  │  │ - Event Stream   │
│ - Health Metrics    │  │ - Recall Context  │  │ - Notifications  │
│ - Profiles          │  └──────────────────┘  └──────────────────┘
└─────────────────────┘
        │
        └─ Backup & Analytics (Data Lake / S3)
```

### 2.2 Component Responsibilities

#### Mobile Layer (React Native / Flutter)
- **Voice Interface:** Speech recognition and synthesis
- **Chat UI:** Message display with accessibility features
- **Local Storage:** SQLite for offline data persistence
- **Sync Engine:** Queue management and conflict resolution
- **Offline Detection:** Graceful degradation based on connectivity

#### API Gateway
- Request routing and load balancing
- Rate limiting per user/device
- Request/response logging for compliance
- SSL/TLS termination

#### Authentication Service
- OAuth2/OIDC implementation
- Token management and refresh
- Device registration and management
- Multi-factor authentication support

#### Backend Services
1. **Chat Service:** Message processing and storage
2. **User Service:** Profile and preference management
3. **Health Service:** Health metrics and alert management
4. **Memory Service:** RAG pipeline coordination

#### LLM Integration
- Persona-aware prompt engineering
- Context window management
- Token optimization
- Failure fallback responses

#### Memory Systems
- **Short-term:** Redis/in-memory context
- **Long-term:** Vector database embeddings
- **Profile:** PostgreSQL structured data

#### Pattern Detection
- Behavioral anomaly detection
- Health metric analysis
- Alert triggering and escalation

---

## 3. Technology Stack Justification

### 3.1 Recommended Stack

#### Frontend: React Native (with Expo for rapid development)

**Choice Rationale:**
- Single codebase for iOS/Android
- Excellent voice integration libraries
- Community support for accessibility features
- Faster iteration during MVP phase

**Key Libraries:**
```
- react-native-voice (speech recognition)
- react-native-tts (text-to-speech)
- @react-native-async-storage (local persistence)
- WatermelonDB (local database - better than SQLite for sync)
- React Native Paper (accessibility-focused UI)
- Redux/Zustand (state management)
- Axios + Axios Offline (API + offline handling)
```

**Alternatives Evaluated:**
| Option | Pros | Cons | Recommendation |
|--------|------|------|-----------------|
| **Flutter** | Native performance, excellent voice support | Smaller ecosystem, Dart learning curve | If native performance critical |
| **Native (Swift/Kotlin)** | Maximum performance | Double development effort | Not recommended for MVP |

---

#### Backend: FastAPI (Python)

**Choice Rationale:**
- Native async support for concurrent connections
- Excellent documentation and rapid development
- Strong ML/AI ecosystem integration
- Pydantic for data validation
- Built-in OpenAPI documentation

**Key Libraries:**
```
- FastAPI (web framework)
- SQLAlchemy (ORM)
- Pydantic (data validation)
- python-jose (JWT tokens)
- anthropic (Claude API client)
- langchain (LLM orchestration)
- redis-py (caching and sessions)
- APScheduler (job scheduling for health checks)
```

**Alternatives Evaluated:**
| Option | Pros | Cons | Recommendation |
|--------|------|------|-----------------|
| **Node.js** | JavaScript everywhere, good ecosystem | Less suitable for ML integration | Consider if team expertise favors JS |
| **Django** | Batteries-included, ORM maturity | Heavier, slower for this use case | Not recommended |

---

#### Primary Database: PostgreSQL 15+

**Choice Rationale:**
- ACID compliance for health data integrity
- JSON support for flexible schema evolution
- Full-text search capabilities
- Native UUID support
- Proven reliability for healthcare data

**Key Extensions:**
```sql
- uuid-ossp (UUID generation)
- pg_trgm (trigram full-text search)
- pgcrypto (encryption functions)
```

---

#### Vector Database: Weaviate (on-premise) OR Pinecone (managed)

**Architecture Decision:**

For MVP, recommend **Weaviate** (self-hosted) + fallback to **Pinecone (managed)**

**Weaviate Benefits:**
- Open-source, avoids vendor lock-in
- Can be deployed on infrastructure
- HIPAA-compliant when self-hosted
- GraphQL + REST APIs
- Built-in keyword search + semantic search

**Pinecone Benefits (if scaling):**
- Fully managed (reduce operational overhead)
- Enterprise SLA
- Automatic scaling
- Hybrid search (keyword + semantic)

**Configuration for Health AI:**

```yaml
# Weaviate schema for health context
Class: HealthContext
  Properties:
    - content (text)
    - timestamp (date)
    - user_id (uuid reference)
    - conversation_id (uuid reference)
    - sentiment (string)
    - health_topics (array)
    - relevance_score (number)
  Vectorizer: text2vec-transformers
  Module: qna-transformers
```

---

#### LLM: Claude API (Anthropic)

**Choice Rationale:**
- Superior understanding of nuance and context
- Excellent for empathetic, long-form responses
- Strong instruction-following for persona engineering
- Extended token window (200K) for memory
- Comprehensive safety guidelines for healthcare

**API Integration:**
```python
- Use Anthropic SDK with streaming for real-time responses
- Implement token counting for cost optimization
- Use system prompts for persona engineering
```

---

#### Message Queue: Redis (development) -> RabbitMQ (production)

**Purpose:**
- Asynchronous task processing
- Event streaming for pattern detection
- Session cache
- Rate limiting

**Use Cases:**
1. Health alert processing (async)
2. Embedding generation (background task)
3. Offline sync event queue
4. Notification delivery

---

#### Caching Layer: Redis

**Caching Strategy:**
```
Cache Layer Architecture:
┌─────────────────────────────────┐
│     API Request                 │
└────────────┬────────────────────┘
             │
    ┌────────▼────────┐
    │  Redis Cache?   │──YES──┐
    └────────┬────────┘       │
             │ NO             │
             │           ┌────▼──────┐
             │           │Return Data│
             │           └───────────┘
             │
    ┌────────▼────────────────────┐
    │ PostgreSQL / Vector DB      │
    └────────┬────────────────────┘
             │
    ┌────────▼────────────────────┐
    │  Store in Redis (TTL-based) │
    └────────┬────────────────────┘
             │
    ┌────────▼──────────────────────┐
    │  Return Data to Client        │
    └───────────────────────────────┘

Cache Keys Strategy:
- user:{user_id}:profile (TTL: 1 hour)
- user:{user_id}:recent_messages:5 (TTL: 5 mins)
- conversation:{conv_id}:context (TTL: 30 mins)
- health_alerts:{user_id} (TTL: 15 mins)
```

---

### 3.2 Infrastructure & Deployment

#### Development/MVP Environment
```
- Docker containers for all services
- Docker Compose for local orchestration
- Localhost database (PostgreSQL + Weaviate)
- Local Redis for caching
```

#### Production Environment
```
- Kubernetes cluster (EKS/GKE/AKS)
- Managed PostgreSQL (AWS RDS, Google Cloud SQL, Azure Database)
- Pinecone or Weaviate cluster (managed service or K8s)
- Redis cluster (AWS ElastiCache, Google Memorystore)
- CDN for static assets
- WAF for API protection
```

---

## 4. Data Models & Database Design

### 4.1 PostgreSQL Schema

#### Core Tables

```sql
-- Users Table
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(255) UNIQUE NOT NULL,
    phone_number VARCHAR(20),
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    date_of_birth DATE,
    gender VARCHAR(10),
    preferred_language VARCHAR(5) DEFAULT 'en',
    timezone VARCHAR(50) DEFAULT 'UTC',

    -- Health Context
    medical_conditions JSONB,  -- [{name, diagnosed_date, status}]
    medications JSONB,          -- [{name, dosage, frequency, side_effects}]
    allergies TEXT[],
    emergency_contacts JSONB,   -- [{name, relationship, phone, email}]
    primary_physician JSONB,    -- {name, phone, email, practice}

    -- Preferences
    communication_style VARCHAR(50) DEFAULT 'formal',  -- formal/casual
    voice_preference VARCHAR(50) DEFAULT 'female',
    conversation_frequency VARCHAR(50),  -- daily/weekly
    topics_of_interest TEXT[],

    -- Privacy & Compliance
    consents JSONB,  -- {data_sharing, emergency_alerts, analytics}
    hipaa_acknowledged BOOLEAN DEFAULT false,
    acknowledged_at TIMESTAMP,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP  -- Soft delete for compliance
);

CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_deleted_at ON users(deleted_at);

-- Device Registration Table
CREATE TABLE devices (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    device_identifier VARCHAR(255) UNIQUE NOT NULL,  -- Firebase Device Token or custom
    device_type VARCHAR(50) NOT NULL,  -- iOS, Android
    app_version VARCHAR(20),
    os_version VARCHAR(20),
    last_activity TIMESTAMP,
    is_active BOOLEAN DEFAULT true,

    -- Offline Support
    local_sync_version INT DEFAULT 0,
    last_sync_at TIMESTAMP,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_devices_user_id ON devices(user_id);
CREATE INDEX idx_devices_identifier ON devices(device_identifier);

-- Conversation Sessions Table
CREATE TABLE conversation_sessions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    device_id UUID REFERENCES devices(id),

    -- Session Context
    session_start TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    session_end TIMESTAMP,
    is_active BOOLEAN DEFAULT true,

    -- Session Metadata
    context_type VARCHAR(50),  -- health_check, casual, emergency
    initiated_by VARCHAR(50) DEFAULT 'user',  -- user, system

    -- Performance Metrics
    total_messages INT DEFAULT 0,
    total_duration_seconds INT DEFAULT 0,
    average_response_time_ms NUMERIC,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_conversations_user_id ON conversation_sessions(user_id);
CREATE INDEX idx_conversations_active ON conversation_sessions(is_active, user_id);
CREATE INDEX idx_conversations_date ON conversation_sessions(session_start);

-- Chat Messages Table
CREATE TABLE chat_messages (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    conversation_id UUID NOT NULL REFERENCES conversation_sessions(id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,

    -- Message Content
    message_type VARCHAR(50) NOT NULL,  -- text, voice, image
    content TEXT NOT NULL,
    voice_transcript TEXT,  -- If voice input

    -- Message Classification
    sender_type VARCHAR(50) NOT NULL,  -- user, assistant
    message_class VARCHAR(50),  -- health_related, emotional, casual
    sentiment VARCHAR(50),  -- positive, neutral, negative, concerning

    -- LLM Integration
    llm_model_used VARCHAR(100),  -- claude-3-sonnet-20240229
    tokens_used INT,
    response_latency_ms INT,

    -- Health Signals
    health_signals JSONB,  -- {sleep_quality, mood, pain_level, symptoms}
    mentioned_symptoms TEXT[],
    mentioned_medications TEXT[],

    -- Embeddings Reference (Foreign Key to Vector DB)
    embedding_id VARCHAR(255),  -- Reference to Weaviate object ID

    -- Compliance & Privacy
    is_encrypted BOOLEAN DEFAULT true,
    encryption_key_version INT,

    -- Offline Sync
    sync_status VARCHAR(50) DEFAULT 'pending',  -- pending, synced, failed
    local_id VARCHAR(255),  -- For offline-first tracking

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_messages_conversation ON chat_messages(conversation_id);
CREATE INDEX idx_messages_user ON chat_messages(user_id);
CREATE INDEX idx_messages_timestamp ON chat_messages(created_at);
CREATE INDEX idx_messages_sentiment ON chat_messages(sentiment);
CREATE INDEX idx_messages_sync_status ON chat_messages(sync_status);

-- Health Metrics Table
CREATE TABLE health_metrics (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    conversation_id UUID REFERENCES conversation_sessions(id) ON DELETE SET NULL,

    -- Vital Signs (if integrated with wearables)
    heart_rate INT,
    blood_pressure JSONB,  -- {systolic, diastolic}
    temperature NUMERIC,
    sleep_hours NUMERIC,
    steps_count INT,

    -- Self-Reported Metrics
    mood_level INT,  -- 1-10 scale
    pain_level INT,  -- 1-10 scale
    energy_level INT,  -- 1-10 scale
    anxiety_level INT,  -- 1-10 scale

    -- Observations
    observations TEXT,
    medication_adherence BOOLEAN,
    nutrition_quality VARCHAR(50),  -- poor, fair, good, excellent

    -- Alert Flags
    requires_attention BOOLEAN DEFAULT false,
    anomaly_detected BOOLEAN DEFAULT false,
    alert_reason TEXT,

    recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_health_metrics_user ON health_metrics(user_id);
CREATE INDEX idx_health_metrics_date ON health_metrics(recorded_at);
CREATE INDEX idx_health_metrics_alerts ON health_metrics(requires_attention);

-- Behavioral Patterns Table
CREATE TABLE behavioral_patterns (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,

    -- Pattern Classification
    pattern_type VARCHAR(100) NOT NULL,  -- sleep_schedule, communication_frequency, mood_trend
    pattern_description TEXT,
    confidence_score NUMERIC(3,2),  -- 0.00 to 1.00

    -- Pattern Data
    pattern_data JSONB,  -- Dynamic based on pattern type

    -- Time Window
    observed_start_date DATE,
    observed_end_date DATE,

    -- Status
    status VARCHAR(50) DEFAULT 'active',  -- active, resolved, investigating

    -- Alerts
    alert_threshold_exceeded BOOLEAN DEFAULT false,
    alert_severity VARCHAR(50),  -- low, medium, high, critical

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_patterns_user ON behavioral_patterns(user_id);
CREATE INDEX idx_patterns_type ON behavioral_patterns(pattern_type);
CREATE INDEX idx_patterns_alert ON behavioral_patterns(alert_threshold_exceeded);

-- Alerts & Notifications Table
CREATE TABLE alerts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,

    -- Alert Details
    alert_type VARCHAR(100) NOT NULL,  -- health_anomaly, behavioral_change, emergency
    severity VARCHAR(50) NOT NULL,  -- info, warning, critical
    title VARCHAR(255),
    description TEXT,

    -- Source & Context
    source_table VARCHAR(100),  -- health_metrics, behavioral_patterns, chat_messages
    source_id UUID,
    related_data JSONB,

    -- Recipient & Status
    recipient_type VARCHAR(50),  -- user, caregiver, healthcare_provider
    recipient_id UUID,

    -- Action Tracking
    is_acknowledged BOOLEAN DEFAULT false,
    acknowledged_by UUID,
    acknowledged_at TIMESTAMP,
    action_taken TEXT,

    -- Escalation
    escalation_level INT DEFAULT 1,
    escalation_time TIMESTAMP,
    escalated_to UUID,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP  -- For time-sensitive alerts
);

CREATE INDEX idx_alerts_user ON alerts(user_id);
CREATE INDEX idx_alerts_severity ON alerts(severity);
CREATE INDEX idx_alerts_acknowledged ON alerts(is_acknowledged);
CREATE INDEX idx_alerts_created ON alerts(created_at);

-- Caregiver Relationships Table
CREATE TABLE caregiver_relationships (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    elderly_user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    caregiver_user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,

    -- Relationship Details
    relationship_type VARCHAR(100),  -- family, professional_caregiver, healthcare_provider
    is_primary_caregiver BOOLEAN DEFAULT false,

    -- Permissions
    can_view_health_data BOOLEAN DEFAULT false,
    can_receive_alerts BOOLEAN DEFAULT true,
    can_communicate BOOLEAN DEFAULT false,
    alert_severity_threshold VARCHAR(50),  -- all, warning, critical

    -- Approval Status
    status VARCHAR(50) DEFAULT 'pending',  -- pending, approved, rejected, revoked
    approved_at TIMESTAMP,
    approved_by UUID,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_caregiver_elderly ON caregiver_relationships(elderly_user_id);
CREATE INDEX idx_caregiver_caregiver ON caregiver_relationships(caregiver_user_id);

-- Audit Log Table (Compliance & HIPAA)
CREATE TABLE audit_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),

    -- Action Details
    action VARCHAR(255) NOT NULL,
    entity_type VARCHAR(100),
    entity_id UUID,

    -- User & Context
    actor_user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    actor_role VARCHAR(50),
    ip_address INET,
    user_agent TEXT,

    -- Changes
    old_values JSONB,
    new_values JSONB,

    -- Status & Result
    status VARCHAR(50),  -- success, failure
    error_message TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_audit_logs_timestamp ON audit_logs(created_at);
CREATE INDEX idx_audit_logs_user ON audit_logs(actor_user_id);
CREATE INDEX idx_audit_logs_entity ON audit_logs(entity_type, entity_id);

-- Session Token Blacklist (for logout / token revocation)
CREATE TABLE token_blacklist (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    token_jti VARCHAR(255) UNIQUE NOT NULL,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    revoked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP NOT NULL
);

CREATE INDEX idx_token_blacklist_expires ON token_blacklist(expires_at);

-- Offline Sync Queue Table
CREATE TABLE sync_queue (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    device_id UUID NOT NULL REFERENCES devices(id) ON DELETE CASCADE,

    -- Queue Details
    operation_type VARCHAR(50) NOT NULL,  -- create, update, delete
    entity_type VARCHAR(100) NOT NULL,  -- chat_message, health_metric
    entity_id UUID,

    -- Payload
    payload JSONB NOT NULL,

    -- Status
    status VARCHAR(50) DEFAULT 'pending',  -- pending, synced, failed
    retry_count INT DEFAULT 0,
    last_retry_at TIMESTAMP,

    -- Conflict Resolution
    conflict_detected BOOLEAN DEFAULT false,
    conflict_resolution_strategy VARCHAR(50),  -- last_write_wins, user_resolution

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_sync_queue_user ON sync_queue(user_id);
CREATE INDEX idx_sync_queue_device ON sync_queue(device_id);
CREATE INDEX idx_sync_queue_status ON sync_queue(status);
```

#### Creating Functions and Triggers

```sql
-- Auto-update timestamp trigger
CREATE OR REPLACE FUNCTION update_timestamp()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER users_update_timestamp
BEFORE UPDATE ON users
FOR EACH ROW
EXECUTE FUNCTION update_timestamp();

CREATE TRIGGER conversation_sessions_update_timestamp
BEFORE UPDATE ON conversation_sessions
FOR EACH ROW
EXECUTE FUNCTION update_timestamp();

CREATE TRIGGER chat_messages_update_timestamp
BEFORE UPDATE ON chat_messages
FOR EACH ROW
EXECUTE FUNCTION update_timestamp();

-- Function to retrieve user memory context
CREATE OR REPLACE FUNCTION get_user_memory_context(
    p_user_id UUID,
    p_days_back INT DEFAULT 30
)
RETURNS TABLE (
    message_content TEXT,
    message_timestamp TIMESTAMP,
    sentiment VARCHAR,
    health_signals JSONB
) AS $$
BEGIN
    RETURN QUERY
    SELECT
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

-- Function to detect health anomalies
CREATE OR REPLACE FUNCTION detect_health_anomaly()
RETURNS TRIGGER AS $$
DECLARE
    v_avg_mood NUMERIC;
    v_avg_pain NUMERIC;
    v_anomaly_detected BOOLEAN := false;
BEGIN
    -- Calculate 7-day averages
    SELECT
        AVG(mood_level) INTO v_avg_mood
    FROM health_metrics
    WHERE user_id = NEW.user_id
        AND recorded_at >= CURRENT_TIMESTAMP - INTERVAL '7 days';

    SELECT
        AVG(pain_level) INTO v_avg_pain
    FROM health_metrics
    WHERE user_id = NEW.user_id
        AND recorded_at >= CURRENT_TIMESTAMP - INTERVAL '7 days';

    -- Detect anomalies (20% deviation)
    IF (NEW.mood_level < v_avg_mood * 0.8) OR
       (NEW.pain_level > v_avg_pain * 1.2) THEN
        v_anomaly_detected := true;
    END IF;

    NEW.anomaly_detected := v_anomaly_detected;
    NEW.requires_attention := v_anomaly_detected;

    IF v_anomaly_detected THEN
        NEW.alert_reason := 'Health metric deviation detected';
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER health_metrics_anomaly_detection
BEFORE INSERT ON health_metrics
FOR EACH ROW
EXECUTE FUNCTION detect_health_anomaly();
```

### 4.2 Vector Database Schema (Weaviate)

```yaml
# Weaviate Class Configuration for RAG

Class: UserHealthContext
  Description: "Semantic storage of health-related conversation context"
  Vectorizer: "text2vec-transformers"  # Uses SBERT model

  Properties:
    - name: "content"
      description: "Raw conversation content"
      dataType: ["text"]

    - name: "summary"
      description: "Summarized content for faster recall"
      dataType: ["text"]

    - name: "user_id"
      description: "Reference to user"
      dataType: ["uuid"]

    - name: "conversation_id"
      description: "Reference to conversation"
      dataType: ["uuid"]

    - name: "timestamp"
      description: "When this context was created"
      dataType: ["date"]

    - name: "health_topics"
      description: "Extracted health topics"
      dataType: ["string[]"]
      examples: ["diabetes", "medication_adherence", "sleep_quality"]

    - name: "sentiment"
      description: "Sentiment of the conversation"
      dataType: ["string"]
      enumeration: ["positive", "neutral", "negative", "concerning"]

    - name: "key_facts"
      description: "Extracted key health facts"
      dataType: ["string[]"]

    - name: "action_items"
      description: "Any action items from conversation"
      dataType: ["string[]"]

    - name: "relevance_score"
      description: "Relevance score for ranking"
      dataType: ["number"]

  References:
    - name: "from_message"
      target: "ChatMessage"
      description: "Reference to source message"

---

Class: ConversationEmbedding
  Description: "Stores full conversation embeddings for semantic search"
  Vectorizer: "text2vec-transformers"

  Properties:
    - name: "full_conversation"
      description: "Complete conversation text"
      dataType: ["text"]

    - name: "user_id"
      description: "User reference"
      dataType: ["uuid"]

    - name: "conversation_id"
      description: "Conversation reference"
      dataType: ["uuid"]

    - name: "date"
      description: "Conversation date"
      dataType: ["date"]

    - name: "conversation_type"
      description: "Type of conversation"
      dataType: ["string"]
      enumeration: ["health_check", "casual", "emergency", "medication_reminder"]

    - name: "topics"
      description: "Main topics discussed"
      dataType: ["string[]"]

    - name: "duration_minutes"
      description: "Conversation duration"
      dataType: ["int"]

    - name: "overall_sentiment"
      description: "Overall sentiment"
      dataType: ["string"]

---

# Hybrid Search Configuration
HybridSearch:
  - keyword: true       # BM25 keyword search
  - semantic: true      # Vector similarity search
  - weight: 0.5         # 50/50 blend
```

### 4.3 Local SQLite Schema (Mobile Offline Storage)

```sql
-- Mobile Local Database (WatermelonDB or similar)
-- Simplified schema for offline sync

CREATE TABLE local_chat_messages (
    local_id TEXT PRIMARY KEY,
    server_id TEXT UNIQUE,
    conversation_id TEXT NOT NULL,
    user_id TEXT NOT NULL,

    content TEXT NOT NULL,
    message_type TEXT,
    sender_type TEXT,

    sync_status TEXT DEFAULT 'pending',  -- pending, synced, failed
    is_locally_modified BOOLEAN DEFAULT false,

    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    server_timestamp TIMESTAMP,

    _status TEXT DEFAULT 'created'  -- WatermelonDB sync status
);

CREATE TABLE local_health_metrics (
    local_id TEXT PRIMARY KEY,
    server_id TEXT UNIQUE,
    user_id TEXT NOT NULL,

    mood_level INTEGER,
    pain_level INTEGER,
    energy_level INTEGER,

    sync_status TEXT DEFAULT 'pending',
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    _status TEXT DEFAULT 'created'
);

CREATE TABLE sync_metadata (
    device_id TEXT PRIMARY KEY,
    last_sync_timestamp TIMESTAMP,
    last_sync_version INT,
    is_syncing BOOLEAN DEFAULT false
);
```

---

## 5. API Specifications

### 5.1 RESTful API Endpoints

#### Authentication Endpoints

```
POST /api/v1/auth/register
Purpose: User registration
Request:
{
  "email": "john.doe@example.com",
  "password": "secure_password",
  "first_name": "John",
  "last_name": "Doe",
  "date_of_birth": "1950-05-15",
  "phone_number": "+1-555-0123",
  "timezone": "America/New_York",
  "emergency_contact": {
    "name": "Jane Doe",
    "relationship": "daughter",
    "phone": "+1-555-0456"
  }
}

Response (201):
{
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "email": "john.doe@example.com",
  "verification_required": true,
  "next_steps": ["verify_email", "health_profile_setup"]
}

Error Cases:
- 400: Validation error
- 409: Email already exists
- 500: Server error
```

```
POST /api/v1/auth/login
Purpose: User login with MFA
Request:
{
  "email": "john.doe@example.com",
  "password": "secure_password",
  "device_identifier": "android_device_123"
}

Response (200):
{
  "access_token": "eyJhbGc...",
  "refresh_token": "eyJhbGc...",
  "expires_in": 3600,
  "mfa_required": false,
  "user": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "email": "john.doe@example.com",
    "first_name": "John"
  }
}

MFA Response (200):
{
  "mfa_required": true,
  "mfa_session_token": "temporary_token",
  "mfa_methods": ["sms", "email"]
}
```

```
POST /api/v1/auth/mfa/verify
Purpose: Verify MFA code
Request:
{
  "mfa_session_token": "temporary_token",
  "mfa_code": "123456",
  "mfa_method": "sms"
}

Response (200):
{
  "access_token": "eyJhbGc...",
  "refresh_token": "eyJhbGc...",
  "expires_in": 3600
}
```

```
POST /api/v1/auth/refresh
Purpose: Refresh access token
Request:
{
  "refresh_token": "eyJhbGc..."
}

Response (200):
{
  "access_token": "eyJhbGc...",
  "expires_in": 3600
}

Error Cases:
- 401: Invalid refresh token
- 410: Refresh token expired
```

```
POST /api/v1/auth/logout
Purpose: Logout and invalidate tokens
Headers:
  Authorization: Bearer <access_token>

Response (204): No content

Post-Logout:
- Add JTI to token blacklist
- Invalidate device session
```

---

#### Chat Endpoints

```
POST /api/v1/conversations
Purpose: Start new conversation
Headers:
  Authorization: Bearer <access_token>

Request:
{
  "device_id": "device_123",
  "context_type": "health_check",  // Optional: health_check, casual, emergency
  "initial_message": "How am I feeling today?"
}

Response (201):
{
  "conversation_id": "conv_123",
  "session_start": "2024-01-15T10:00:00Z",
  "message": {
    "id": "msg_456",
    "content": "Hello! I'm here to check in on you today. How are you feeling?",
    "sender": "assistant",
    "timestamp": "2024-01-15T10:00:05Z"
  }
}
```

```
POST /api/v1/conversations/{conversation_id}/messages
Purpose: Send message in conversation
Headers:
  Authorization: Bearer <access_token>

Request:
{
  "content": "I'm feeling a bit tired today",
  "message_type": "text",  // text, voice_transcript
  "voice_data": null,  // Optional: Base64 encoded audio
  "health_signals": {
    "mood_level": 6,
    "energy_level": 5,
    "pain_level": 2
  }
}

Response (201):
{
  "user_message": {
    "id": "msg_789",
    "content": "I'm feeling a bit tired today",
    "sender": "user",
    "timestamp": "2024-01-15T10:05:00Z"
  },
  "assistant_message": {
    "id": "msg_790",
    "content": "I understand. Low energy can happen to anyone. Have you been sleeping well recently?",
    "sender": "assistant",
    "timestamp": "2024-01-15T10:05:02Z",
    "voice_url": "https://audio.smartai.com/msg_790.mp3"
  },
  "health_signals_recorded": true
}

Streaming Response (Optional):
- Use Server-Sent Events (SSE) for real-time response streaming
- Enables text-to-speech to start playing before full response
```

```
GET /api/v1/conversations/{conversation_id}/messages
Purpose: Retrieve conversation history with pagination
Headers:
  Authorization: Bearer <access_token>

Query Parameters:
  ?limit=50
  &offset=0
  &start_date=2024-01-01
  &end_date=2024-01-31

Response (200):
{
  "conversation_id": "conv_123",
  "total_messages": 250,
  "messages": [
    {
      "id": "msg_001",
      "content": "Good morning",
      "sender": "user",
      "timestamp": "2024-01-15T08:00:00Z",
      "sentiment": "neutral",
      "health_signals": {...}
    },
    ...
  ],
  "pagination": {
    "limit": 50,
    "offset": 0,
    "total": 250,
    "has_next": true
  }
}
```

```
POST /api/v1/conversations/{conversation_id}/end
Purpose: End conversation
Headers:
  Authorization: Bearer <access_token>

Request:
{
  "end_reason": "user_initiated"  // user_initiated, timeout, error
}

Response (200):
{
  "conversation_id": "conv_123",
  "session_end": "2024-01-15T10:30:00Z",
  "total_messages": 8,
  "total_duration_seconds": 1800,
  "summary": {
    "topics_discussed": ["sleep", "medication"],
    "mood_trend": "improving",
    "health_concerns": [],
    "next_recommended_check_in": "2024-01-16"
  }
}
```

---

#### Health Metrics Endpoints

```
POST /api/v1/health/metrics
Purpose: Record health metrics
Headers:
  Authorization: Bearer <access_token>

Request:
{
  "conversation_id": "conv_123",  // Optional
  "mood_level": 7,  // 1-10
  "pain_level": 2,
  "energy_level": 6,
  "anxiety_level": 3,
  "sleep_hours": 7.5,
  "medication_adherence": true,
  "nutrition_quality": "good",
  "observations": "Feeling better today"
}

Response (201):
{
  "metric_id": "metric_123",
  "recorded_at": "2024-01-15T10:00:00Z",
  "anomalies_detected": false,
  "alerts": []
}

Anomaly Response (201):
{
  "metric_id": "metric_123",
  "recorded_at": "2024-01-15T10:00:00Z",
  "anomalies_detected": true,
  "alerts": [
    {
      "id": "alert_123",
      "type": "mood_decline",
      "severity": "warning",
      "message": "Your mood has declined 35% from your 7-day average",
      "recommended_action": "Consider reaching out to your family"
    }
  ]
}
```

```
GET /api/v1/health/metrics
Purpose: Get health metrics history
Headers:
  Authorization: Bearer <access_token>

Query Parameters:
  ?days=30
  &metric_types=mood,pain,energy

Response (200):
{
  "metrics": [
    {
      "date": "2024-01-15",
      "mood_level": 7,
      "pain_level": 2,
      "energy_level": 6,
      "anxiety_level": 3,
      "anomalies": []
    },
    ...
  ],
  "trends": {
    "mood_trend": "stable",
    "pain_trend": "improving",
    "energy_trend": "declining",
    "sleep_trend": "declining"
  },
  "summary": {
    "average_mood": 6.5,
    "average_pain": 3.2,
    "average_energy": 6.8,
    "concerning_patterns": ["declining_energy"]
  }
}
```

---

#### Memory/Context Endpoints

```
GET /api/v1/memory/context
Purpose: Get relevant context for conversation
Headers:
  Authorization: Bearer <access_token>

Query Parameters:
  ?query=medications
  &context_days=30
  &limit=10

Response (200):
{
  "query": "medications",
  "context_items": [
    {
      "id": "ctx_001",
      "source_type": "health_metric",
      "content": "You mentioned taking Metformin every morning",
      "timestamp": "2024-01-14T10:00:00Z",
      "relevance_score": 0.95,
      "health_topics": ["diabetes", "medication_adherence"]
    },
    {
      "id": "ctx_002",
      "source_type": "chat_message",
      "content": "I forgot to take my blood pressure medication yesterday",
      "timestamp": "2024-01-12T15:30:00Z",
      "relevance_score": 0.87,
      "health_topics": ["hypertension", "medication_adherence"]
    }
  ],
  "summary": "Recent mentions: Metformin (diabetes), blood pressure medication"
}
```

```
POST /api/v1/memory/embeddings/refresh
Purpose: Trigger embedding refresh (async)
Headers:
  Authorization: Bearer <access_token>

Request:
{
  "time_period": "last_7_days",  // last_7_days, last_30_days, all
  "force_refresh": false
}

Response (202): Accepted
{
  "job_id": "job_123",
  "status": "processing",
  "estimated_completion": "2024-01-15T11:00:00Z"
}
```

---

#### User Profile Endpoints

```
GET /api/v1/users/profile
Purpose: Get user profile
Headers:
  Authorization: Bearer <access_token>

Response (200):
{
  "id": "user_123",
  "email": "john.doe@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "date_of_birth": "1950-05-15",
  "timezone": "America/New_York",
  "preferred_language": "en",

  "health_context": {
    "medical_conditions": [
      {
        "name": "Type 2 Diabetes",
        "diagnosed_date": "2010-03-15",
        "status": "managed"
      }
    ],
    "medications": [
      {
        "name": "Metformin",
        "dosage": "500mg",
        "frequency": "twice daily",
        "side_effects": ["nausea"]
      }
    ],
    "allergies": ["Penicillin"]
  },

  "preferences": {
    "communication_style": "formal",
    "voice_preference": "female",
    "conversation_frequency": "daily"
  },

  "emergency_contacts": [
    {
      "name": "Jane Doe",
      "relationship": "daughter",
      "phone": "+1-555-0456",
      "email": "jane@example.com"
    }
  ],

  "privacy_settings": {
    "data_sharing_enabled": true,
    "emergency_alerts_enabled": true,
    "analytics_enabled": false
  }
}
```

```
PUT /api/v1/users/profile
Purpose: Update user profile
Headers:
  Authorization: Bearer <access_token>

Request:
{
  "first_name": "John",
  "preferred_language": "es",
  "health_context": {
    "medications": [
      {
        "name": "Metformin",
        "dosage": "1000mg",
        "frequency": "daily",
        "side_effects": []
      }
    ]
  }
}

Response (200):
{
  "id": "user_123",
  "updated_fields": ["preferred_language", "health_context.medications"],
  "updated_at": "2024-01-15T10:00:00Z"
}
```

---

#### Alerts & Notifications Endpoints

```
GET /api/v1/alerts
Purpose: Get user alerts
Headers:
  Authorization: Bearer <access_token>

Query Parameters:
  ?severity=warning,critical
  &unacknowledged_only=true
  &limit=50

Response (200):
{
  "alerts": [
    {
      "id": "alert_123",
      "type": "health_anomaly",
      "severity": "warning",
      "title": "Unusual mood decline",
      "description": "Your mood has declined 40% from your 7-day average",
      "source": "health_metrics",
      "created_at": "2024-01-15T09:30:00Z",
      "is_acknowledged": false,
      "recommended_action": "Consider speaking with someone",
      "can_dismiss": true,
      "requires_human_review": false
    }
  ],
  "summary": {
    "total_alerts": 1,
    "critical_count": 0,
    "warning_count": 1,
    "info_count": 3
  }
}
```

```
PUT /api/v1/alerts/{alert_id}/acknowledge
Purpose: Acknowledge alert
Headers:
  Authorization: Bearer <access_token>

Request:
{
  "action_taken": "Called my daughter about my mood",
  "resolved": false  // true if problem is resolved
}

Response (200):
{
  "alert_id": "alert_123",
  "acknowledged_at": "2024-01-15T10:00:00Z",
  "acknowledged_by": "user_123"
}
```

---

#### Caregiver Endpoints

```
POST /api/v1/caregivers/invite
Purpose: Invite caregiver
Headers:
  Authorization: Bearer <access_token>

Request:
{
  "caregiver_email": "jane@example.com",
  "relationship_type": "family",
  "permissions": {
    "can_view_health_data": true,
    "can_receive_alerts": true,
    "alert_severity_threshold": "warning"
  }
}

Response (201):
{
  "invitation_id": "inv_123",
  "caregiver_email": "jane@example.com",
  "status": "pending",
  "expires_at": "2024-01-22T10:00:00Z",
  "invitation_link": "https://smartai.com/join/inv_123"
}
```

```
GET /api/v1/caregivers
Purpose: Get user's caregivers
Headers:
  Authorization: Bearer <access_token>

Response (200):
{
  "caregivers": [
    {
      "id": "caregiver_rel_123",
      "user": {
        "id": "user_456",
        "first_name": "Jane",
        "last_name": "Doe",
        "email": "jane@example.com"
      },
      "relationship_type": "daughter",
      "permissions": {
        "can_view_health_data": true,
        "can_receive_alerts": true,
        "alert_severity_threshold": "warning"
      },
      "status": "approved",
      "approved_at": "2024-01-10T10:00:00Z"
    }
  ]
}
```

---

### 5.2 WebSocket API for Real-Time Chat

```python
# WebSocket Connection for streaming responses and real-time notifications

Connection: ws://api.smartai.com/v1/ws
Headers:
  Authorization: Bearer <access_token>

Subscribe Message:
{
  "type": "subscribe",
  "channels": ["conversation_updates", "alerts", "health_metrics"]
}

Send Message:
{
  "type": "message",
  "conversation_id": "conv_123",
  "content": "How are you today?",
  "health_signals": {
    "mood_level": 7
  }
}

Response Stream:
{
  "type": "message_response",
  "message_id": "msg_790",
  "chunk": "I'm glad",
  "is_final": false,
  "timestamp": "2024-01-15T10:05:02Z"
}

{
  "type": "message_response",
  "message_id": "msg_790",
  "chunk": " you're doing well today!",
  "is_final": true,
  "timestamp": "2024-01-15T10:05:03Z",
  "full_message": "I'm glad you're doing well today!",
  "voice_url": "https://audio.smartai.com/msg_790.mp3"
}

Alert Notification:
{
  "type": "alert",
  "alert_id": "alert_123",
  "severity": "warning",
  "title": "Unusual mood decline",
  "timestamp": "2024-01-15T10:10:00Z"
}

Disconnection:
{
  "type": "disconnect",
  "reason": "Token expired"
}
```

---

### 5.3 Error Response Format

```json
{
  "error": {
    "code": "INVALID_REQUEST",
    "message": "The request parameters are invalid",
    "details": [
      {
        "field": "email",
        "issue": "Invalid email format"
      }
    ],
    "request_id": "req_abc123",
    "timestamp": "2024-01-15T10:00:00Z"
  }
}

Common Error Codes:
- INVALID_REQUEST: 400
- UNAUTHORIZED: 401
- FORBIDDEN: 403
- NOT_FOUND: 404
- CONFLICT: 409
- RATE_LIMITED: 429
- INTERNAL_ERROR: 500
- SERVICE_UNAVAILABLE: 503
```

---

## 6. Memory Systems

### 6.1 Three-Layer Memory Architecture

```
┌─────────────────────────────────────────────────────────────┐
│              SHORT-TERM MEMORY (Current Context)            │
│              Kept in API request/response context            │
├─────────────────────────────────────────────────────────────┤
│  - Last N messages (typically 10-15)                        │
│  - Current conversation context                             │
│  - Recent health signals                                    │
│  - TTL: Duration of current conversation                    │
│  - Storage: Redis cache + API memory                        │
│  - Access: Direct context injection to LLM                 │
└─────────────────────────────────────────────────────────────┘
                              ▲
                              │
┌─────────────────────────────┼──────────────────────────────┐
│      MID-TERM MEMORY (Last 7-30 days)                       │
│      Cached for quick retrieval                             │
├─────────────────────────────┼──────────────────────────────┤
│  - Recent conversation summaries                            │
│  - Health trend data                                        │
│  - Behavioral patterns                                      │
│  - TTL: 24 hours                                            │
│  - Storage: Redis cache                                     │
│  - Access: Retrieved on conversation start                 │
└─────────────────────────────┬──────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│         LONG-TERM MEMORY (Historical Context)               │
│         Semantic search with embeddings                     │
├─────────────────────────────────────────────────────────────┤
│  - All past conversations (embeddings)                      │
│  - Historical health patterns                               │
│  - Personality/preference data                              │
│  - Storage: Vector DB (Weaviate/Pinecone)                  │
│  - Storage: PostgreSQL (structured data)                    │
│  - Access: RAG-based semantic search                        │
│  - TTL: Indefinite (compliant archival)                    │
└─────────────────────────────────────────────────────────────┘
```

### 6.2 Memory Retrieval Flow (RAG Pipeline)

```
User Query: "What medication did I start last month?"

┌─────────────────────────────────────────────────┐
│  1. QUERY ENCODING                              │
│     Convert query to embedding vector            │
│     Model: sentence-transformers/all-MiniLM     │
└────────────────────┬────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────┐
│  2. SEMANTIC SEARCH IN VECTOR DB                │
│     Find top-K similar contexts (K=5)            │
│     Score: Cosine similarity threshold > 0.6    │
└────────────────────┬────────────────────────────┘
                     │
        ┌────────────┴────────────┐
        │ Retrieved Contexts:     │
        │ 1. "Started Lisinopril" │
        │ 2. "BP medication"      │
        │ 3. "Doctor advised..."  │
        └────────────┬────────────┘
                     │
┌────────────────────▼────────────────────────────┐
│  3. CONTEXT RANKING & FILTERING                 │
│     - Remove duplicates                         │
│     - Sort by relevance                         │
│     - Filter by time window                     │
│     - Max context tokens: 2000                  │
└────────────────────┬────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────┐
│  4. PROMPT AUGMENTATION                         │
│     Inject ranked contexts into system prompt   │
└────────────────────┬────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────┐
│  5. LLM RESPONSE GENERATION                     │
│     Claude generates contextualized response    │
│     Response: "You started Lisinopril last..."  │
└────────────────────┬────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────┐
│  6. RESPONSE EMBEDDING & STORAGE                │
│     Store response as new embedding             │
│     Link to conversation for future retrieval   │
└─────────────────────────────────────────────────┘
```

### 6.3 Memory System Implementation

```python
# backend/services/memory_service.py

from typing import List, Dict, Any
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Weaviate
from langchain.text_splitter import RecursiveCharacterTextSplitter
from redis import Redis
import json
from datetime import datetime, timedelta

class MemoryService:
    """Manages 3-layer memory system for Smart AI"""

    def __init__(self, vector_client, postgres_client, redis_client):
        self.vector_db = vector_client
        self.postgres = postgres_client
        self.redis = redis_client
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )

    # ============ SHORT-TERM MEMORY ============

    async def get_conversation_context(
        self,
        conversation_id: str,
        limit: int = 10
    ) -> Dict[str, Any]:
        """Get recent messages for current conversation context"""

        # Try Redis cache first
        cache_key = f"conversation:{conversation_id}:context"
        cached = self.redis.get(cache_key)
        if cached:
            return json.loads(cached)

        # Query database
        messages = self.postgres.query("""
            SELECT
                id, content, sender_type, sentiment,
                health_signals, created_at
            FROM chat_messages
            WHERE conversation_id = %s
            ORDER BY created_at DESC
            LIMIT %s
        """, [conversation_id, limit])

        context = {
            "conversation_id": conversation_id,
            "messages": messages,
            "retrieved_at": datetime.now().isoformat()
        }

        # Cache for 30 minutes
        self.redis.setex(cache_key, 1800, json.dumps(context))

        return context

    # ============ MID-TERM MEMORY ============

    async def get_recent_summary(
        self,
        user_id: str,
        days: int = 7
    ) -> Dict[str, Any]:
        """Get summary of recent conversations and patterns"""

        cache_key = f"user:{user_id}:summary:{days}d"
        cached = self.redis.get(cache_key)
        if cached:
            return json.loads(cached)

        # Aggregate recent data
        summary = {
            "user_id": user_id,
            "time_period": f"last_{days}_days",
            "conversation_count": 0,
            "average_sentiment": None,
            "health_trends": {},
            "behavioral_patterns": [],
            "key_topics": []
        }

        # Query aggregates
        result = self.postgres.query("""
            SELECT
                COUNT(*) as conv_count,
                AVG(CASE WHEN sentiment='positive' THEN 1
                         WHEN sentiment='neutral' THEN 0.5
                         ELSE 0 END) as avg_sentiment,
                array_agg(DISTINCT message_class) as topics
            FROM chat_messages
            WHERE user_id = %s
                AND created_at >= NOW() - INTERVAL %s
                AND sender_type = 'user'
        """, [user_id, f"{days} days"])

        if result:
            summary.update(result[0])

        # Cache for 6 hours
        self.redis.setex(cache_key, 21600, json.dumps(summary))

        return summary

    # ============ LONG-TERM MEMORY - RAG PIPELINE ============

    async def semantic_search(
        self,
        user_id: str,
        query: str,
        limit: int = 5,
        similarity_threshold: float = 0.6,
        time_window_days: int = 90
    ) -> List[Dict[str, Any]]:
        """
        Semantic search over historical conversations using embeddings
        """

        # Generate query embedding
        query_embedding = self.embeddings.embed_query(query)

        # Search Weaviate with hybrid search (keyword + semantic)
        where_filter = {
            "path": ["user_id"],
            "operator": "Equal",
            "valueString": user_id
        }

        results = self.vector_db.query(
            class_name="UserHealthContext",
            where=where_filter,
            vector=query_embedding,
            limit=limit,
            alpha=0.5  # 50% semantic, 50% keyword
        )

        # Filter by similarity threshold and time window
        filtered_results = []
        cutoff_date = datetime.now() - timedelta(days=time_window_days)

        for result in results:
            if result.get("_additional", {}).get("distance", 1.0) < (1 - similarity_threshold):
                timestamp = datetime.fromisoformat(result.get("timestamp"))
                if timestamp > cutoff_date:
                    filtered_results.append({
                        "id": result.get("id"),
                        "content": result.get("content"),
                        "summary": result.get("summary"),
                        "timestamp": result.get("timestamp"),
                        "health_topics": result.get("health_topics", []),
                        "relevance_score": 1 - result.get("_additional", {}).get("distance", 1.0),
                        "source": "semantic_search"
                    })

        return filtered_results

    async def augment_prompt_with_context(
        self,
        user_id: str,
        conversation_id: str,
        current_query: str,
        system_prompt: str
    ) -> str:
        """
        Augment system prompt with relevant historical context
        """

        # Get short-term context
        short_term = await self.get_conversation_context(conversation_id)

        # Get semantic matches for current query
        semantic_matches = await self.semantic_search(
            user_id=user_id,
            query=current_query,
            limit=3
        )

        # Build augmented context
        context_section = "\n## User Context:\n"

        if semantic_matches:
            context_section += "\nRelevant historical information:\n"
            for i, match in enumerate(semantic_matches, 1):
                context_section += f"{i}. {match['summary']} (relevance: {match['relevance_score']:.2%})\n"

        # Add recent pattern information
        recent_summary = await self.get_recent_summary(user_id, days=7)
        if recent_summary.get("average_sentiment"):
            context_section += f"\nRecent mood trend: {recent_summary['average_sentiment']:.1%}\n"

        # Add short-term messages
        context_section += "\nRecent conversation:\n"
        for msg in short_term.get("messages", [])[-5:]:
            context_section += f"- [{msg['sender_type']}]: {msg['content'][:100]}...\n"

        # Inject into prompt (carefully manage token count)
        augmented_prompt = system_prompt + context_section

        return augmented_prompt

    # ============ MEMORY MAINTENANCE ============

    async def refresh_embeddings(
        self,
        user_id: str,
        time_period: str = "last_7_days"
    ) -> Dict[str, Any]:
        """
        Background job to refresh embeddings for new conversations
        """

        if time_period == "last_7_days":
            since_date = datetime.now() - timedelta(days=7)
        elif time_period == "last_30_days":
            since_date = datetime.now() - timedelta(days=30)
        else:
            since_date = None

        # Get messages that need embedding
        query = """
            SELECT cm.id, cm.conversation_id, cm.content, cm.created_at,
                   cs.id as session_id, array_agg(cm.message_class) as topics
            FROM chat_messages cm
            JOIN conversation_sessions cs ON cm.conversation_id = cs.id
            WHERE cm.user_id = %s
                AND cm.embedding_id IS NULL
                AND cm.sender_type = 'user'
        """

        if since_date:
            query += f" AND cm.created_at >= '{since_date.isoformat()}'"

        messages = self.postgres.query(query, [user_id])

        embeddings_created = 0

        for msg in messages:
            # Split long messages
            splitter = RecursiveCharacterTextSplitter(
                chunk_size=500,
                chunk_overlap=50
            )
            chunks = splitter.split_text(msg["content"])

            for chunk in chunks:
                # Create embedding
                embedding = self.embeddings.embed_query(chunk)

                # Store in Weaviate
                obj = {
                    "content": chunk,
                    "user_id": user_id,
                    "conversation_id": msg["conversation_id"],
                    "timestamp": msg["created_at"].isoformat(),
                    "health_topics": msg.get("topics", []),
                    "sentiment": "neutral"  # Would be classified separately
                }

                weaviate_id = self.vector_db.create(
                    class_name="UserHealthContext",
                    properties=obj,
                    vector=embedding
                )

                embeddings_created += 1

                # Update reference in PostgreSQL
                self.postgres.execute(
                    "UPDATE chat_messages SET embedding_id = %s WHERE id = %s",
                    [weaviate_id, msg["id"]]
                )

        return {
            "embeddings_created": embeddings_created,
            "user_id": user_id,
            "time_period": time_period
        }

    async def cleanup_old_cache(self):
        """Remove expired cache entries"""
        # Redis handles this with TTL automatically
        # This is for manual cleanup if needed
        pass
```

### 6.4 Prompt Engineering for Persona

```python
# backend/services/llm_service.py

SYSTEM_PROMPT_TEMPLATE = """
You are a compassionate AI companion with a nurse-like persona, designed to provide
empathetic support and health monitoring for elderly adults.

## Your Personality & Guidelines:

### Communication Style
- Speak clearly and use simple language (avoid jargon)
- Use a warm, patient, and encouraging tone
- Show genuine interest and empathy
- Address the person by name when appropriate
- Speak as if talking to a respected elder

### Health Awareness
- Always prioritize the user's wellbeing
- Ask follow-up questions about health concerns
- Remember and reference previous health discussions
- Gently suggest professional help when needed
- Never provide medical advice; encourage consultation with doctors

### Memory & Personalization
- Reference past conversations when relevant
- Remember likes, dislikes, family members, and routines
- Acknowledge patterns you observe (e.g., "You mentioned better sleep lately")
- Tailor responses based on user preferences

### Tone & Pacing
- Give yourself permission to take time responding (no rushing)
- Use short, clear sentences
- Pause thoughtfully before responding
- Show you're listening by acknowledging what was said

### Safety & Boundaries
- If user mentions crisis/emergency, suggest calling emergency services
- Do not diagnosis medical conditions
- Encourage them to speak with their healthcare provider
- If user seems at risk, escalate appropriately

## User Profile:
{user_profile}

## Recent Context:
{recent_context}

## Relevant Historical Information:
{semantic_context}

---

Now, respond to the user's message with empathy and care:
"""

async def generate_response(
    user_id: str,
    conversation_id: str,
    user_message: str,
    health_signals: Dict = None
) -> str:
    """
    Generate contextualized response using Claude API with augmented memory
    """

    # Get user profile
    user = await get_user_profile(user_id)

    # Get augmented context
    recent_context = await memory_service.get_conversation_context(conversation_id)
    semantic_context = await memory_service.semantic_search(
        user_id=user_id,
        query=user_message,
        limit=3
    )

    # Format context for prompt
    context_messages = "\n".join([
        f"[{msg['sender_type']}]: {msg['content']}"
        for msg in recent_context[-5:]
    ])

    semantic_context_str = "\n".join([
        f"- {ctx['summary']} (from {ctx['timestamp']})"
        for ctx in semantic_context
    ])

    # Build final prompt
    final_prompt = SYSTEM_PROMPT_TEMPLATE.format(
        user_profile=f"Name: {user['first_name']}, Age: {user.age}, Timezone: {user['timezone']}",
        recent_context=context_messages,
        semantic_context=semantic_context_str
    )

    # Stream response from Claude
    response_text = ""
    async with anthropic.Anthropic() as client:
        with client.messages.stream(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1024,
            system=final_prompt,
            messages=[{
                "role": "user",
                "content": user_message
            }]
        ) as stream:
            for text in stream.text_stream:
                response_text += text
                yield text  # Stream back to client

    return response_text
```

---

## 7. Security & Compliance

### 7.1 HIPAA Compliance Architecture

```
┌──────────────────────────────────────────────────────┐
│            HIPAA SECURITY SAFEGUARDS               │
├──────────────────────────────────────────────────────┤
│                                                      │
│  1. ADMINISTRATIVE SAFEGUARDS                       │
│     - Access controls and authentication            │
│     - Workforce security training                   │
│     - Audit controls and logging                    │
│     - Security incident procedures                  │
│                                                      │
│  2. PHYSICAL SAFEGUARDS                             │
│     - Facility access controls                      │
│     - Data center security                          │
│     - Device and media controls                     │
│                                                      │
│  3. TECHNICAL SAFEGUARDS                            │
│     - Encryption (transit & rest)                   │
│     - Access controls (authentication & authz)      │
│     - Audit controls (detailed logging)             │
│     - Integrity controls (checksums)                │
│                                                      │
└──────────────────────────────────────────────────────┘
```

### 7.2 Encryption Strategy

```python
# backend/services/security_service.py

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2
import os
import base64

class EncryptionService:
    """Handles encryption/decryption of sensitive health data"""

    def __init__(self, kms_client):
        self.kms = kms_client  # AWS KMS or similar

    def encrypt_health_data(
        self,
        data: str,
        user_id: str,
        data_type: str = "health_record"
    ) -> str:
        """
        Encrypt sensitive health data using key management service

        Encryption hierarchy:
        - User DEK (Data Encryption Key) stored in KMS
        - Data encrypted with DEK
        - DEK key version tracked in DB
        """

        # Get or create user's DEK from KMS
        dek = self.kms.get_or_create_dek(user_id)

        # Encrypt data
        cipher_suite = Fernet(dek)
        encrypted_data = cipher_suite.encrypt(data.encode())

        # Return with key version for future decryption
        return {
            "encrypted_value": encrypted_data.decode(),
            "key_version": self.kms.get_key_version(user_id)
        }

    def decrypt_health_data(
        self,
        encrypted_data: str,
        user_id: str,
        key_version: int
    ) -> str:
        """Decrypt health data using stored key version"""

        # Retrieve specific DEK version
        dek = self.kms.get_dek(user_id, key_version)
        cipher_suite = Fernet(dek)

        try:
            decrypted = cipher_suite.decrypt(encrypted_data.encode())
            return decrypted.decode()
        except Exception as e:
            log_security_event("decryption_failure", user_id, str(e))
            raise
```

### 7.3 Authentication & Authorization

```python
# backend/services/auth_service.py

from fastapi_jwt_extended import create_access_token, create_refresh_token
from datetime import datetime, timedelta
import os

class AuthService:
    """OAuth2 with JWT tokens"""

    async def login(self, email: str, password: str) -> Dict:
        """
        Login with OAuth2 / OIDC pattern

        Flow:
        1. Validate credentials
        2. Check MFA requirement
        3. Generate JWT tokens
        4. Store device info
        """

        user = await self.db.get_user_by_email(email)
        if not user or not self.verify_password(password, user.password_hash):
            log_security_event("failed_login", email)
            raise UnauthorizedException("Invalid credentials")

        # Check if MFA required
        if user.mfa_enabled:
            mfa_token = create_access_token(
                data={"sub": user.id, "type": "mfa"},
                expires_delta=timedelta(minutes=5)
            )
            return {"mfa_required": True, "mfa_token": mfa_token}

        # Generate tokens
        access_token = create_access_token(
            data={"sub": user.id, "type": "access"},
            expires_delta=timedelta(hours=1)
        )

        refresh_token = create_refresh_token(
            data={"sub": user.id, "type": "refresh"},
            expires_delta=timedelta(days=30)
        )

        log_security_event("successful_login", user.id)

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "expires_in": 3600
        }

# RBAC (Role-Based Access Control)

PERMISSION_MATRIX = {
    "user": {
        "chat_messages": ["create", "read_own"],
        "health_metrics": ["create", "read_own"],
        "profile": ["read_own", "update_own"],
        "alerts": ["read_own"]
    },
    "caregiver": {
        "chat_messages": ["read_approved"],
        "health_metrics": ["read_approved"],
        "alerts": ["read_approved"]
    },
    "healthcare_provider": {
        "health_metrics": ["read_approved"],
        "alerts": ["read_approved"],
        "recommendations": ["create"]
    },
    "admin": {
        "*": ["*"]  # Full access
    }
}

async def check_permission(
    user_id: str,
    resource: str,
    action: str,
    resource_owner_id: str = None
) -> bool:
    """Check if user has permission for action"""

    user = await get_user(user_id)
    user_role = user.role

    permissions = PERMISSION_MATRIX.get(user_role, {})

    # Check if admin
    if "*" in permissions:
        return True

    # Check resource permissions
    resource_perms = permissions.get(resource, [])
    if action not in resource_perms:
        return False

    # Check ownership for personal resources
    if action == "read_own" and resource_owner_id != user_id:
        return False

    return True
```

### 7.4 Audit Logging

```python
# backend/services/audit_service.py

async def log_audit_event(
    action: str,
    entity_type: str,
    entity_id: str,
    actor_user_id: str,
    old_values: Dict = None,
    new_values: Dict = None,
    status: str = "success",
    ip_address: str = None
):
    """Log all health data access and modifications for HIPAA compliance"""

    audit_log = {
        "action": action,
        "entity_type": entity_type,
        "entity_id": entity_id,
        "actor_user_id": actor_user_id,
        "old_values": encrypt_for_log(old_values),
        "new_values": encrypt_for_log(new_values),
        "status": status,
        "ip_address": ip_address,
        "timestamp": datetime.now().isoformat(),
        "request_id": get_request_id()
    }

    # Write to database
    await db.audit_logs.insert_one(audit_log)

    # Write to audit log file (for archival)
    with open(f"/var/log/smartai/audit-{datetime.now().date()}.log", "a") as f:
        f.write(json.dumps(audit_log) + "\n")

    # Alert if suspicious activity
    if is_suspicious(action, actor_user_id):
        await send_security_alert(audit_log)

# Events to log:
AUDIT_EVENTS = [
    ("health_metric_viewed", "health_metrics"),
    ("health_metric_created", "health_metrics"),
    ("chat_message_accessed", "chat_messages"),
    ("user_profile_accessed", "users"),
    ("user_profile_updated", "users"),
    ("caregiver_permission_changed", "caregiver_relationships"),
    ("alert_acknowledged", "alerts"),
    ("data_export_requested", "exports"),
]
```

### 7.5 Data Privacy & Consent

```python
# backend/models/consent.py

class ConsentModel(BaseModel):
    """User consent for data usage"""

    user_id: UUID

    # Data sharing
    share_with_caregivers: bool = True
    share_with_healthcare_providers: bool = False
    share_for_emergency_alerts: bool = True

    # Analytics
    analytics_enabled: bool = False
    research_participation: bool = False

    # Preferences
    voice_data_retention_days: int = 30  # Auto-delete
    conversation_retention_days: int = 3650  # 10 years

    # Consent tracking
    consented_at: datetime
    expires_at: Optional[datetime] = None
    consent_version: str  # Track consent policy version
```

---

## 8. Voice Integration

### 8.1 Voice I/O Architecture

```
┌─────────────────┐
│  User speaks    │
└────────┬────────┘
         │
         ▼
┌─────────────────────────────┐
│  Speech Recognition (STT)   │
│  - Google Cloud STT         │
│  - Azure Speech Services    │
│  - Local Vosk (privacy)     │
└────────┬────────────────────┘
         │
         ▼
┌─────────────────────────────┐
│  Text Processing            │
│  - Intent recognition       │
│  - Entity extraction        │
│  - Sentiment analysis       │
└────────┬────────────────────┘
         │
         ▼
┌─────────────────────────────┐
│  LLM Processing             │
│  - Generate response        │
│  - Apply persona            │
│  - Consider context         │
└────────┬────────────────────┘
         │
         ▼
┌─────────────────────────────┐
│  Speech Synthesis (TTS)     │
│  - Google Cloud TTS         │
│  - Azure Speech Services    │
│  - Natural voice            │
└────────┬────────────────────┘
         │
         ▼
┌─────────────────┐
│  Audio playback │
│  to user        │
└─────────────────┘
```

### 8.2 Voice Service Implementation

```typescript
// mobile/services/voiceService.ts

import Voice from '@react-native-voice/voice';
import TextToSpeech from 'react-native-tts';

interface VoiceConfig {
  language: 'en-US' | 'es-ES' | 'fr-FR';
  voiceGender: 'male' | 'female';
  speechRate: number; // 0.5 to 2.0, slower for elderly
  pitch: number; // 0.5 to 2.0
  volume: number; // 0 to 1
}

class VoiceService {
  private isListening: boolean = false;
  private config: VoiceConfig;

  constructor(config: VoiceConfig) {
    this.config = config;

    Voice.onSpeechStart = this.onSpeechStart.bind(this);
    Voice.onSpeechRecognized = this.onSpeechRecognized.bind(this);
    Voice.onSpeechEnd = this.onSpeechEnd.bind(this);
    Voice.onSpeechError = this.onSpeechError.bind(this);
    Voice.onSpeechResults = this.onSpeechResults.bind(this);
  }

  async startListening(): Promise<void> {
    if (this.isListening) return;

    try {
      // Request microphone permission
      const permission = await this.requestMicrophonePermission();
      if (!permission) throw new Error('Microphone permission denied');

      this.isListening = true;

      // Start speech recognition
      // Timeout: 60 seconds of silence
      await Voice.start(this.config.language, {
        timeout: 60000,
        continuous: false,
        recognizeGoogle: true
      });
    } catch (error) {
      console.error('Speech recognition error:', error);
      this.isListening = false;
      throw error;
    }
  }

  async stopListening(): Promise<void> {
    if (!this.isListening) return;

    try {
      await Voice.stop();
      this.isListening = false;
    } catch (error) {
      console.error('Error stopping voice:', error);
    }
  }

  private onSpeechStart(): void {
    console.log('Speech recognition started');
    // Show visual indicator
    emit('voice_started');
  }

  private onSpeechRecognized(): void {
    console.log('Speech recognized');
  }

  private onSpeechEnd(): void {
    console.log('Speech ended');
    this.isListening = false;
  }

  private onSpeechError(error: any): void {
    console.error('Speech error:', error);
    emit('voice_error', error);
    this.isListening = false;
  }

  private onSpeechResults(results: string[]): void {
    // Results are sorted by confidence
    const transcribedText = results[0];

    // Send to backend
    emit('speech_recognized', transcribedText);
  }

  async speak(text: string): Promise<void> {
    try {
      await TextToSpeech.stop();

      await TextToSpeech.speak({
        text: text,
        language: this.config.language.split('-')[0],
        rate: this.config.speechRate,
        pitch: this.config.pitch,
        volume: this.config.volume,
        androidParams: {
          KEY_PARAM_PAN: 0,
          KEY_PARAM_VOLUME: this.config.volume,
          KEY_PARAM_STREAM: 'STREAM_MUSIC'
        }
      });

      // Handle completion
      TextToSpeech.addEventListener('tts-finish', () => {
        emit('speech_finished');
      });

      TextToSpeech.addEventListener('tts-cancel', () => {
        emit('speech_cancelled');
      });

    } catch (error) {
      console.error('Text-to-speech error:', error);
      throw error;
    }
  }

  private async requestMicrophonePermission(): Promise<boolean> {
    // Platform-specific permission handling
    const permission = await PermissionsAndroid.request(
      PermissionsAndroid.PERMISSIONS.RECORD_AUDIO
    );
    return permission === PermissionsAndroid.RESULTS.GRANTED;
  }

  async updateConfig(newConfig: Partial<VoiceConfig>): Promise<void> {
    this.config = { ...this.config, ...newConfig };
  }
}

export default VoiceService;
```

---

## 9. Offline-First Strategy

### 9.1 Offline Architecture

```
┌──────────────────────────────────┐
│    Online Status Detection       │
├──────────────────────────────────┤
│  - Network connectivity check    │
│  - API health endpoint            │
│  - Graceful degradation           │
└──────────────┬───────────────────┘
               │
        ┌──────▼──────┐
        │  ONLINE?    │
        └──┬───────┬──┘
           │       │
       YES │       │ NO
          │       │
    ┌─────▼─┐  ┌──▼──────────────────────┐
    │ SYNC  │  │ LOCAL MODE              │
    │ MODE  │  │ - Store locally         │
    └─────────  │ - Queue operations     │
               │ - Serve from cache     │
               │ - Graceful errors      │
               └──┬─────────────────────┘
                  │
        ┌─────────▼──────────┐
        │ When back online:   │
        │ - Sync queued ops   │
        │ - Resolve conflicts │
        │ - Merge data        │
        └────────────────────┘
```

### 9.2 Offline Sync Implementation

```typescript
// mobile/services/syncService.ts

import WatermelonDB from '@nozbe/watermelondb';
import SQLiteAdapter from '@nozbe/watermelondb/adapters/sqlite';

interface SyncQueueItem {
  id: string;
  operationType: 'create' | 'update' | 'delete';
  entityType: 'message' | 'metric';
  localId: string;
  serverId?: string;
  payload: any;
  timestamp: number;
  retryCount: number;
  status: 'pending' | 'synced' | 'failed' | 'conflict';
}

class SyncService {
  private db: WatermelonDB.Database;
  private isOnline: boolean = true;
  private syncInProgress: boolean = false;
  private syncQueue: SyncQueueItem[] = [];
  private conflictResolver: ConflictResolver;

  constructor(database: WatermelonDB.Database) {
    this.db = database;
    this.monitorConnectivity();
    this.conflictResolver = new ConflictResolver();
  }

  private monitorConnectivity(): void {
    // Monitor network state
    NetInfo.addEventListener((state) => {
      const wasOnline = this.isOnline;
      this.isOnline = state.isConnected && state.isInternetReachable;

      // Trigger sync if we just came online
      if (!wasOnline && this.isOnline) {
        this.syncWithServer();
      }
    });
  }

  // Operation: Add message locally
  async addMessageOffline(message: LocalChatMessage): Promise<void> {
    const localId = uuidv4();

    // Save to local database
    await this.db.write(async () => {
      await this.db.get('local_chat_messages').create((record) => {
        record.local_id = localId;
        record.content = message.content;
        record.sender_type = message.senderType;
        record.sync_status = 'pending';
        record.timestamp = new Date();
      });
    });

    // Add to sync queue
    await this.addToSyncQueue({
      operationType: 'create',
      entityType: 'message',
      localId: localId,
      payload: message
    });

    // Emit event
    emit('message_added_offline', { localId });

    // Try to sync if online
    if (this.isOnline) {
      await this.syncWithServer();
    }
  }

  private async addToSyncQueue(item: Partial<SyncQueueItem>): Promise<void> {
    const queueItem: SyncQueueItem = {
      id: uuidv4(),
      operationType: item.operationType || 'create',
      entityType: item.entityType || 'message',
      localId: item.localId || '',
      payload: item.payload || {},
      timestamp: Date.now(),
      retryCount: 0,
      status: 'pending',
      ...item
    };

    // Store in queue table
    await this.db.write(async () => {
      await this.db.get('sync_queue').create((record) => {
        Object.assign(record, queueItem);
      });
    });

    this.syncQueue.push(queueItem);
  }

  async syncWithServer(): Promise<SyncResult> {
    if (this.syncInProgress || !this.isOnline) {
      return { status: 'skipped', reason: 'Already syncing or offline' };
    }

    this.syncInProgress = true;
    emit('sync_started');

    try {
      // Get pending operations
      const pendingOps = await this.db.get('sync_queue')
        .query(WatermelonDB.Q.where('status', 'pending'))
        .fetch();

      // Sync each operation
      for (const op of pendingOps) {
        try {
          const result = await this.syncOperation(op);

          // Update local record
          await this.db.write(async () => {
            await op.update((record) => {
              record.status = result.status;
              record.serverId = result.serverId;
              if (result.status === 'synced') {
                record.retryCount = 0;
              } else {
                record.retryCount += 1;
              }
            });
          });

          // Update local message if successful
          if (result.status === 'synced' && op.entityType === 'message') {
            await this.updateLocalRecord(op.localId, {
              serverId: result.serverId,
              sync_status: 'synced'
            });
          }

        } catch (error) {
          console.error('Sync error for operation:', op.id, error);

          // Mark for retry (exponential backoff)
          await this.db.write(async () => {
            await op.update((record) => {
              record.status = 'failed';
              record.retryCount += 1;
            });
          });
        }
      }

      emit('sync_completed');
      return { status: 'completed', syncedCount: pendingOps.length };

    } finally {
      this.syncInProgress = false;
    }
  }

  private async syncOperation(operation: SyncQueueItem): Promise<SyncOperationResult> {
    const { operationType, entityType, payload, localId } = operation;

    switch (operationType) {
      case 'create':
        return await this.syncCreate(entityType, payload, localId);

      case 'update':
        return await this.syncUpdate(entityType, operation.serverId, payload);

      case 'delete':
        return await this.syncDelete(entityType, operation.serverId);

      default:
        throw new Error(`Unknown operation type: ${operationType}`);
    }
  }

  private async syncCreate(
    entityType: string,
    payload: any,
    localId: string
  ): Promise<SyncOperationResult> {
    const response = await api.post(`/api/v1/${entityType}`, payload);

    return {
      status: 'synced',
      serverId: response.id,
      localId: localId
    };
  }

  private async syncUpdate(
    entityType: string,
    serverId: string,
    payload: any
  ): Promise<SyncOperationResult> {
    await api.put(`/api/v1/${entityType}/${serverId}`, payload);

    return {
      status: 'synced',
      serverId: serverId
    };
  }

  private async syncDelete(
    entityType: string,
    serverId: string
  ): Promise<SyncOperationResult> {
    await api.delete(`/api/v1/${entityType}/${serverId}`);

    return {
      status: 'synced',
      serverId: serverId
    };
  }

  // Handle conflicts
  private async resolveConflict(
    localData: any,
    remoteData: any,
    entityType: string
  ): Promise<any> {
    // Use configurable conflict resolution strategies
    const strategy = this.conflictResolver.getStrategy(entityType);

    return await strategy.resolve(localData, remoteData);
  }
}

// Conflict Resolution Strategies
class ConflictResolver {
  getStrategy(entityType: string): ConflictResolutionStrategy {
    switch (entityType) {
      case 'message':
        return new LastWriteWinsStrategy();
      case 'metric':
        return new MergeStrategy();
      default:
        return new LastWriteWinsStrategy();
    }
  }
}

class LastWriteWinsStrategy implements ConflictResolutionStrategy {
  async resolve(local: any, remote: any): Promise<any> {
    // Compare timestamps, use newer version
    return local.timestamp > remote.timestamp ? local : remote;
  }
}

class MergeStrategy implements ConflictResolutionStrategy {
  async resolve(local: any, remote: any): Promise<any> {
    // For metrics, merge readings
    return {
      ...remote,
      local_observations: local.local_observations || remote.local_observations
    };
  }
}
```

---

## 10. Implementation Roadmap

### 10.1 Phase 1: MVP (Weeks 1-4)

#### Week 1: Core Infrastructure & Authentication

**Deliverables:**
- PostgreSQL schema deployed
- FastAPI backend skeleton
- JWT authentication implementation
- Device registration flow
- React Native mobile app scaffold

**Tasks:**
```
- [] Set up PostgreSQL database with initial schema
- [] Implement FastAPI with async handlers
- [] Build OAuth2/JWT authentication service
- [] Create user registration API
- [] Implement device registration
- [] Set up error handling and logging
- [] Create mobile app UI shell
- [] Set up Redux state management

Estimated Hours: 80 hours
Team: 2 Backend + 1 Mobile
```

#### Week 2: Chat Functionality & Basic RAG

**Deliverables:**
- Chat API endpoints
- Claude API integration
- Basic embeddings pipeline
- Vector DB setup (Weaviate local)
- Chat UI in mobile app

**Tasks:**
```
- [] Implement conversation endpoints
- [] Integrate Claude API
- [] Set up sentence-transformers for embeddings
- [] Deploy Weaviate locally
- [] Create chat message storage
- [] Build chat UI components
- [] Implement basic message streaming
- [] Add conversation history retrieval

Estimated Hours: 100 hours
Team: 2 Backend + 1 Mobile + 1 ML
```

#### Week 3: Voice Integration & Health Metrics

**Deliverables:**
- Speech-to-text integration
- Text-to-speech implementation
- Health metrics API
- Health metrics UI
- Initial persona refinement

**Tasks:**
```
- [] Integrate speech recognition (Google Cloud STT)
- [] Integrate text-to-speech (Google Cloud TTS)
- [] Create health metrics API
- [] Implement health metrics UI
- [] Add sentiment analysis to messages
- [] Create persona system prompt
- [] Refine response generation
- [] User testing for voice

Estimated Hours: 90 hours
Team: 1 Backend + 2 Mobile + 1 ML
```

#### Week 4: Offline Support & Polish

**Deliverables:**
- Offline sync engine
- Local SQLite storage
- Sync conflict resolution
- UI/UX refinements
- Comprehensive testing

**Tasks:**
```
- [] Implement WatermelonDB for local storage
- [] Build sync queue system
- [] Create conflict resolution logic
- [] Implement offline detection
- [] Add sync status indicators
- [] Refine voice experience
- [] Accessibility improvements
- [] Security audit (partial)
- [] Integration testing

Estimated Hours: 100 hours
Team: 2 Backend + 2 Mobile + 1 QA
```

**MVP Release Criteria:**
- Core chat with Claude working end-to-end
- Voice input/output functional
- Offline capability with sync
- Basic health metrics recording
- 50+ user testing cohort ready
- Security baseline met (encryption, auth)

---

### 10.2 Phase 2: Health Monitoring (Weeks 5-7)

**Focus:** Advanced health tracking, pattern detection, emergency alerts

**Key Features:**
- Behavioral pattern detection
- Health anomaly alerts
- Caregiver notifications
- Emergency contact system
- Health data dashboard

---

### 10.3 Phase 3: Production Hardening (Weeks 8-10)

**Focus:** Scale, security, compliance, operations

**Key Deliverables:**
- Kubernetes deployment
- Full HIPAA audit
- Advanced monitoring
- Disaster recovery
- Performance optimization

---

### 10.4 Critical Path

```
Start
  ↓
Database & Auth (CRITICAL)
  ↓
Chat API & Claude Integration (CRITICAL)
  ├→ Vector DB Setup (parallel)
  │   ↓
  ├→ Voice Integration (parallel)
  │   ↓
  └→ Offline Sync (CRITICAL)
      ↓
    MVP Ready
      ↓
Health Monitoring Features
      ↓
Production Deployment
```

---

## 11. Deployment & Operations

### 11.1 Local Development Setup

```dockerfile
# docker-compose.yml
version: '3.9'

services:
  postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: smartai
      POSTGRES_USER: smartai
      POSTGRES_PASSWORD: dev_password
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./scripts/init.sql:/docker-entrypoint-initdb.d/init.sql

  weaviate:
    image: semitechnologies/weaviate:latest
    environment:
      QUERY_DEFAULTS_LIMIT: 25
      AUTHENTICATION_ANONYMOUS_ACCESS_ENABLED: 'true'
    ports:
      - "8080:8080"
    volumes:
      - weaviate_data:/var/lib/weaviate

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

  fastapi:
    build:
      context: ./backend
      dockerfile: Dockerfile
    environment:
      DATABASE_URL: postgresql://smartai:dev_password@postgres:5432/smartai
      REDIS_URL: redis://redis:6379
      WEAVIATE_URL: http://weaviate:8080
      ANTHROPIC_API_KEY: ${ANTHROPIC_API_KEY}
    ports:
      - "8000:8000"
    depends_on:
      - postgres
      - redis
      - weaviate
    volumes:
      - ./backend:/app
      - /app/__pycache__

volumes:
  postgres_data:
  weaviate_data:
```

```bash
# Setup script
docker-compose up -d
docker-compose exec fastapi alembic upgrade head
docker-compose exec fastapi pytest tests/
```

### 11.2 Production Deployment Architecture

```
┌────────────────────────────────────────────────────────┐
│                   PRODUCTION DEPLOYMENT                │
├────────────────────────────────────────────────────────┤
│                                                        │
│  ┌──────────────────────────────────────────────┐    │
│  │  CDN / CloudFront (Static Assets)            │    │
│  └───────────────────┬──────────────────────────┘    │
│                      │                                │
│  ┌───────────────────▼──────────────────────────┐    │
│  │  API Gateway / Load Balancer                 │    │
│  │  - Rate limiting                              │    │
│  │  - WAF protection                            │    │
│  │  - SSL/TLS termination                       │    │
│  └───────────────────┬──────────────────────────┘    │
│                      │                                │
│  ┌───────────────────▼──────────────────────────┐    │
│  │  Kubernetes Cluster (EKS/GKE/AKS)           │    │
│  │  ┌──────────────────────────────────────┐   │    │
│  │  │ FastAPI Pods (autoscaled)            │   │    │
│  │  │ - Min: 3 replicas                    │   │    │
│  │  │ - Max: 20 replicas                   │   │    │
│  │  └──────────────────────────────────────┘   │    │
│  │  ┌──────────────────────────────────────┐   │    │
│  │  │ Ingress Controller (NGINX)           │   │    │
│  │  └──────────────────────────────────────┘   │    │
│  └────────────────────────────────────────────────   │
│                      │                                │
│  ┌───────────────────▼──────────────────────────┐    │
│  │  Managed Services                            │    │
│  │  - PostgreSQL (AWS RDS, read replicas)      │    │
│  │  - Redis Cluster (ElastiCache)              │    │
│  │  - Weaviate (Kubernetes StatefulSet)        │    │
│  │  - S3 / Cloud Storage (audit logs)          │    │
│  └──────────────────────────────────────────────┘    │
│                                                        │
│  ┌──────────────────────────────────────────────┐    │
│  │  Monitoring & Logging                        │    │
│  │  - Prometheus metrics                        │    │
│  │  - CloudWatch / Stackdriver logs             │    │
│  │  - Datadog / New Relic APM                   │    │
│  │  - AlertManager for incidents                │    │
│  └──────────────────────────────────────────────┘    │
│                                                        │
└────────────────────────────────────────────────────────┘
```

### 11.3 Kubernetes Deployment Configuration

```yaml
# backend/k8s/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: smartai-api
  namespace: smartai
spec:
  replicas: 3
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  selector:
    matchLabels:
      app: smartai-api
  template:
    metadata:
      labels:
        app: smartai-api
    spec:
      containers:
      - name: api
        image: smartai/api:latest
        imagePullPolicy: Always
        ports:
        - containerPort: 8000
          name: http

        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: smartai-secrets
              key: database-url
        - name: REDIS_URL
          valueFrom:
            configMapKeyRef:
              name: smartai-config
              key: redis-url
        - name: ANTHROPIC_API_KEY
          valueFrom:
            secretKeyRef:
              name: smartai-secrets
              key: anthropic-api-key

        # Health checks
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10

        readinessProbe:
          httpGet:
            path: /ready
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5

        # Resource limits
        resources:
          requests:
            memory: "512Mi"
            cpu: "250m"
          limits:
            memory: "1Gi"
            cpu: "500m"

        # Security context
        securityContext:
          runAsNonRoot: true
          allowPrivilegeEscalation: false
          readOnlyRootFilesystem: true
          capabilities:
            drop:
            - ALL

---
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: smartai-api-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: smartai-api
  minReplicas: 3
  maxReplicas: 20
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
```

### 11.4 Monitoring & Alerting

```python
# backend/services/monitoring.py

from prometheus_client import Counter, Histogram, Gauge
import time

# Define metrics
api_requests = Counter(
    'smartai_api_requests_total',
    'Total API requests',
    ['method', 'endpoint', 'status']
)

request_duration = Histogram(
    'smartai_api_request_duration_seconds',
    'API request duration in seconds',
    ['endpoint']
)

llm_tokens_used = Counter(
    'smartai_llm_tokens_used_total',
    'Total LLM tokens used',
    ['model']
)

health_alerts_triggered = Counter(
    'smartai_health_alerts_triggered_total',
    'Total health alerts triggered',
    ['alert_type', 'severity']
)

active_conversations = Gauge(
    'smartai_active_conversations',
    'Number of active conversations'
)

sync_queue_size = Gauge(
    'smartai_sync_queue_size',
    'Number of items in sync queue'
)

# Middleware for request tracking
@app.middleware("http")
async def track_requests(request, call_next):
    start_time = time.time()

    response = await call_next(request)

    duration = time.time() - start_time
    request_duration.labels(endpoint=request.url.path).observe(duration)
    api_requests.labels(
        method=request.method,
        endpoint=request.url.path,
        status=response.status_code
    ).inc()

    return response

# Alert rules (Prometheus)
ALERT_RULES = """
groups:
- name: smartai_alerts
  interval: 30s
  rules:
  - alert: HighErrorRate
    expr: rate(smartai_api_requests_total{status=~"5.."}[5m]) > 0.05
    for: 5m
    annotations:
      summary: "High error rate detected"

  - alert: HighLatency
    expr: histogram_quantile(0.95, smartai_api_request_duration_seconds) > 2
    for: 5m
    annotations:
      summary: "High API latency"

  - alert: SyncQueueBacklog
    expr: smartai_sync_queue_size > 1000
    for: 10m
    annotations:
      summary: "Sync queue backlog detected"
"""
```

---

## 12. Security Checklist

- [ ] TLS/SSL for all communications (1.3+)
- [ ] Strong password requirements (14+ chars, complexity)
- [ ] MFA implementation (TOTP/SMS)
- [ ] Rate limiting (per user, per IP)
- [ ] CORS properly configured
- [ ] CSRF tokens for state-changing ops
- [ ] Input validation on all endpoints
- [ ] SQL injection prevention (parameterized queries)
- [ ] XSS prevention (output encoding)
- [ ] Secure password hashing (bcrypt with 12+ rounds)
- [ ] Token expiration (short-lived access tokens)
- [ ] Refresh token rotation
- [ ] Audit logging for all health data access
- [ ] Encryption at rest (AES-256)
- [ ] Encryption in transit (TLS 1.3)
- [ ] Key management (HSM/KMS)
- [ ] Secrets management (not in code)
- [ ] PII data masking in logs
- [ ] HIPAA Business Associate Agreement
- [ ] Regular security audits/penetration testing
- [ ] Incident response plan
- [ ] Data retention policy enforcement
- [ ] Right-to-deletion (GDPR)
- [ ] Right-to-access (data export)
- [ ] Backup encryption and testing
- [ ] API authentication (every request)
- [ ] Authorization (RBAC)
- [ ] Device fingerprinting
- [ ] Anomaly detection

---

## 13. Cost Estimation

### Development Costs

| Component | Estimate | Notes |
|-----------|----------|-------|
| Backend Development | 400 hours | 2 engineers, 10 weeks |
| Mobile Development | 450 hours | 1 engineer, 11-12 weeks |
| ML/RAG Integration | 150 hours | 1 ML engineer, consulting |
| QA & Testing | 200 hours | Automation + manual |
| DevOps / Infrastructure | 100 hours | Setup, monitoring |
| **Total Dev Effort** | **1,300 hours** | **6-month timeline** |

### Infrastructure Costs (Monthly Production)

| Service | Estimated Cost |
|---------|-----------------|
| PostgreSQL (RDS, 4vCPU) | $500-800 |
| Weaviate / Vector DB | $300-500 |
| Redis cluster | $200-400 |
| Kubernetes cluster (EKS) | $600-1,000 |
| Claude API (at scale) | $5,000-20,000 |
| Speech services (STT/TTS) | $2,000-5,000 |
| CDN & storage | $500-1,000 |
| Monitoring & logs | $500-800 |
| **Total Monthly** | **$9,600-28,500** |

---

## 14. Risk Assessment & Mitigation

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|-----------|
| LLM API cost overrun | Medium | High | Token tracking, rate limits, fallback responses |
| Data privacy breach | Low | Critical | Encryption, audit logging, regular security audits |
| Poor elderly UX | Medium | Medium | User testing early, accessibility focus, voice-first |
| Offline sync conflicts | Medium | Medium | Comprehensive testing, well-designed conflict resolution |
| Regulatory compliance gaps | Medium | High | Legal review, HIPAA audit, documentation |
| Mobile app performance | Medium | Medium | Local caching, efficient queries, profiling |
| Server scaling issues | Low | High | Load testing, auto-scaling, capacity planning |

---

## 15. References & Resources

### Technology Documentation
- FastAPI: https://fastapi.tiangolo.com/
- PostgreSQL: https://www.postgresql.org/docs/
- Weaviate: https://weaviate.io/developers/weaviate/
- Anthropic Claude: https://docs.anthropic.com/
- React Native: https://reactnative.dev/docs

### Healthcare Compliance
- HIPAA Security Rule: https://www.hhs.gov/hipaa/
- HL7 Standards: http://www.hl7.org/
- FDA Software Guidance: https://www.fda.gov/

### Security Best Practices
- OWASP Top 10: https://owasp.org/Top10/
- CWE Top 25: https://cwe.mitre.org/top25/
- NIST Cybersecurity Framework: https://www.nist.gov/

---

## Summary

This comprehensive architecture provides:

1. **Scalable System Design:** Multi-layer architecture supporting growth from MVP to enterprise scale
2. **Privacy-First Approach:** Built-in encryption, audit logging, HIPAA compliance framework
3. **User-Centric Experience:** Voice-first interface, offline capability, accessibility focus
4. **Operational Excellence:** Monitoring, logging, auto-scaling, disaster recovery
5. **Phased Implementation:** Clear roadmap from MVP to production with defined milestones
6. **Technology Selection:** Justified choices balancing performance, cost, and team capability

The MVP can be delivered in 4 weeks with core functionality, followed by progressive feature rollout over 10 weeks to reach production-ready status.

---

**Document Version:** 1.0
**Last Updated:** January 15, 2024
**Status:** Ready for Implementation
**Next Review:** Post-MVP completion
