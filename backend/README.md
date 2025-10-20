# Smart AI - Backend Service

FastAPI-based backend service for the Smart AI elderly care companion system.

## Overview

The backend service handles:
- User authentication and authorization
- Chat message processing and Claude API integration
- RAG (Retrieval-Augmented Generation) pipeline for memory
- Health monitoring and pattern detection
- Voice service integration (STT/TTS)
- Caregiver alerts and notifications

## Tech Stack

- **Framework:** FastAPI 0.104+
- **Language:** Python 3.11+
- **ORM:** SQLAlchemy 2.0+ (async)
- **Validation:** Pydantic v2
- **Database:** PostgreSQL 15+
- **Vector DB:** Weaviate
- **Cache:** Redis (optional)
- **Testing:** Pytest, pytest-asyncio

## Project Structure

```
backend/
├── app/
│   ├── api/                # API endpoints
│   │   ├── v1/
│   │   │   ├── auth.py
│   │   │   ├── chat.py
│   │   │   ├── health.py
│   │   │   ├── users.py
│   │   │   └── voice.py
│   │   └── deps.py         # Dependencies (auth, db)
│   ├── core/               # Core configuration
│   │   ├── config.py
│   │   ├── security.py
│   │   └── logging.py
│   ├── models/             # SQLAlchemy models
│   │   ├── user.py
│   │   ├── conversation.py
│   │   └── health.py
│   ├── schemas/            # Pydantic schemas
│   │   ├── user.py
│   │   ├── chat.py
│   │   └── health.py
│   ├── services/           # Business logic
│   │   ├── auth.py
│   │   ├── chat.py
│   │   ├── rag.py
│   │   ├── health.py
│   │   └── voice.py
│   ├── utils/              # Helper functions
│   │   ├── embeddings.py
│   │   ├── prompts.py
│   │   └── validators.py
│   ├── db/                 # Database utilities
│   │   ├── base.py
│   │   └── session.py
│   └── main.py             # FastAPI application
├── tests/
│   ├── unit/
│   ├── integration/
│   └── conftest.py
├── alembic/                # Database migrations
│   ├── versions/
│   └── env.py
├── requirements.txt        # Python dependencies
├── requirements-dev.txt    # Development dependencies
├── .env.example            # Environment variables template
├── Dockerfile
└── README.md
```

## Getting Started

### Prerequisites

- Python 3.11+
- PostgreSQL 15+
- Weaviate (or Docker)
- Redis (optional, for caching)

### Installation

1. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt  # For development
   ```

3. **Setup environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

4. **Run database migrations**
   ```bash
   alembic upgrade head
   ```

5. **Start development server**
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

   API will be available at: http://localhost:8000
   Interactive docs: http://localhost:8000/docs

### Environment Variables

Required variables in `.env`:

```env
# Database
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/seva_ai

# Weaviate
WEAVIATE_URL=http://localhost:8080

# Redis (optional)
REDIS_URL=redis://localhost:6379/0

# Security
SECRET_KEY=your-secret-key-here
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# Claude API
ANTHROPIC_API_KEY=your-claude-api-key

# OpenAI (for embeddings)
OPENAI_API_KEY=your-openai-api-key

# Google Cloud (for voice)
GOOGLE_APPLICATION_CREDENTIALS=/path/to/credentials.json

# Application
ENVIRONMENT=development
DEBUG=True
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:19006
```

## Development

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/unit/test_auth.py

# Run with verbose output
pytest -v
```

### Code Formatting

```bash
# Format code
black app/ tests/

# Check formatting
black --check app/ tests/

# Sort imports
isort app/ tests/
```

### Linting

```bash
# Run linter
ruff check app/ tests/

# Fix auto-fixable issues
ruff check --fix app/ tests/
```

### Type Checking

```bash
mypy app/
```

### Database Migrations

```bash
# Create new migration
alembic revision --autogenerate -m "Description of changes"

# Apply migrations
alembic upgrade head

# Rollback one migration
alembic downgrade -1

# View migration history
alembic history
```

## API Documentation

