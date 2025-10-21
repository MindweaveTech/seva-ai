# Smart AI - Testing Plan & Report

**Project:** Smart AI - AI-Powered Elderly Care Companion
**Last Updated:** 2025-10-21
**Status:** Phase 1 Testing Plan

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

| Component | Target Coverage | Current Status |
|-----------|----------------|----------------|
| Backend | 90%+ | 🔴 0% |
| Mobile App | 85%+ | 🔴 0% |
| Admin Dashboard | 85%+ | 🔴 0% |
| **Overall** | **85%+** | **🔴 0%** |

---

## Phase 1: Minimal Test Plan

### Backend Testing (Priority: HIGH)

#### 1.1 Authentication Tests

**File:** `backend/tests/test_auth.py`

**Test Cases:**

```python
✅ test_register_user_success
   - Valid email, password, name
   - Returns 201 and user object
   - Password is hashed
   - Profile is created

✅ test_register_duplicate_email
   - Returns 400
   - Error message: "Email already registered"

✅ test_login_success
   - Valid credentials
   - Returns access_token and refresh_token
   - Last login updated

✅ test_login_invalid_credentials
   - Wrong password
   - Returns 401
   - Error message: "Incorrect email or password"

✅ test_login_inactive_user
   - User.is_active = False
   - Returns 403
   - Error message: "Inactive user account"

✅ test_refresh_token_success
   - Valid refresh token
   - Returns new access_token and refresh_token

✅ test_refresh_token_invalid
   - Invalid/expired token
   - Returns 401

✅ test_get_current_user
   - Valid access token
   - Returns user with profile

✅ test_get_current_user_unauthorized
   - No token or invalid token
   - Returns 401

✅ test_logout
   - Returns success message
```

**Status:** 🔴 Not Started
**Priority:** P0 (Critical)
**Estimated Time:** 2 hours

---

#### 1.2 Chat Tests

**File:** `backend/tests/test_chat.py`

**Test Cases:**

```python
✅ test_send_message_new_session
   - Send message without session_id
   - Creates new session
   - Returns user message and AI response
   - Both messages saved to DB

✅ test_send_message_existing_session
   - Send message with session_id
   - Adds to existing session
   - Message count incremented

✅ test_send_message_unauthorized
   - No auth token
   - Returns 401

✅ test_get_sessions_list
   - Returns paginated sessions
   - Ordered by started_at DESC

✅ test_get_session_with_messages
   - Returns session with messages array
   - Messages ordered by created_at

✅ test_get_session_not_found
   - Invalid session_id
   - Returns 404

✅ test_get_session_unauthorized_user
   - Session belongs to different user
   - Returns 404

✅ test_delete_session_success
   - Deletes session and all messages (cascade)
   - Returns success

✅ test_delete_session_not_found
   - Returns 404

✅ test_claude_api_integration
   - Mock Claude API
   - Verify request format
   - Verify response handling

✅ test_conversation_context
   - Send 3 messages in session
   - Verify history is passed to Claude
   - Max 10 messages in context
```

**Status:** 🔴 Not Started
**Priority:** P0 (Critical)
**Estimated Time:** 3 hours

---

#### 1.3 Database Tests

**File:** `backend/tests/test_models.py`

**Test Cases:**

```python
✅ test_user_model_creation
   - Create user with required fields
   - Verify defaults (is_active=True, role='user')

✅ test_user_profile_relationship
   - User.profile returns UserProfile
   - Cascade delete works

✅ test_conversation_session_model
   - Create session
   - Verify message_count defaults to 0

✅ test_chat_message_model
   - Create message
   - Verify trigger increments session.message_count

✅ test_password_not_exposed
   - User model doesn't expose password_hash in serialization

✅ test_cascade_delete
   - Delete user
   - Verify profile, sessions, messages deleted
```

**Status:** 🔴 Not Started
**Priority:** P1 (High)
**Estimated Time:** 1.5 hours

---

#### 1.4 Security Tests

**File:** `backend/tests/test_security.py`

**Test Cases:**

```python
✅ test_password_hashing
   - Verify bcrypt is used
   - Same password → different hashes

✅ test_jwt_token_generation
   - Access token contains user_id and type
   - Refresh token has longer expiry

✅ test_jwt_token_expiration
   - Expired token returns 401

✅ test_jwt_token_invalid_signature
   - Tampered token returns 401

✅ test_sql_injection_protection
   - Try SQL injection in email field
   - Should be safely escaped

✅ test_xss_protection
   - Try XSS in message content
   - Should be sanitized

✅ test_rate_limiting (future)
   - Too many requests → 429
```

