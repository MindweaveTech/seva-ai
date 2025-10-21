# Smart AI - Test Plan

**Project:** Smart AI - AI-Powered Elderly Care Companion
**Version:** 1.0
**Last Updated:** 2025-10-21

---

## Testing Strategy

### Testing Pyramid

```
           /\
          /  \
         / E2E \          ← 10% (Critical user flows)
        /______\
       /        \
      /Integration\       ← 30% (API + DB + Services)
     /____________\
    /              \
   /  Unit Tests    \    ← 60% (Models, Utils, Services)
  /__________________\
```

### Coverage Targets

| Component | Target Coverage | Priority |
|-----------|----------------|----------|
| Backend | 90%+ | P0 |
| Mobile App | 85%+ | P1 |
| Admin Dashboard | 85%+ | P2 |

---

## Backend Test Plan

### 1. Authentication Tests

**File:** `backend/tests/test_auth.py`
**Priority:** P0 (Critical)
**Estimated Time:** 2 hours

**Test Cases:**

| Test | Description | Expected Result |
|------|-------------|-----------------|
| `test_register_user_success` | Register with valid data | 201, user object, password hashed, profile created |
| `test_register_duplicate_email` | Register with existing email | 400, "Email already registered" |
| `test_login_success` | Login with valid credentials | 200, access_token, refresh_token, last_login updated |
| `test_login_invalid_credentials` | Login with wrong password | 401, "Incorrect email or password" |
| `test_login_inactive_user` | Login with is_active=False | 403, "Inactive user account" |
| `test_refresh_token_success` | Refresh with valid refresh_token | 200, new tokens |
| `test_refresh_token_invalid` | Refresh with invalid token | 401, error |
| `test_get_current_user` | Get /auth/me with valid token | 200, user with profile |
| `test_get_current_user_unauthorized` | Get /auth/me without token | 401, error |
| `test_logout` | Logout endpoint | 200, success message |

---

### 2. Chat Tests

**File:** `backend/tests/test_chat.py`
**Priority:** P0 (Critical)
**Estimated Time:** 3 hours

**Test Cases:**

| Test | Description | Expected Result |
|------|-------------|-----------------|
| `test_send_message_new_session` | Send message without session_id | Creates session, returns user + AI messages, both saved to DB |
| `test_send_message_existing_session` | Send message with session_id | Adds to existing session, message_count incremented |
| `test_send_message_unauthorized` | Send without auth token | 401, error |
| `test_get_sessions_list` | Get /chat/sessions | Paginated sessions, ordered by started_at DESC |
| `test_get_session_with_messages` | Get /chat/sessions/{id} | Session with messages array, ordered by created_at |
| `test_get_session_not_found` | Get session with invalid ID | 404, error |
| `test_get_session_unauthorized_user` | Get session of different user | 404, error |
| `test_delete_session_success` | Delete session | 200, session + messages deleted (cascade) |
| `test_delete_session_not_found` | Delete invalid session | 404, error |
| `test_claude_api_integration` | Mock Claude API call | Verify request format, response handling |
| `test_conversation_context` | Send 3+ messages | Verify history passed to Claude, max 10 messages |
| `test_message_pagination` | Get sessions with page params | Correct page, page_size, total |

---

### 3. Database Model Tests

**File:** `backend/tests/test_models.py`
**Priority:** P1 (High)
**Estimated Time:** 1.5 hours

**Test Cases:**

| Test | Description | Expected Result |
|------|-------------|-----------------|
| `test_user_model_creation` | Create User with required fields | Defaults: is_active=True, role='user' |
| `test_user_profile_relationship` | Access User.profile | Returns UserProfile, cascade delete works |
| `test_conversation_session_model` | Create ConversationSession | message_count defaults to 0 |
| `test_chat_message_model` | Create ChatMessage | Trigger increments session.message_count |
| `test_password_not_exposed` | Serialize User | password_hash not in JSON |
| `test_cascade_delete` | Delete User | Profile, sessions, messages deleted |

---

### 4. Security Tests

**File:** `backend/tests/test_security.py`
**Priority:** P0 (Critical)
**Estimated Time:** 2 hours

**Test Cases:**

| Test | Description | Expected Result |
|------|-------------|-----------------|
| `test_password_hashing` | Hash same password twice | Different hashes (bcrypt salt) |
| `test_password_verification` | Verify correct password | Returns True |
| `test_jwt_token_generation` | Create access token | Contains user_id, exp, type='access' |
| `test_jwt_refresh_token` | Create refresh token | Longer expiry, type='refresh' |
| `test_jwt_token_expiration` | Use expired token | 401, error |
| `test_jwt_token_invalid_signature` | Use tampered token | 401, error |
| `test_sql_injection_protection` | SQL injection in email field | Safely escaped, no execution |
| `test_xss_protection` | XSS in message content | Sanitized or rejected |

