# Smart AI - Technical Summary & Quick Reference

## System Architecture at a Glance

```
USER (Elderly Adult)
    ↓
Mobile App (React Native)
    ├─ Chat Interface
    ├─ Voice Input/Output
    ├─ Health Tracking
    └─ Offline Support (WatermelonDB)
    ↓
API Gateway + Load Balancer
    ├─ Rate Limiting
    ├─ Authentication
    └─ Request Validation
    ↓
Backend Services (FastAPI)
    ├─ Chat Service
    ├─ LLM Integration (Claude API)
    ├─ Memory Service (RAG)
    ├─ Health Monitoring
    └─ Pattern Detection
    ↓
Data Layer
    ├─ PostgreSQL (Primary Data)
    ├─ Weaviate (Vector Embeddings)
    ├─ Redis (Cache & Sessions)
    └─ S3 (Backup & Audit Logs)
```

---

## Technology Stack Reference

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Mobile Frontend** | React Native | Cross-platform app |
| **Voice Input** | Google Cloud STT | Speech recognition |
| **Voice Output** | Google Cloud TTS | Text-to-speech |
| **Backend** | FastAPI (Python) | REST API & WebSocket |
| **LLM** | Anthropic Claude API | Conversational AI |
| **Primary DB** | PostgreSQL 15+ | Relational data |
| **Vector DB** | Weaviate | Embeddings & RAG |
| **Cache** | Redis | Session & performance |
| **Message Queue** | Redis/RabbitMQ | Async tasks |
| **Embeddings Model** | sentence-transformers/all-MiniLM-L6-v2 | Vector generation |
| **Monitoring** | Prometheus + Grafana | Observability |
| **Logging** | ELK Stack | Centralized logging |
| **Container** | Docker | Containerization |
| **Orchestration** | Kubernetes | Production deployment |

---

## API Endpoints Quick Reference

### Authentication
```
POST   /api/v1/auth/register          Register new user
POST   /api/v1/auth/login             Login with credentials
POST   /api/v1/auth/mfa/verify        Verify MFA code
POST   /api/v1/auth/refresh           Refresh access token
POST   /api/v1/auth/logout            Logout
```

### Chat
```
POST   /api/v1/conversations           Start new conversation
GET    /api/v1/conversations/{id}      Get conversation details
POST   /api/v1/conversations/{id}/messages          Send message
GET    /api/v1/conversations/{id}/messages          Get message history
POST   /api/v1/conversations/{id}/end  End conversation
WS     /api/v1/ws                      WebSocket for streaming
```

### Health
```
POST   /api/v1/health/metrics          Record health metric
GET    /api/v1/health/metrics          Get metrics history
GET    /api/v1/health/trends           Get health trends
```

### Memory & Context
```
GET    /api/v1/memory/context          Get relevant context
POST   /api/v1/memory/embeddings/refresh  Refresh embeddings
```

### Users
```
GET    /api/v1/users/profile           Get user profile
PUT    /api/v1/users/profile           Update profile
```

### Alerts
```
GET    /api/v1/alerts                  Get user alerts
PUT    /api/v1/alerts/{id}/acknowledge Acknowledge alert
```

### Caregivers
```
POST   /api/v1/caregivers/invite       Invite caregiver
GET    /api/v1/caregivers              Get user's caregivers
```

---

## Database Schema Quick Reference

### Core Tables

```
users                    → User accounts & profiles
devices                  → Device registration
conversation_sessions    → Chat sessions
chat_messages           → Individual messages
health_metrics          → Health readings
behavioral_patterns     → Detected patterns
alerts                  → System alerts
caregiver_relationships → Caregiver access
audit_logs              → Compliance logs
sync_queue              → Offline sync queue
token_blacklist         → Revoked tokens
```

### Key Fields by Table

**users:**
- id (UUID)
- email, password_hash
- medical_conditions, medications, allergies (JSONB)
- consents, hipaa_acknowledged

**chat_messages:**
- id (UUID)
- conversation_id, user_id
- content (TEXT)
- sentiment, health_signals
- embedding_id, sync_status

**health_metrics:**
- id (UUID)
- user_id
- mood_level, pain_level, energy_level, anxiety_level (1-10 INT)
- anomaly_detected, requires_attention (BOOLEAN)

---

## Memory System Reference

### Three-Layer Architecture

**Layer 1: Short-Term Memory**
- Duration: Current conversation only
- Storage: Redis + API context
- Retrieval: Direct injection to LLM
- Capacity: 10-15 recent messages

