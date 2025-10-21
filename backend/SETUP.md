# Backend Setup Guide

Quick guide to get the Smart AI backend running locally.

## Prerequisites

- Python 3.11+
- Docker & Docker Compose (for databases)
- PostgreSQL 15+ (or use Docker)

## Quick Start

### 1. Start Infrastructure Services

```bash
# From project root
docker-compose -f infrastructure/docker/docker-compose.dev.yml up -d

# Verify services are running
docker ps --filter name=seva-
```

This starts:
- PostgreSQL (localhost:5432)
- Weaviate (localhost:8080)
- Redis (localhost:6379)
- Adminer (localhost:8081) - Database UI

### 2. Setup Python Environment

```bash
cd ../../backend

# Create virtual environment
python3.11 -m venv venv

# Activate it
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

### 3. Configure Environment

```bash
# Copy environment template
cp .env.example .env

# Edit .env and add your API keys:
# - ANTHROPIC_API_KEY (for Claude)
# - OPENAI_API_KEY (for embeddings)
# - SECRET_KEY (generate with: openssl rand -hex 32)
```

### 4. Database Setup

**Note:** The database is already initialized with all tables! You can skip this step.

If you need to recreate the database:

```bash
# Run database migrations
alembic upgrade head

# Or use the SQL script directly
docker exec -i seva-postgres psql -U seva_user -d seva_ai < ../database/postgresql/schemas/001_init.sql
```

**Create Test User:**

```bash
# Create test user (test@smartai.com / TestPass123!)
docker exec -i seva-postgres psql -U seva_user -d seva_ai < create_test_user.sql
```

**Verify in Adminer:** http://localhost:8081
- Server: `seva-postgres`
- Username: `seva_user`
- Password: `seva_password`
- Database: `seva_ai`

### 5. Run the Server

```bash
# Development mode (with auto-reload)
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Or use the module directly
python -m app.main
```

### 6. Test the API

Visit: http://localhost:8000/docs

You should see the interactive API documentation with:
- Health check endpoints
- Authentication endpoints (register, login, refresh)
- Chat endpoints (send message, get sessions)

## Testing the Flow

### 1. Register a User

```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "testpass123",
    "full_name": "Test User"
  }'
```

### 2. Login

```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "testpass123"
  }'
```

Save the `access_token` from the response.

### 3. Send a Chat Message

```bash
curl -X POST http://localhost:8000/api/v1/chat/send \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{
    "message": "Hello! How are you today?"
  }'
```

## Running Tests

```bash
# Run all tests
pytest

# With coverage
pytest --cov=app --cov-report=html

# Watch mode
pytest -f

# Specific test file
pytest tests/test_auth.py -v
```

## Code Quality

```bash
# Format code
black app/ tests/

# Lint
ruff check app/ tests/

# Type check
mypy app/

# All checks
black app/ && ruff check app/ && mypy app/ && pytest
```

## Common Issues

### Database Connection Error

```
sqlalchemy.exc.OperationalError: could not connect to server
```

**Solution:** Make sure Docker services are running:
```bash
cd infrastructure/docker
docker-compose -f docker-compose.dev.yml up -d
```

### Claude API Error

```
Failed to generate AI response: api_key_invalid
```

**Solution:** Add your Anthropic API key to `.env`:
```
ANTHROPIC_API_KEY=sk-ant-...
```

### Migration Errors

```
alembic.util.exc.CommandError: Target database is not up to date
```

**Solution:**
```bash
# Check current version
alembic current

# Upgrade to latest
alembic upgrade head

# If needed, reset and recreate
alembic downgrade base
alembic upgrade head
```

## Database Management

### View Database

Adminer UI: http://localhost:8081

### Run SQL Manually

```bash
# Connect to PostgreSQL
docker exec -it seva-postgres psql -U seva_user -d seva_ai

# Or use Adminer web UI
```

### Create New Migration

```bash
# After modifying models in app/models/
alembic revision --autogenerate -m "Description of changes"

# Review the generated migration in alembic/versions/
# Then apply it
alembic upgrade head
```

### Rollback Migration

```bash
# Rollback one migration
alembic downgrade -1

# Rollback to specific version
alembic downgrade <revision_id>

# Rollback all
alembic downgrade base
```

## Development Workflow

1. **Make changes** to code
2. **Format** with `black app/`
3. **Lint** with `ruff check app/`
4. **Type check** with `mypy app/`
5. **Test** with `pytest`
6. **Commit** changes

## Next Steps

- Add tests for your endpoints in `tests/`
- Implement health monitoring endpoints
- Add voice service integration
- Configure rate limiting
- Setup monitoring (Prometheus metrics)

## Useful Commands

```bash
# View logs
docker-compose -f infrastructure/docker/docker-compose.dev.yml logs -f

# Restart services
docker-compose -f infrastructure/docker/docker-compose.dev.yml restart

# Stop all services
docker-compose -f infrastructure/docker/docker-compose.dev.yml down

# Clean up (WARNING: deletes data)
docker-compose -f infrastructure/docker/docker-compose.dev.yml down -v
```

## Production Deployment

See `../infrastructure/README.md` for Kubernetes deployment instructions.

## Support

- Documentation: `../docs/`
- Issues: GitHub Issues
- Questions: GitHub Discussions