**Status:** 🔴 Not Started
**Priority:** P0 (Critical)
**Estimated Time:** 2 hours

---

### Mobile App Testing (Priority: MEDIUM)

#### 2.1 API Service Tests

**File:** `mobile-app/__tests__/services/auth.test.ts`

**Test Cases:**

```typescript
✅ test_auth_service_login
   - Mock axios response
   - Verify tokens stored in AsyncStorage

✅ test_auth_service_register
   - Verify API called with correct data

✅ test_auth_service_logout
   - Verify tokens cleared from AsyncStorage

✅ test_auth_service_get_current_user
   - Verify user cached in AsyncStorage

✅ test_api_client_auto_refresh
   - Mock 401 response
   - Verify refresh token called
   - Verify original request retried
```

**Status:** 🔴 Not Started
**Priority:** P1 (High)
**Estimated Time:** 2 hours

---

#### 2.2 State Management Tests

**File:** `mobile-app/__tests__/store/authStore.test.ts`

**Test Cases:**

```typescript
✅ test_auth_store_login
   - Call login action
   - Verify user state updated
   - Verify isAuthenticated = true

✅ test_auth_store_logout
   - Call logout action
   - Verify state cleared

✅ test_auth_store_error_handling
   - Mock API error
   - Verify error state set
```

**Status:** 🔴 Not Started
**Priority:** P1 (High)
**Estimated Time:** 1.5 hours

---

#### 2.3 Component Tests (After UI is built)

**File:** `mobile-app/__tests__/screens/LoginScreen.test.tsx`

**Test Cases:**

```typescript
✅ test_login_screen_renders
✅ test_login_form_validation
✅ test_login_submit_success
✅ test_login_submit_error
✅ test_navigation_to_register
```

**Status:** 🔴 Not Started (Waiting for UI)
**Priority:** P2 (Medium)
**Estimated Time:** 2 hours

---

### Integration Tests (Priority: MEDIUM)

#### 3.1 End-to-End API Flow

**File:** `backend/tests/integration/test_e2e_flow.py`

**Test Cases:**

```python
✅ test_complete_user_journey
   1. Register user
   2. Login
   3. Send message
   4. Get sessions
   5. Get session with messages
   6. Logout

✅ test_token_refresh_flow
   1. Login
   2. Wait for token expiry (or mock it)
   3. Make authenticated request
   4. Verify auto-refresh works

✅ test_conversation_flow
   1. Start new session
   2. Send 5 messages
   3. Verify conversation history works
   4. Verify Claude gets context
```

**Status:** 🔴 Not Started
**Priority:** P1 (High)
**Estimated Time:** 2 hours

---

### Manual Testing Checklist

#### Backend API (via Swagger UI)

- [ ] Start Docker services
- [ ] Run migrations
- [ ] Start backend server
- [ ] Open http://localhost:8000/docs
- [ ] Test /auth/register
- [ ] Test /auth/login (save token)
- [ ] Test /auth/me (with token)
- [ ] Test /chat/send (with token)
- [ ] Test /chat/sessions (with token)
- [ ] Verify database entries in Adminer

**Status:** 🔴 Not Started
**Estimated Time:** 30 minutes

---

#### Mobile App (when UI is ready)

- [ ] Install dependencies (npm install)
- [ ] Start backend server
- [ ] Start Expo (npm start)
- [ ] Test registration flow
- [ ] Test login flow
- [ ] Test sending message
- [ ] Test viewing sessions
- [ ] Test logout
- [ ] Test offline message queue
- [ ] Test token refresh

**Status:** 🔴 Not Started (Waiting for UI)
**Estimated Time:** 1 hour

---

## Test Coverage Report

### Current Status (2025-10-21)

| Component | Files | Lines | Coverage | Status |
|-----------|-------|-------|----------|--------|
| Backend Auth | 0 | 0 | 0% | 🔴 Not Started |
| Backend Chat | 0 | 0 | 0% | 🔴 Not Started |
| Backend Models | 0 | 0 | 0% | 🔴 Not Started |
| Mobile Services | 0 | 0 | 0% | 🔴 Not Started |
| Mobile Stores | 0 | 0 | 0% | 🔴 Not Started |
| **Total** | **0** | **0** | **0%** | **🔴 Not Started** |

---

## Minimal Test Plan for Phase 1

### Priority Order (Must Complete Before Phase 2)

**P0 - Critical (Must Have):**
1. Backend auth tests (register, login, logout) - 2h
2. Backend chat tests (send message, sessions) - 2h
3. Security tests (JWT, password hashing) - 2h
4. Manual API testing - 0.5h

**Total P0 Time:** ~6.5 hours