**Layer 2: Mid-Term Memory**
- Duration: 7-30 days
- Storage: Redis cache
- Retrieval: On conversation start
- Capacity: Summary + trends

**Layer 3: Long-Term Memory**
- Duration: Indefinite
- Storage: PostgreSQL + Weaviate
- Retrieval: Semantic search (RAG)
- Capacity: All historical data

### RAG Pipeline Flow

```
User Query
    ↓
Encode Query (sentence-transformers)
    ↓
Semantic Search (Weaviate hybrid search)
    ↓
Rank & Filter Results
    ↓
Inject into System Prompt
    ↓
Claude API Response Generation
    ↓
Store Response in Vector DB
```

---

## Security & Compliance Checklist

### Authentication & Authorization
- [x] OAuth2/JWT tokens
- [x] Token refresh rotation
- [x] MFA support
- [x] RBAC (Role-Based Access Control)
- [x] Device fingerprinting

### Encryption
- [x] TLS 1.3 for transport
- [x] AES-256 for data at rest
- [x] KMS for key management
- [x] Encrypted database fields

### HIPAA Compliance
- [x] Audit logging for all health data access
- [x] Business Associate Agreement
- [x] Encryption requirements
- [x] Access controls
- [x] Data retention policies
- [x] Breach notification procedures

### Privacy
- [x] Data minimization
- [x] Consent management
- [x] Right to deletion (GDPR)
- [x] Right to access (data export)
- [x] PII masking in logs

---

## Deployment Quick Start

### Local Development

```bash
# Prerequisites
git clone <repo>
cd seva-ai

# Setup environment
cp .env.example .env
# Edit .env with your values

# Start services
docker-compose up -d

# Initialize database
docker-compose exec fastapi alembic upgrade head

# Seed data (optional)
docker-compose exec fastapi python scripts/seed_data.py

# Run tests
docker-compose exec fastapi pytest tests/

# Access API
# - API: http://localhost:8000
# - Docs: http://localhost:8000/docs
# - Postgres: localhost:5432
# - Weaviate: http://localhost:8080
# - Redis: localhost:6379
```

### Production Deployment

```bash
# Build Docker image
docker build -t smartai/api:latest backend/

# Push to registry
docker push smartai/api:latest

# Deploy to Kubernetes
kubectl apply -f backend/k8s/

# Verify deployment
kubectl get pods -n smartai
kubectl logs -n smartai -l app=smartai-api

# Check service
kubectl get svc -n smartai
```

---

## Performance Benchmarks & Targets

| Metric | Target | Monitoring |
|--------|--------|------------|
| API Response Time (p95) | < 2 seconds | Application Insights |
| LLM Response Time | < 5 seconds | CloudWatch |
| Embeddings Generation | < 500ms | Prometheus |
| Database Query (p95) | < 100ms | Slow query log |
| Cache Hit Ratio | > 80% | Redis info stats |
| Sync Success Rate | > 99% | Application logs |
| Uptime | > 99.5% | Uptime monitoring |
| Error Rate | < 0.1% | Error tracking |

---

## Monitoring & Observability

### Key Metrics to Track

```python
# Request metrics
smartai_api_requests_total
smartai_api_request_duration_seconds
smartai_api_response_errors_total

# LLM metrics
smartai_llm_tokens_used_total
smartai_llm_api_errors_total
smartai_llm_response_time_seconds

# Database metrics
smartai_db_query_duration_seconds
smartai_db_connection_pool_size
smartai_db_active_connections

# Health metrics
smartai_health_alerts_triggered_total
smartai_anomalies_detected_total
smartai_sync_queue_size

# Business metrics
smartai_active_conversations
smartai_active_users_today
smartai_total_messages_processed
```

### Alert Rules

```yaml
- name: HighErrorRate
  condition: error_rate > 0.001  # 0.1%
  duration: 5m
  severity: critical

- name: HighLatency
  condition: p95_latency > 2000ms
  duration: 5m
  severity: warning

- name: SyncBacklog
  condition: sync_queue_size > 1000
  duration: 10m
  severity: warning

- name: DatabaseDown
  condition: db_connection_error
  duration: 1m
  severity: critical
```

---

## Development Workflow

### Version Control Strategy

```
main (production)
    ↑
    ├── release-v1.0
    │
develop (staging)
    ↑
    ├── feature/voice-improvements
    ├── feature/caregiver-portal
    ├── fix/memory-optimization
    └── chore/dependency-updates
```