---

### 5. Integration Tests

**File:** `backend/tests/integration/test_e2e_flow.py`
**Priority:** P1 (High)
**Estimated Time:** 2 hours

**Test Cases:**

| Test | Description | Flow |
|------|-------------|------|
| `test_complete_user_journey` | Full user flow | Register → Login → Send message → Get sessions → Get session → Logout |
| `test_token_refresh_flow` | Token expiry handling | Login → Wait/mock expiry → Request → Auto-refresh → Success |
| `test_conversation_flow` | Multi-message conversation | New session → Send 5 messages → Verify history → Verify Claude context |

---

## Mobile Test Plan

### 6. API Service Tests

**File:** `mobile-app/__tests__/services/auth.test.ts`
**Priority:** P1 (High)
**Estimated Time:** 2 hours

**Test Cases:**

| Test | Description | Expected Result |
|------|-------------|-----------------|
| `test_auth_service_login` | Call login with credentials | Tokens stored in AsyncStorage |
| `test_auth_service_register` | Call register | API called with correct data |
| `test_auth_service_logout` | Call logout | Tokens cleared from AsyncStorage |
| `test_auth_service_get_current_user` | Get current user | User cached in AsyncStorage |
| `test_api_client_auto_refresh` | Mock 401 response | Refresh token called, original request retried |

---

### 7. State Management Tests

**File:** `mobile-app/__tests__/store/authStore.test.ts`
**Priority:** P1 (High)
**Estimated Time:** 1.5 hours

**Test Cases:**

| Test | Description | Expected Result |
|------|-------------|-----------------|
| `test_auth_store_login` | Call login action | user state updated, isAuthenticated=true |
| `test_auth_store_logout` | Call logout action | State cleared |
| `test_auth_store_error_handling` | Mock API error | Error state set, user null |
| `test_chat_store_send_message` | Send message action | Message added to state |
| `test_chat_store_load_sessions` | Load sessions action | Sessions array populated |

---

### 8. Component Tests (After UI)

**File:** `mobile-app/__tests__/screens/LoginScreen.test.tsx`
**Priority:** P2 (Medium)
**Estimated Time:** 2 hours

**Test Cases:**

| Test | Description | Expected Result |
|------|-------------|-----------------|
| `test_login_screen_renders` | Render LoginScreen | Email, password fields, submit button visible |
| `test_login_form_validation` | Submit with empty fields | Validation errors shown |
| `test_login_submit_success` | Submit valid credentials | Navigate to Chat screen |
| `test_login_submit_error` | Submit invalid credentials | Error message displayed |
| `test_navigation_to_register` | Click "Register" link | Navigate to Register screen |

---

## Manual Testing Checklist

### Backend API Testing (via Swagger UI)

**Setup:**
- [ ] Start Docker services: `docker-compose up -d`
- [ ] Run migrations: `alembic upgrade head`
- [ ] Start backend: `uvicorn app.main:app --reload`
- [ ] Open: http://localhost:8000/docs

**Tests:**
- [ ] POST /api/v1/auth/register - Create test user
- [ ] POST /api/v1/auth/login - Login (save token)
- [ ] GET /api/v1/auth/me - Get current user (with token)
- [ ] POST /api/v1/chat/send - Send message (with token)
- [ ] GET /api/v1/chat/sessions - List sessions (with token)
- [ ] GET /api/v1/chat/sessions/{id} - Get session with messages
- [ ] DELETE /api/v1/chat/sessions/{id} - Delete session
- [ ] POST /api/v1/auth/logout - Logout

