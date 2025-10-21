# Smart AI - API Documentation

**Base URL:** `http://localhost:8000/api/v1`

**Interactive Docs:** http://localhost:8000/docs (Swagger UI)

---

## Authentication

All endpoints except `/auth/register` and `/auth/login` require authentication.

### Headers

```http
Authorization: Bearer <access_token>
Content-Type: application/json
```

### Token Management

- **Access Token:** Valid for 30 minutes
- **Refresh Token:** Valid for 7 days
- Tokens are automatically refreshed by the mobile app on 401 responses

---

## Endpoints

### Authentication

#### 1. Register User

```http
POST /auth/register
```

**Request Body:**

```json
{
  "email": "user@example.com",
  "password": "SecurePassword123!",
  "full_name": "John Doe"
}
```

**Response (201 Created):**

```json
{
  "id": "ea685676-815a-45f9-94b7-55fa7204d647",
  "email": "user@example.com",
  "full_name": "John Doe",
  "role": "user",
  "is_active": true,
  "is_verified": false,
  "created_at": "2025-10-21T00:00:00Z",
  "last_login_at": null,
  "profile": {
    "id": "profile-uuid",
    "user_id": "ea685676-815a-45f9-94b7-55fa7204d647",
    "date_of_birth": null,
    "phone_number": null,
    "preferences": {}
  }
}
```

**Errors:**
- `400` - Email already registered
- `422` - Validation error (weak password, invalid email)

---

#### 2. Login

```http
POST /auth/login
```

**Request Body:**

```json
{
  "email": "test@smartai.com",
  "password": "TestPass123!"
}
```

**Response (200 OK):**

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Errors:**
- `401` - Incorrect email or password
- `403` - Inactive user account

---

#### 3. Refresh Token

```http
POST /auth/refresh
```

**Request Body:**