### CI/CD Pipeline

```
Push to PR
    ↓
Run Tests (unit + integration)
    ↓
Code Quality Check (SonarQube)
    ↓
Security Scan (SAST)
    ↓
Build Docker Image
    ↓
Deploy to Staging
    ↓
Run E2E Tests
    ↓
Approval Required
    ↓
Deploy to Production
    ↓
Monitor Health
```

### Testing Strategy

```
Unit Tests (pytest)
- Models & schemas: 95%+ coverage
- Services: 85%+ coverage
- Utils: 90%+ coverage

Integration Tests (pytest + TestClient)
- API endpoints
- Database operations
- LLM integration
- Cache behavior

E2E Tests (Cypress/Playwright)
- User registration flow
- Chat functionality
- Offline/online transitions
- Health metric recording

Load Tests (Locust)
- 1000 concurrent users
- Ramp up over 5 minutes
- Hold for 15 minutes
```

---

## Troubleshooting Guide

### Common Issues

**Problem: Embeddings not being generated**
```python
# Check:
1. Weaviate service running: curl http://localhost:8080/v1/meta
2. Model downloaded: check disk space
3. Queue size: SELECT COUNT(*) FROM sync_queue WHERE status='pending'
4. Logs: docker logs smartai_weaviate
```

**Problem: High API latency**
```python
# Diagnose:
1. Check database query time: SELECT * FROM pg_stat_statements
2. Cache hit ratio: redis-cli info stats
3. LLM response time: check CloudWatch logs
4. Network issues: ping to vector DB
```

**Problem: Offline sync conflicts**
```python
# Resolution:
1. Check conflict_detected flag: SELECT * FROM sync_queue WHERE conflict_detected=true
2. Review conflict_resolution_strategy
3. Check timestamps for time-based resolution
4. Manual intervention if needed
```

**Problem: User not receiving alerts**
```sql
-- Check:
SELECT * FROM alerts WHERE user_id = ? AND created_at > NOW() - INTERVAL '1 hour';
SELECT * FROM caregiver_relationships WHERE elderly_user_id = ? AND can_receive_alerts = true;
-- Check notification service logs
```

---

## Cost Optimization Tips

### Infrastructure
- Use spot instances for non-critical workloads
- Right-size database instances based on actual load
- Use CloudFront for static assets
- Implement data compression in APIs
- Archive old logs to cold storage

### API & LLM
- Implement prompt caching for common queries
- Batch embeddings generation
- Use token counting to optimize prompts
- Monitor token usage per user
- Implement fallback responses for cost control

### Database
- Archive data older than 3 years
- Implement partitioning for large tables
- Use read replicas for analytics
- Optimize slow queries regularly

---

## Scaling Considerations

### Horizontal Scaling
```
- API pods: 3 → 20+ (autoscaling)
- Database: Primary → Read replicas
- Cache: Single node → Redis cluster
- Vector DB: Single → Distributed
```

### Vertical Scaling
```
- Increase pod memory: 512MB → 2GB
- Increase pod CPU: 250m → 1000m
- Increase database connections
- Increase vector DB memory
```

### Data Scaling
```
- Current: 100K users → 10M messages/day
- Expected growth: 50% YoY
- Archive strategy: 3-year retention
- Partitioning: By user ID, by date
```

---

## Emergency Procedures

### Database Outage
1. Check database status: `aws rds describe-db-instances`
2. Review CloudWatch metrics for errors
3. Trigger failover to read replica if available
4. Restore from backup if necessary
5. Post-incident review

### API Service Down
1. Check Kubernetes cluster: `kubectl get nodes`
2. Review pod logs: `kubectl logs -f pod/name`
3. Check resource limits: `kubectl top nodes`
4. Restart pods: `kubectl rollout restart deployment/smartai-api`
5. Monitor metrics until stable

### Security Incident
1. Disable affected user accounts
2. Rotate compromised API keys
3. Review audit logs for suspicious activity
4. Notify affected users if data exposed
5. Post-incident security review

---

## Key Files & Locations