**Verification:**
- [ ] Check Adminer (http://localhost:8081) for DB entries
- [ ] Verify password is hashed in users table
- [ ] Verify messages saved in chat_messages table
- [ ] Verify session message_count increments

**Estimated Time:** 30 minutes

---

### Mobile App Testing (After UI)

**Setup:**
- [ ] Backend running on http://localhost:8000
- [ ] npm install dependencies
- [ ] Update .env with API_URL
- [ ] npm start (Expo)

**Tests:**
- [ ] Test registration flow
- [ ] Test login flow
- [ ] Test send message (new session)
- [ ] Test send message (existing session)
- [ ] Test view sessions list
- [ ] Test open session with history
- [ ] Test delete session
- [ ] Test logout
- [ ] Test token auto-refresh (wait 30 min or mock)
- [ ] Test offline message queue

**Estimated Time:** 1 hour

---

## Test Execution Commands

### Backend

```bash
# Install dependencies
cd backend
pip install -r requirements-dev.txt

# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html --cov-report=term

# Run specific test file
pytest tests/test_auth.py -v

# Run specific test
pytest tests/test_auth.py::test_login_success -v

# Run with markers
pytest -m "auth" -v

# Generate HTML coverage report
pytest --cov=app --cov-report=html
# Open htmlcov/index.html in browser
```

### Mobile

```bash
# Install dependencies
cd mobile-app
npm install

# Run all tests
npm test

# Run with coverage
npm run test:coverage

# Run in watch mode
npm run test:watch

# Run specific file
npm test -- auth.test.ts

# Update snapshots
npm test -- -u
```

---

## Test Data & Fixtures

### Backend Fixtures

**File:** `backend/tests/conftest.py`

```python
import pytest
from app.db.session import AsyncSessionLocal
from app.models.user import User
from app.core.security import get_password_hash, create_access_token

@pytest.fixture
async def db_session():
    """Async database session for tests."""
    async with AsyncSessionLocal() as session:
        yield session
        await session.rollback()

@pytest.fixture
def test_user_data():
    """Test user data."""
    return {
        "email": "test@example.com",
        "password": "testpass123",
        "full_name": "Test User"
    }

@pytest.fixture
async def test_user(db_session, test_user_data):
    """Create test user in database."""
    user = User(
        email=test_user_data["email"],
        full_name=test_user_data["full_name"],
        password_hash=get_password_hash(test_user_data["password"])
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    return user

@pytest.fixture
def auth_headers(test_user):
    """Authentication headers with valid token."""
    token = create_access_token(test_user.id)
    return {"Authorization": f"Bearer {token}"}
```

### Mobile Fixtures

**File:** `mobile-app/__tests__/fixtures/user.ts`

```typescript
export const mockUser = {
  id: "123e4567-e89b-12d3-a456-426614174000",
  email: "test@example.com",
  full_name: "Test User",
  role: "user",
  is_active: true,
  is_verified: false,
  created_at: "2025-10-21T00:00:00Z",
  last_login_at: null,
  profile: null,
};

export const mockTokens = {
  access_token: "mock_access_token",
  refresh_token: "mock_refresh_token",
  token_type: "bearer",
};
```

---

## Priority-Based Execution Plan

### Minimal Viable Testing (6.5 hours)

**P0 - Critical (Must Have):**
1. Backend auth tests - 2h
2. Backend chat tests - 2h
3. Security tests - 2h
4. Manual API testing - 0.5h

### Comprehensive Testing (12 hours)

**P1 - High (Should Have):**
1. Database model tests - 1.5h
2. Integration E2E tests - 2h
3. Mobile service tests - 2h

### Full Coverage (16 hours)

**P2 - Medium (Nice to Have):**
1. Mobile UI tests - 2h
2. Performance tests - 1h
3. Load testing - 1h

---

## CI/CD Integration

### GitHub Actions

Tests run automatically on:
- Every push to main/develop
- Every pull request
- Before deployment

**Workflows:**
- `.github/workflows/backend-ci.yml` - Backend tests
- `.github/workflows/mobile-ci.yml` - Mobile tests
- `.github/workflows/dashboard-ci.yml` - Dashboard tests

**Coverage Enforcement:**
- Fail build if coverage < 85%
- Upload coverage to Codecov
- Comment coverage report on PRs

---

## Performance Testing Plan

### Load Testing (Future - Phase 3)

**Tool:** Locust or K6

**Scenarios:**
- 100 concurrent users
- 1,000 messages per minute
- Token refresh under load
- Database connection pooling

**Performance Targets:**
- API p95 response time < 500ms
- API p99 response time < 1000ms
- Support 10,000 daily active users
- Database queries < 100ms (p95)

---

## Security Testing Plan

### Automated Security Scans

- [ ] **Dependabot** - Vulnerable dependencies
- [ ] **Bandit** - Python SAST
- [ ] **ESLint Security** - TypeScript SAST
- [ ] **Secret Scanning** - Detect committed secrets
- [ ] **SQL Injection Testing** - SQLMap
- [ ] **API Fuzzing** - Postman/Newman

### Manual Security Review

- [ ] OWASP Top 10 checklist
- [ ] Authentication security review
- [ ] Authorization checks
- [ ] Input validation review
- [ ] HIPAA compliance verification

---

## Test Maintenance

### When to Update Tests

- [ ] After adding new features
- [ ] After bug fixes
- [ ] After refactoring
- [ ] Before major releases

### Test Quality Guidelines

- Tests should be fast (< 5s per test)
- Tests should be independent
- Tests should be deterministic
- Test names should be descriptive
- Use arrange-act-assert pattern

---

**Version:** 1.0
**Status:** Plan created, not yet executed
**Next Action:** Execute P0 tests or continue with UI development
