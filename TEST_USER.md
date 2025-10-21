# Test User Credentials

## Smart AI - Test Account

A test user has been created in the database for development and testing purposes.

### Login Credentials

```
Email:    test@smartai.com
Password: TestPass123!
```

### User Details

- **User ID:** ea685676-815a-45f9-94b7-55fa7204d647
- **Full Name:** Test User
- **Role:** user
- **Status:** Active and Verified
- **Phone:** +1234567890
- **Emergency Contact:** Emergency Contact (+1234567890)
- **Preferences:**
  - Timezone: America/New_York
  - Language: en

### How to Use

#### Mobile App

1. Start the mobile app:
   ```bash
   cd mobile-app
   npm start
   ```

2. Press `i` for iOS simulator or `a` for Android emulator

3. Login with the credentials above

#### Backend API (Swagger UI)

1. Make sure Docker services are running:
   ```bash
   docker-compose -f infrastructure/docker/docker-compose.dev.yml up -d
   ```

2. Start the backend server:
   ```bash
   cd backend
   pip install -r requirements.txt
   uvicorn app.main:app --reload
   ```

3. Open http://localhost:8000/docs

4. Click "Authorize" button and login:
   - Username: `test@smartai.com`
   - Password: `TestPass123!`

5. Try the endpoints:
   - GET `/api/v1/auth/me` - Get current user
   - POST `/api/v1/chat/send` - Send a message to AI
   - GET `/api/v1/chat/sessions` - Get conversation history

### Testing Scenarios

**Authentication:**
- [x] Login with test credentials
- [x] Get current user profile
- [x] Logout and login again
- [ ] Test token refresh (wait 30 min or manually expire)

**Chat:**
- [ ] Send first message (creates new session)
- [ ] Send multiple messages in same session
- [ ] View conversation history
- [ ] Create new conversation
- [ ] Delete old conversation

**Mobile:**
- [ ] Login on mobile app
- [ ] Send messages via chat interface
- [ ] View sessions list
- [ ] Switch between sessions
- [ ] Logout and login again

### Password Hash

The password `TestPass123!` is hashed using bcrypt with cost factor 12:

```
$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYIWXQXqJUe
```

### Database Access

You can also access the test user directly in the database:

```bash
# Via Docker
docker exec -it seva-postgres psql -U seva_user -d seva_ai

# Query test user
SELECT * FROM users WHERE email = 'test@smartai.com';
SELECT * FROM user_profiles WHERE user_id = 'ea685676-815a-45f9-94b7-55fa7204d647';
```

### Adminer (Database GUI)

Access Adminer at http://localhost:8081

- **System:** PostgreSQL
- **Server:** seva-postgres
- **Username:** seva_user
- **Password:** seva_password
- **Database:** seva_ai

Then navigate to the `users` and `user_profiles` tables to view the test user.

### Creating Additional Test Users

You can create more test users via the registration endpoint:

```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test2@smartai.com",
    "password": "TestPass123!",
    "full_name": "Test User 2"
  }'
```

Or use the SQL script:

```bash
docker exec -i seva-postgres psql -U seva_user -d seva_ai < backend/create_test_user.sql
```

### Security Notes

- This test user should **ONLY** be used in development environments
- Never use this account in production
- The password is intentionally simple for testing purposes
- In production, enforce strong password policies

---

**Created:** 2025-10-21
**Status:** Active
**Environment:** Development only