### Authentication

**Register**
```bash
POST /api/v1/auth/register
{
  "email": "user@example.com",
  "password": "secure_password",
  "full_name": "John Doe"
}
```

**Login**
```bash
POST /api/v1/auth/login
{
  "email": "user@example.com",
  "password": "secure_password"
}
```

**Refresh Token**
```bash
POST /api/v1/auth/refresh
{
  "refresh_token": "your-refresh-token"
}
```

### Chat

**Send Message**
```bash
POST /api/v1/chat/messages
Authorization: Bearer <token>
{
  "session_id": "uuid",
  "message": "How are you today?"
}
```

**Stream Message (WebSocket)**
```bash
WS /api/v1/chat/stream
Authorization: Bearer <token>
```

### Health Monitoring

**Log Health Metric**
```bash
POST /api/v1/health/metrics
Authorization: Bearer <token>
{
  "metric_type": "blood_pressure",
  "value": {"systolic": 120, "diastolic": 80}
}
```

For complete API documentation, visit: http://localhost:8000/docs

## Architecture

### RAG Pipeline

```
User Message
    ↓
Generate Embedding (OpenAI)
    ↓
Semantic Search (Weaviate)
    ↓
Retrieve Relevant Context
    ↓
Construct Prompt with Context
    ↓
Send to Claude API
    ↓
Stream Response
    ↓
Store Message + Embedding
```

### Health Monitoring Flow

```
Chat Message
    ↓
Sentiment Analysis
    ↓
Extract Health Signals
    ↓
Pattern Detection
    ↓
Anomaly Detection
    ↓
Generate Alert (if needed)
    ↓
Notify Caregiver
```

## Performance

### Targets
- API response time (p95): <500ms
- API response time (p99): <1000ms
- Database query time: <100ms
- RAG retrieval time: <200ms
- Claude API call: <2000ms (streaming)

### Optimization Tips
- Use connection pooling for database
- Cache frequently accessed data in Redis
- Use async/await for I/O operations
- Batch embedding generation
- Optimize database indexes

## Testing

### Test Coverage Requirements
- Overall coverage: 90%+
- Critical paths (auth, health): 95%+
- Unit tests for all services
- Integration tests for API endpoints
- Load tests for production readiness

### Example Test

```python
import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_register_user():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            "/api/v1/auth/register",
            json={
                "email": "test@example.com",
                "password": "password123",
                "full_name": "Test User"
            }
        )
    assert response.status_code == 201
    assert "access_token" in response.json()
```

## Deployment

### Docker

```bash
# Build image
docker build -t seva-ai-backend .

# Run container
docker run -p 8000:8000 --env-file .env seva-ai-backend
```

### Kubernetes

See `../infrastructure/kubernetes/backend/` for K8s manifests.

```bash
kubectl apply -f ../infrastructure/kubernetes/backend/
```

## Monitoring

### Health Checks

```bash
# Liveness probe
GET /health

# Readiness probe
GET /health/ready

# Detailed status
GET /health/detailed
```

### Metrics

Prometheus metrics available at: `/metrics`

Key metrics:
- `http_requests_total` - Total HTTP requests
- `http_request_duration_seconds` - Request duration
- `db_query_duration_seconds` - Database query duration
- `claude_api_calls_total` - Claude API usage
- `rag_retrieval_duration_seconds` - RAG retrieval time

## Troubleshooting

### Common Issues

**Database connection errors**
- Check DATABASE_URL in .env
- Ensure PostgreSQL is running
- Verify database exists

**Claude API errors**
- Check ANTHROPIC_API_KEY is valid
- Verify API rate limits
- Check internet connectivity

**Weaviate connection errors**
- Ensure Weaviate is running
- Check WEAVIATE_URL
- Verify schema is initialized

**Import errors**
- Ensure virtual environment is activated
- Check all dependencies installed: `pip install -r requirements.txt`

## Contributing

1. Create a feature branch
2. Write tests for new features
3. Ensure all tests pass
4. Format code with Black
5. Submit pull request

## License

MIT License - see LICENSE file for details