```
/home/grao/Projects/seva-ai/
├── ARCHITECTURE.md                 ← Main architecture doc
├── IMPLEMENTATION_GUIDE.md         ← Step-by-step implementation
├── DATABASE_SETUP.md               ← Database initialization
├── TECHNICAL_SUMMARY.md            ← This file
│
├── backend/
│   ├── app/
│   │   ├── main.py                 ← FastAPI app entry
│   │   ├── config.py               ← Configuration
│   │   ├── api/v1/
│   │   ├── services/
│   │   ├── models/
│   │   └── db/
│   ├── requirements.txt
│   ├── Dockerfile
│   ├── alembic/                    ← Database migrations
│   ├── tests/
│   └── scripts/
│
├── mobile/
│   ├── src/
│   │   ├── App.tsx
│   │   ├── screens/
│   │   ├── services/
│   │   ├── components/
│   │   └── redux/
│   ├── package.json
│   └── app.json
│
└── k8s/                             ← Kubernetes manifests
    ├── deployment.yaml
    ├── service.yaml
    ├── ingress.yaml
    └── configmap.yaml
```

---

## Useful Commands

### PostgreSQL
```sql
-- Connect
psql postgresql://smartai:password@localhost:5432/smartai

-- Useful queries
\dt              -- List tables
\d table_name    -- Describe table
SELECT * FROM information_schema.tables WHERE table_schema='public';
```

### Weaviate
```bash
# Check status
curl http://localhost:8080/v1/meta

# Query examples
curl http://localhost:8080/v1/graphql -X POST \
  -H 'Content-Type: application/json' \
  -d '{...query...}'
```

### FastAPI
```bash
# Run development server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Run tests
pytest tests/ -v --cov=app

# Generate API docs
openapi-generator-cli generate -i http://localhost:8000/openapi.json -g python
```

### Redis
```bash
# Connect
redis-cli -h localhost -p 6379

# Check keys
KEYS *
DBSIZE

# Monitor traffic
MONITOR

# Check memory
INFO memory
```

### Docker
```bash
# Build image
docker build -t smartai/api:latest backend/

# Run container
docker run -p 8000:8000 --env-file .env smartai/api:latest

# View logs
docker logs container_id -f

# Stop services
docker-compose down -v
```

### Kubernetes
```bash
# Deploy
kubectl apply -f k8s/

# Check status
kubectl get pods -n smartai
kubectl get svc -n smartai

# View logs
kubectl logs -n smartai -l app=smartai-api

# Scale
kubectl scale deployment smartai-api -n smartai --replicas=5

# Update
kubectl set image deployment/smartai-api api=smartai/api:v1.1 -n smartai
```

---

## Quick Checklists

### Pre-Launch Checklist
- [ ] Database backups configured
- [ ] Monitoring & alerting active
- [ ] SSL certificates valid
- [ ] API rate limiting enabled
- [ ] Auth tokens secure
- [ ] Encryption keys in KMS
- [ ] Audit logging enabled
- [ ] Disaster recovery plan tested
- [ ] Load testing passed
- [ ] Security audit completed
- [ ] User documentation ready
- [ ] Support team trained

### Daily Operations
- [ ] Monitor error rates
- [ ] Check database performance
- [ ] Review alert logs
- [ ] Verify backup completion
- [ ] Check API health metrics
- [ ] Monitor LLM API costs
- [ ] Review user feedback

### Weekly Review
- [ ] Performance analytics
- [ ] Security scan results
- [ ] User growth metrics
- [ ] Feature usage analytics
- [ ] Infrastructure costs
- [ ] Team capacity planning

---

## Resources & References

### Documentation
- PostgreSQL: https://www.postgresql.org/docs/15/
- Weaviate: https://weaviate.io/developers/
- FastAPI: https://fastapi.tiangolo.com/
- React Native: https://reactnative.dev/
- Claude API: https://docs.anthropic.com/

### Standards & Guidelines
- HIPAA Security Rule: https://www.hhs.gov/hipaa/
- OWASP Top 10: https://owasp.org/Top10/
- REST API Best Practices: https://restfulapi.net/
- OpenAPI Specification: https://swagger.io/specification/

### Tools
- Postman: API testing
- DataGrip: Database IDE
- AWS Console: Cloud management
- Grafana: Metrics visualization
- PagerDuty: Incident management

---

## Getting Help

For questions or issues:

1. **Documentation:** Check ARCHITECTURE.md, IMPLEMENTATION_GUIDE.md
2. **Troubleshooting:** Review this TECHNICAL_SUMMARY.md
3. **Database:** See DATABASE_SETUP.md
4. **Code Examples:** Check IMPLEMENTATION_GUIDE.md
5. **Team:** Contact the development team

---

**Document Version:** 1.0
**Last Updated:** January 15, 2024
**Status:** Ready for Development
**Next Review:** Post-MVP Launch