**P1 - High (Should Have):**
1. Database model tests - 1.5h
2. Integration E2E flow tests - 2h
3. Mobile service tests - 2h

**Total P1 Time:** ~5.5 hours

**P2 - Medium (Nice to Have):**
1. Mobile UI tests (after screens built) - 2h
2. Performance tests - 1h
3. Load testing - 1h

**Total P2 Time:** ~4 hours

**Grand Total:** ~16 hours for comprehensive Phase 1 testing

---

## Recommended Approach

### Quick Validation (1-2 hours)
For immediate confidence before continuing:

1. **Manual API Testing** (30 min)
   - Start services
   - Test each endpoint via Swagger
   - Verify DB changes

2. **Write 3 Critical Tests** (1 hour)
   - test_login_success
   - test_send_message_new_session
   - test_jwt_token_generation

3. **Run Tests** (5 min)
   ```bash
   cd backend
   pytest tests/ -v
   ```

### Full Testing (6-16 hours)
For production readiness:

1. Complete all P0 tests
2. Complete all P1 tests
3. Achieve 85%+ coverage
4. Setup CI to run tests automatically

---

## Test Execution Commands

### Backend

```bash
# Run all tests
cd backend
pytest

# Run with coverage
pytest --cov=app --cov-report=html --cov-report=term

# Run specific test file
pytest tests/test_auth.py -v

# Run specific test
pytest tests/test_auth.py::test_login_success -v

# Run and show print statements
pytest -s

# Run with markers
pytest -m "auth" -v
```

### Mobile

```bash
# Run all tests
cd mobile-app
npm test

# Run with coverage
npm run test:coverage

# Run in watch mode
npm run test:watch

# Run specific file
npm test -- auth.test.ts
```

---

## CI/CD Integration

### GitHub Actions (Already Setup)

Current workflows will run tests automatically:

```yaml
# .github/workflows/backend-ci.yml
- Run tests
- Upload coverage to Codecov
- Fail build if coverage < 85%

# .github/workflows/mobile-ci.yml
- Run tests
- Upload coverage to Codecov
```

**Status:** ✅ CI configured, waiting for tests

---

## Security Testing

### Automated Security Scans

- [ ] Dependabot (GitHub) - Check for vulnerable dependencies
- [ ] SAST (Static Analysis) - Bandit for Python, ESLint for TypeScript
- [ ] Secret scanning - Detect committed API keys
- [ ] SQL injection testing - SQLMap
- [ ] API fuzzing - Postman/Newman

**Status:** 🔴 Not Configured
**Priority:** P1

---

## Performance Testing

### Load Testing (Future)

Tools: Locust, K6, Artillery

**Scenarios:**
- 100 concurrent users
- 1000 messages/minute
- Token refresh under load
- Database query performance

**Targets:**
- API p95 response time < 500ms
- API p99 response time < 1000ms
- Support 10,000 daily active users

**Status:** 🔴 Not Started
**Priority:** P2 (Phase 3+)

---

## Test Data Management

### Test Fixtures

**Backend:**
```python
# tests/conftest.py
@pytest.fixture
def test_user():
    return User(
        email="test@example.com",
        full_name="Test User",
        password_hash="..."
    )

@pytest.fixture
def auth_headers(test_user):
    token = create_access_token(test_user.id)
    return {"Authorization": f"Bearer {token}"}
```

**Mobile:**
```typescript
// __tests__/fixtures/user.ts
export const mockUser = {
  id: "123",
  email: "test@example.com",
  full_name: "Test User",
  // ...
};
```

---

## Bug Tracking

### Known Issues

| ID | Component | Description | Severity | Status |
|----|-----------|-------------|----------|--------|
| - | - | None yet | - | - |

---

## Test Metrics Dashboard (Future)

Goals for Phase 2+:
- [ ] Setup Codecov integration
- [ ] Create test result dashboard
- [ ] Track coverage trends over time
- [ ] Monitor test execution time
- [ ] Flaky test detection

---

## Next Steps

**Immediate (Before Phase 2):**
1. ✅ Create test plan (this document)
2. 🔴 Write P0 backend tests (6.5 hours)
3. 🔴 Run manual API testing (30 min)
4. 🔴 Verify 85%+ coverage

**Short-term (Phase 1 completion):**
1. Write P1 tests (5.5 hours)
2. Setup test automation in CI
3. Document test results

**Long-term (Phase 2+):**
1. Add E2E tests with Playwright
2. Performance testing
3. Security audits
4. Load testing

---

**Last Updated:** 2025-10-21
**Status:** Test plan created, no tests implemented yet
**Next Action:** Decide on immediate testing vs. continue with UI development