```json
{
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Response (200 OK):**

```json
{
  "access_token": "new-access-token",
  "refresh_token": "new-refresh-token",
  "token_type": "bearer"
}
```

**Errors:**
- `401` - Invalid or expired refresh token

---

#### 4. Get Current User

```http
GET /auth/me
```

**Headers:** `Authorization: Bearer <access_token>`

**Response (200 OK):**

```json
{
  "id": "ea685676-815a-45f9-94b7-55fa7204d647",
  "email": "test@smartai.com",
  "full_name": "Test User",
  "role": "user",
  "is_active": true,
  "is_verified": true,
  "created_at": "2025-10-21T00:00:00Z",
  "last_login_at": "2025-10-21T07:00:00Z",
  "profile": {
    "id": "profile-uuid",
    "user_id": "ea685676-815a-45f9-94b7-55fa7204d647",
    "phone_number": "+1234567890",
    "emergency_contact_name": "Emergency Contact",
    "preferences": {
      "timezone": "America/New_York",
      "language": "en"
    }
  }
}
```

**Errors:**
- `401` - Unauthorized (invalid or missing token)

---

#### 5. Logout

```http
POST /auth/logout
```

**Headers:** `Authorization: Bearer <access_token>`

**Response (200 OK):**

```json
{
  "message": "Successfully logged out"
}
```

---

### Chat

#### 1. Send Message

```http
POST /chat/send
```

**Headers:** `Authorization: Bearer <access_token>`

**Request Body:**

```json
{
  "message": "Hello, how are you today?",
  "session_id": "optional-session-uuid"
}
```

If `session_id` is omitted, a new conversation session is created.

**Response (200 OK):**

```json
{
  "session_id": "session-uuid",
  "user_message": {
    "id": "message-uuid-1",
    "session_id": "session-uuid",
    "user_id": "user-uuid",
    "content": "Hello, how are you today?",
    "sender": "user",
    "created_at": "2025-10-21T07:10:00Z",
    "sentiment_score": null,
    "tokens_used": null
  },
  "ai_message": {
    "id": "message-uuid-2",
    "session_id": "session-uuid",
    "user_id": "user-uuid",
    "content": "Hello! I'm doing well, thank you for asking. How are you feeling today? Is there anything you'd like to talk about or any way I can help you?",
    "sender": "ai",
    "created_at": "2025-10-21T07:10:01Z",
    "sentiment_score": null,
    "tokens_used": 245
  }
}
```

**Errors:**
- `401` - Unauthorized
- `404` - Session not found (if session_id provided)
- `500` - Claude API error

---

#### 2. Get Conversation Sessions

```http
GET /chat/sessions?page=1&page_size=20
```

**Headers:** `Authorization: Bearer <access_token>`

**Query Parameters:**
- `page` (optional): Page number (default: 1)
- `page_size` (optional): Items per page (default: 20, max: 100)

**Response (200 OK):**

```json
{
  "sessions": [
    {
      "id": "session-uuid-1",
      "user_id": "user-uuid",
      "title": "Conversation",
      "is_active": true,
      "message_count": 12,
      "started_at": "2025-10-21T07:00:00Z",
      "last_message_at": "2025-10-21T07:15:00Z"
    },
    {
      "id": "session-uuid-2",
      "user_id": "user-uuid",
      "title": "Health Check",
      "is_active": false,
      "message_count": 6,
      "started_at": "2025-10-20T14:00:00Z",
      "last_message_at": "2025-10-20T14:10:00Z"
    }
  ],
  "total": 2,
  "page": 1,
  "page_size": 20
}
```

**Errors:**
- `401` - Unauthorized

---

#### 3. Get Session with Messages

```http
GET /chat/sessions/{session_id}
```

**Headers:** `Authorization: Bearer <access_token>`

**Response (200 OK):**

```json
{
  "id": "session-uuid",
  "user_id": "user-uuid",
  "title": "Conversation",
  "is_active": true,
  "message_count": 4,
  "started_at": "2025-10-21T07:00:00Z",
  "last_message_at": "2025-10-21T07:10:00Z",
  "messages": [
    {
      "id": "message-uuid-1",
      "content": "Hello!",
      "sender": "user",
      "created_at": "2025-10-21T07:00:00Z",
      "sentiment_score": null,
      "tokens_used": null
    },
    {
      "id": "message-uuid-2",
      "content": "Hello! How can I help you today?",
      "sender": "ai",
      "created_at": "2025-10-21T07:00:01Z",
      "sentiment_score": null,
      "tokens_used": 156
    }
  ]
}
```

**Errors:**
- `401` - Unauthorized
- `404` - Session not found or doesn't belong to user

---

#### 4. Delete Session

```http
DELETE /chat/sessions/{session_id}
```

**Headers:** `Authorization: Bearer <access_token>`

**Response (200 OK):**

```json
{
  "message": "Session deleted successfully"
}
```

**Errors:**
- `401` - Unauthorized
- `404` - Session not found or doesn't belong to user

---

## Health Check

#### Get API Health

```http
GET /health
```

**Response (200 OK):**

```json
{
  "status": "healthy",
  "version": "0.1.0",
  "timestamp": "2025-10-21T07:00:00Z"
}
```

---

#### Get Readiness

```http
GET /health/ready
```

Checks database and external service connections.

**Response (200 OK):**

```json
{
  "status": "ready",
  "database": "connected",
  "claude_api": "configured"
}
```

**Response (503 Service Unavailable):**

```json
{
  "status": "not ready",
  "database": "disconnected",
  "claude_api": "not configured"
}
```

---

## Error Responses

All errors follow this format:

```json
{
  "detail": "Error message describing what went wrong"
}
```

### Common HTTP Status Codes

- **200** - Success
- **201** - Created (registration)
- **400** - Bad Request (validation error, duplicate email)
- **401** - Unauthorized (invalid or missing token)
- **403** - Forbidden (inactive account)
- **404** - Not Found (session not found)
- **422** - Unprocessable Entity (validation error)
- **500** - Internal Server Error
- **503** - Service Unavailable (database down)

---

## Rate Limiting

**Not yet implemented** - Will be added in Phase 3

Planned limits:
- Authentication: 10 requests/minute
- Chat: 60 messages/hour per user
- Sessions: 100 requests/minute

---

## AI Model Configuration

**Current Model:** Claude 3.5 Sonnet (2024-10-22)

**System Prompt:** Nurse persona - compassionate, patient, caring

**Context Window:**
- Maximum 10 recent messages included in conversation history
- Each API call includes conversation context
- Older messages are stored but not sent to Claude

**Token Usage:**
- Average: 150-300 tokens per response
- Tracked per message in `tokens_used` field
- Can be used for cost analysis

---

## Example Workflows

### 1. New User Registration & First Chat

```bash
# 1. Register
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "newuser@example.com",
    "password": "SecurePass123!",
    "full_name": "New User"
  }'

# 2. Login
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "newuser@example.com",
    "password": "SecurePass123!"
  }' | jq -r '.access_token'

# Save token
export TOKEN="<access_token>"

# 3. Send first message
curl -X POST http://localhost:8000/api/v1/chat/send \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Hi, I need someone to talk to."
  }'
```

### 2. Continue Existing Conversation

```bash
# Get sessions
curl -X GET http://localhost:8000/api/v1/chat/sessions \
  -H "Authorization: Bearer $TOKEN" | jq '.sessions[0].id'

# Save session ID
export SESSION_ID="<session-id>"

# Send message to existing session
curl -X POST http://localhost:8000/api/v1/chat/send \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "How is my health looking?",
    "session_id": "'$SESSION_ID'"
  }'
```

### 3. View Conversation History

```bash
# Get session with all messages
curl -X GET http://localhost:8000/api/v1/chat/sessions/$SESSION_ID \
  -H "Authorization: Bearer $TOKEN" | jq '.messages'
```

---

## WebSocket Support (Phase 2)

Planned for real-time messaging:

```javascript
const ws = new WebSocket('ws://localhost:8000/ws/chat');
ws.send(JSON.stringify({
  type: 'message',
  content: 'Hello',
  session_id: 'session-uuid'
}));
```

---

## SDK / Client Libraries

**Mobile App:** Built-in services in `mobile-app/src/services/api/`

**Python Client:** Coming in Phase 2

**JavaScript Client:** Coming in Phase 2

---

**Last Updated:** 2025-10-21
**API Version:** v1
**Backend Version:** 0.1.0
