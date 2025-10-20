# Smart AI - Implementation Guide

## Quick Start for Development Teams

This guide provides step-by-step instructions for implementing the Smart AI architecture.

---

## Part 1: Backend Setup

### 1.1 FastAPI Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI app initialization
│   ├── config.py               # Configuration management
│   ├── dependencies.py         # Shared dependencies
│   │
│   ├── api/
│   │   ├── __init__.py
│   │   ├── v1/
│   │   │   ├── __init__.py
│   │   │   ├── endpoints/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── auth.py     # Authentication routes
│   │   │   │   ├── chat.py     # Chat endpoints
│   │   │   │   ├── health.py   # Health metrics
│   │   │   │   ├── users.py    # User management
│   │   │   │   ├── alerts.py   # Alert management
│   │   │   │   └── memory.py   # Memory/RAG endpoints
│   │   │   └── ws/
│   │   │       └── chat_ws.py  # WebSocket handlers
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── auth_service.py     # Authentication logic
│   │   ├── chat_service.py     # Chat processing
│   │   ├── llm_service.py      # LLM integration
│   │   ├── memory_service.py   # RAG pipeline
│   │   ├── health_service.py   # Health monitoring
│   │   ├── pattern_service.py  # Pattern detection
│   │   └── voice_service.py    # Voice processing
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── schemas.py          # Pydantic models
│   │   ├── database.py         # SQLAlchemy models
│   │   └── enums.py            # Enums
│   │
│   ├── db/
│   │   ├── __init__.py
│   │   ├── base.py             # Database session
│   │   ├── crud.py             # CRUD operations
│   │   └── migrations/
│   │       └── versions/
│   │
│   ├── core/
│   │   ├── __init__.py
│   │   ├── security.py         # Security utilities
│   │   ├── logger.py           # Logging setup
│   │   └── constants.py        # App constants
│   │
│   └── utils/
│       ├── __init__.py
│       ├── validators.py       # Data validators
│       ├── decorators.py       # Custom decorators
│       └── helpers.py          # Helper functions
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_auth.py
│   ├── test_chat.py
│   ├── test_health.py
│   └── test_memory.py
│
├── scripts/
│   ├── init_db.py
│   ├── seed_data.py
│   └── migrate.py
│
├── Dockerfile
├── requirements.txt
├── alembic.ini
└── pytest.ini
```

### 1.2 FastAPI Main Application

```python
# backend/app/main.py

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZIPMiddleware
from fastapi.exceptions import RequestValidationError
from contextlib import asynccontextmanager
from prometheus_client import make_asgi_app

from app.api.v1 import endpoints
from app.core.logger import setup_logger
from app.db.base import init_db
import app.config as config

# Setup logging
logger = setup_logger(__name__)

# Lifespan context manager
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Starting Smart AI application")
    await init_db()
    yield
    # Shutdown
    logger.info("Shutting down Smart AI application")

# Create FastAPI app
app = FastAPI(
    title="Smart AI - Elder Care Companion",
    description="AI companion system for elderly care with voice support",
    version="1.0.0",
    lifespan=lifespan
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=config.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["X-Request-ID"]
)

# Gzip compression
app.add_middleware(GZIPMiddleware, minimum_size=1000)

# Include routers
app.include_router(endpoints.auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(endpoints.chat.router, prefix="/api/v1/conversations", tags=["chat"])
app.include_router(endpoints.health.router, prefix="/api/v1/health", tags=["health"])
app.include_router(endpoints.users.router, prefix="/api/v1/users", tags=["users"])
app.include_router(endpoints.alerts.router, prefix="/api/v1/alerts", tags=["alerts"])
app.include_router(endpoints.memory.router, prefix="/api/v1/memory", tags=["memory"])

# Health check endpoints
@app.get("/health", tags=["monitoring"])
async def health():
    return {"status": "healthy"}

@app.get("/ready", tags=["monitoring"])
async def readiness():
    return {"status": "ready"}

# Prometheus metrics
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)

# Exception handlers
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.warning(f"Validation error: {exc}")
    return {
        "error": {
            "code": "INVALID_REQUEST",
            "message": "Request validation failed",
            "details": exc.errors()
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=config.DEBUG,
        workers=4
    )
```

### 1.3 Database Configuration

```python
# backend/app/db/base.py

from sqlalchemy import create_engine, pool
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
import app.config as config

# Create async engine
engine = create_async_engine(
    config.DATABASE_URL,
    echo=config.DEBUG,
    poolclass=pool.NullPool if config.DATABASE_POOL_SIZE == 0 else pool.QueuePool,
    pool_size=config.DATABASE_POOL_SIZE,
    max_overflow=config.DATABASE_MAX_OVERFLOW,
    connect_args={
        "timeout": 30,
        "server_settings": {
            "application_name": "smartai",
            "jit": "off"
        }
    }
)

# Create session factory
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False
)

# Declarative base
Base = declarative_base()

async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
```

### 1.4 SQLAlchemy Models

```python
# backend/app/models/database.py

from sqlalchemy import Column, String, Integer, DateTime, Boolean, JSON, UUID, ForeignKey, Float, Text, ARRAY
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from app.db.base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    date_of_birth = Column(String(10))
    timezone = Column(String(50), default="UTC")
    preferred_language = Column(String(5), default="en")

    # Health context
    medical_conditions = Column(JSON, default=list)
    medications = Column(JSON, default=list)
    allergies = Column(ARRAY(String), default=list)
    emergency_contacts = Column(JSON, default=list)

    # Preferences
    communication_style = Column(String(50), default="formal")
    voice_preference = Column(String(50), default="female")
    conversation_frequency = Column(String(50))

    # Privacy
    consents = Column(JSON, default=dict)
    hipaa_acknowledged = Column(Boolean, default=False)

    # Audit
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = Column(DateTime, nullable=True)

    # Relationships
    devices = relationship("Device", back_populates="user")
    conversations = relationship("ConversationSession", back_populates="user")
    messages = relationship("ChatMessage", back_populates="user")
    health_metrics = relationship("HealthMetric", back_populates="user")
    alerts = relationship("Alert", back_populates="user")

class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    conversation_id = Column(UUID(as_uuid=True), ForeignKey("conversation_sessions.id"))
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))

    message_type = Column(String(50), default="text")
    content = Column(Text, nullable=False)
    sender_type = Column(String(50), nullable=False)
    sentiment = Column(String(50))

    # LLM metadata
    llm_model_used = Column(String(100))
    tokens_used = Column(Integer)
    response_latency_ms = Column(Integer)

    # Health signals
    health_signals = Column(JSON)
    mentioned_symptoms = Column(ARRAY(String))

    # Embedding reference
    embedding_id = Column(String(255))

    # Sync tracking
    sync_status = Column(String(50), default="pending")
    local_id = Column(String(255))

    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    conversation = relationship("ConversationSession")
    user = relationship("User", back_populates="messages")

class HealthMetric(Base):
    __tablename__ = "health_metrics"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))

    mood_level = Column(Integer)
    pain_level = Column(Integer)
    energy_level = Column(Integer)
    anxiety_level = Column(Integer)
    sleep_hours = Column(Float)

    observations = Column(Text)
    medication_adherence = Column(Boolean)

    requires_attention = Column(Boolean, default=False)
    anomaly_detected = Column(Boolean, default=False)
    alert_reason = Column(Text)

    recorded_at = Column(DateTime, default=datetime.utcnow, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="health_metrics")

class Alert(Base):
    __tablename__ = "alerts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))

    alert_type = Column(String(100), nullable=False)
    severity = Column(String(50), nullable=False)
    title = Column(String(255))
    description = Column(Text)

    is_acknowledged = Column(Boolean, default=False)
    acknowledged_at = Column(DateTime)

    created_at = Column(DateTime, default=datetime.utcnow, index=True)

    user = relationship("User", back_populates="alerts")
```

### 1.5 Pydantic Schemas

```python
# backend/app/models/schemas.py

from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional, List, Dict, Any
from uuid import UUID
from datetime import datetime

class UserRegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=14)
    first_name: str
    last_name: str
    timezone: str = "UTC"
    date_of_birth: Optional[str] = None

class UserLoginRequest(BaseModel):
    email: EmailStr
    password: str

class ChatMessageCreate(BaseModel):
    content: str
    message_type: str = "text"
    health_signals: Optional[Dict[str, Any]] = None

class ChatMessageResponse(BaseModel):
    id: UUID
    content: str
    sender_type: str
    sentiment: Optional[str]
    timestamp: datetime

    class Config:
        from_attributes = True

class HealthMetricCreate(BaseModel):
    mood_level: int = Field(..., ge=1, le=10)
    pain_level: int = Field(..., ge=0, le=10)
    energy_level: int = Field(..., ge=1, le=10)
    anxiety_level: Optional[int] = Field(None, ge=0, le=10)
    observations: Optional[str] = None

class HealthMetricResponse(HealthMetricCreate):
    id: UUID
    recorded_at: datetime
    anomalies_detected: bool

    class Config:
        from_attributes = True

class AlertResponse(BaseModel):
    id: UUID
    alert_type: str
    severity: str
    title: str
    description: Optional[str]
    created_at: datetime
    is_acknowledged: bool

    class Config:
        from_attributes = True
```

---

## Part 2: Mobile Implementation

### 2.1 React Native Project Structure

```
mobile/
├── src/
│   ├── App.tsx                 # Root component
│   ├── index.tsx               # Entry point
│   │
│   ├── navigation/
│   │   ├── RootNavigator.tsx
│   │   ├── AuthNavigator.tsx
│   │   └── AppNavigator.tsx
│   │
│   ├── screens/
│   │   ├── auth/
│   │   │   ├── LoginScreen.tsx
│   │   │   └── RegisterScreen.tsx
│   │   ├── home/
│   │   │   └── HomeScreen.tsx
│   │   ├── chat/
│   │   │   ├── ChatScreen.tsx
│   │   │   └── ChatHistoryScreen.tsx
│   │   ├── health/
│   │   │   ├── HealthScreen.tsx
│   │   │   └── MetricsDetailScreen.tsx
│   │   └── profile/
│   │       └── ProfileScreen.tsx
│   │
│   ├── services/
│   │   ├── api/
│   │   │   ├── apiClient.ts
│   │   │   ├── authApi.ts
│   │   │   ├── chatApi.ts
│   │   │   ├── healthApi.ts
│   │   │   └── offsetSyncApi.ts
│   │   ├── storage/
│   │   │   ├── localStorage.ts
│   │   │   └── database.ts
│   │   ├── voice/
│   │   │   ├── voiceService.ts
│   │   │   └── ttsService.ts
│   │   └── sync/
│   │       ├── syncService.ts
│   │       └── conflictResolver.ts
│   │
│   ├── components/
│   │   ├── common/
│   │   │   ├── Button.tsx
│   │   │   ├── Input.tsx
│   │   │   ├── Card.tsx
│   │   │   └── LoadingSpinner.tsx
│   │   ├── chat/
│   │   │   ├── ChatBubble.tsx
│   │   │   ├── VoiceButton.tsx
│   │   │   └── ChatInput.tsx
│   │   └── health/
│   │       ├── MetricSlider.tsx
│   │       └── MetricCard.tsx
│   │
│   ├── redux/
│   │   ├── store.ts
│   │   ├── slices/
│   │   │   ├── authSlice.ts
│   │   │   ├── chatSlice.ts
│   │   │   ├── healthSlice.ts
│   │   │   └── uiSlice.ts
│   │   └── thunks/
│   │       ├── authThunks.ts
│   │       └── chatThunks.ts
│   │
│   ├── utils/
│   │   ├── validators.ts
│   │   ├── formatters.ts
│   │   ├── logger.ts
│   │   └── constants.ts
│   │
│   └── styles/
│       ├── colors.ts
│       ├── fonts.ts
│       └── spacing.ts
│
├── app.json
├── package.json
├── tsconfig.json
└── jest.config.js
```

### 2.2 API Client Setup

```typescript
// mobile/src/services/api/apiClient.ts

import axios, { AxiosInstance, AxiosError } from 'axios';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { Platform } from 'react-native';

const API_BASE_URL = 'https://api.smartai.com/api/v1';

class APIClient {
  private client: AxiosInstance;
  private accessToken: string | null = null;
  private refreshToken: string | null = null;

  constructor() {
    this.client = axios.create({
      baseURL: API_BASE_URL,
      timeout: 30000,
      headers: {
        'Content-Type': 'application/json',
        'X-Platform': Platform.OS,
      }
    });

    this.setupInterceptors();
  }

  private setupInterceptors() {
    // Request interceptor
    this.client.interceptors.request.use(
      async (config) => {
        // Add auth token
        if (this.accessToken) {
          config.headers.Authorization = `Bearer ${this.accessToken}`;
        }

        // Add request ID for tracing
        config.headers['X-Request-ID'] = generateUUID();

        return config;
      },
      (error) => Promise.reject(error)
    );

    // Response interceptor
    this.client.interceptors.response.use(
      (response) => response,
      async (error: AxiosError) => {
        const originalRequest = error.config as any;

        // Handle token expiration
        if (error.response?.status === 401 && !originalRequest._retry) {
          originalRequest._retry = true;

          try {
            const newTokens = await this.refreshAccessToken();
            this.accessToken = newTokens.access_token;
            originalRequest.headers.Authorization = `Bearer ${newTokens.access_token}`;
            return this.client(originalRequest);
          } catch (refreshError) {
            // Clear auth and redirect to login
            await this.clearAuth();
            return Promise.reject(refreshError);
          }
        }

        return Promise.reject(error);
      }
    );
  }

  async setAuth(accessToken: string, refreshToken: string): Promise<void> {
    this.accessToken = accessToken;
    this.refreshToken = refreshToken;

    await AsyncStorage.multiSet([
      ['@smartai_access_token', accessToken],
      ['@smartai_refresh_token', refreshToken]
    ]);
  }

  async loadAuth(): Promise<boolean> {
    try {
      const [accessToken, refreshToken] = await AsyncStorage.multiGet([
        '@smartai_access_token',
        '@smartai_refresh_token'
      ]);

      if (accessToken[1] && refreshToken[1]) {
        this.accessToken = accessToken[1];
        this.refreshToken = refreshToken[1];
        return true;
      }
      return false;
    } catch (error) {
      console.error('Error loading auth:', error);
      return false;
    }
  }

  private async refreshAccessToken(): Promise<{ access_token: string }> {
    const response = await axios.post(`${API_BASE_URL}/auth/refresh`, {
      refresh_token: this.refreshToken
    });

    return response.data;
  }

  async clearAuth(): Promise<void> {
    this.accessToken = null;
    this.refreshToken = null;
    await AsyncStorage.removeItem('@smartai_access_token');
    await AsyncStorage.removeItem('@smartai_refresh_token');
  }

  get instance(): AxiosInstance {
    return this.client;
  }
}

export default new APIClient();
```

### 2.3 Chat Screen Component

```typescript
// mobile/src/screens/chat/ChatScreen.tsx

import React, { useState, useEffect, useRef } from 'react';
import {
  View,
  ScrollView,
  TextInput,
  TouchableOpacity,
  ActivityIndicator,
  SafeAreaView,
  AccessibilityInfo,
  Dimensions,
} from 'react-native';
import { useDispatch, useSelector } from 'react-redux';
import LinearGradient from 'react-native-linear-gradient';
import Animated, {
  useAnimatedStyle,
  useSharedValue,
  withSpring,
} from 'react-native-reanimated';

import VoiceButton from '../../components/chat/VoiceButton';
import ChatBubble from '../../components/chat/ChatBubble';
import { chatThunks } from '../../redux/thunks/chatThunks';
import { chatSlice } from '../../redux/slices/chatSlice';
import styles from './ChatScreen.styles';

const ChatScreen: React.FC<{ conversationId: string }> = ({ conversationId }) => {
  const dispatch = useDispatch();
  const { messages, loading, error } = useSelector((state: any) => state.chat);
  const scrollViewRef = useRef<ScrollView>(null);

  const [inputText, setInputText] = useState('');
  const [isVoiceActive, setIsVoiceActive] = useState(false);
  const messageInputAnim = useSharedValue(0);

  const screenHeight = Dimensions.get('window').height;

  useEffect(() => {
    // Load conversation history
    dispatch(chatThunks.fetchConversationHistory({ conversationId }));
  }, [conversationId]);

  const handleSendMessage = async () => {
    if (!inputText.trim()) return;

    const message = inputText;
    setInputText('');

    try {
      // Dispatch action to send message
      dispatch(chatThunks.sendMessage({
        conversationId,
        content: message,
        messageType: 'text',
      }));

      // Scroll to bottom
      setTimeout(() => {
        scrollViewRef.current?.scrollToEnd({ animated: true });
      }, 100);
    } catch (error) {
      console.error('Error sending message:', error);
    }
  };

  const handleVoiceStart = async () => {
    setIsVoiceActive(true);
    // Trigger voice recording
  };

  const handleVoiceEnd = async (transcript: string) => {
    setIsVoiceActive(false);

    if (transcript) {
      dispatch(chatThunks.sendMessage({
        conversationId,
        content: transcript,
        messageType: 'voice_transcript',
      }));
    }
  };

  const messageAnimatedStyle = useAnimatedStyle(() => {
    return {
      transform: [{ scaleY: withSpring(messageInputAnim.value) }],
    };
  });

  return (
    <SafeAreaView style={styles.container}>
      <LinearGradient
        colors={['#E8F4F8', '#F5F8FA']}
        style={styles.background}
      >
        {/* Messages Area */}
        <ScrollView
          ref={scrollViewRef}
          style={styles.messagesContainer}
          showsVerticalScrollIndicator={false}
          onContentSizeChange={() => scrollViewRef.current?.scrollToEnd()}
        >
          {messages.map((message) => (
            <ChatBubble
              key={message.id}
              message={message}
              isUser={message.sender_type === 'user'}
            />
          ))}

          {loading && (
            <View style={styles.loadingContainer}>
              <ActivityIndicator size="large" color="#4A90E2" />
            </View>
          )}

          {error && (
            <View style={styles.errorContainer}>
              <Text style={styles.errorText}>{error}</Text>
            </View>
          )}
        </ScrollView>

        {/* Input Area */}
        <Animated.View style={[styles.inputContainer, messageAnimatedStyle]}>
          <View style={styles.inputRow}>
            <TextInput
              style={styles.input}
              placeholder="Type your message..."
              placeholderTextColor="#999"
              value={inputText}
              onChangeText={setInputText}
              multiline
              maxLength={500}
              editable={!loading}
              accessibilityHint="Text input for sending messages"
            />

            <VoiceButton
              onStart={handleVoiceStart}
              onEnd={handleVoiceEnd}
              isActive={isVoiceActive}
            />

            <TouchableOpacity
              style={[
                styles.sendButton,
                { opacity: inputText.trim() ? 1 : 0.5 }
              ]}
              onPress={handleSendMessage}
              disabled={!inputText.trim() || loading}
              accessible
              accessibilityRole="button"
              accessibilityLabel="Send message"
            >
              <Text style={styles.sendButtonText}>Send</Text>
            </TouchableOpacity>
          </View>
        </Animated.View>
      </LinearGradient>
    </SafeAreaView>
  );
};

export default ChatScreen;
```

---

## Part 3: Vector Database Integration

### 3.1 Weaviate Setup & Configuration

```python
# backend/services/weaviate_service.py

import weaviate
from weaviate.classes.config import Configure, Property, DataType, Vectorizer, ModuleConfig
import json
from typing import List, Dict, Any

class WeaviateService:
    def __init__(self, weaviate_url: str):
        self.client = weaviate.connect_to_local(
            host=weaviate_url.replace("http://", "").split(":")[0],
            port=int(weaviate_url.split(":")[-1] if ":" in weaviate_url else 8080)
        )

    async def setup_schema(self):
        """Initialize Weaviate schema for health context storage"""

        # Define UserHealthContext class
        user_health_context_class = {
            "class": "UserHealthContext",
            "description": "Semantic storage of health-related conversation context",
            "vectorizer": "text2vec-transformers",
            "properties": [
                Property(
                    name="content",
                    data_type=DataType.TEXT,
                    description="Raw conversation content"
                ),
                Property(
                    name="summary",
                    data_type=DataType.TEXT,
                    description="Summarized content"
                ),
                Property(
                    name="user_id",
                    data_type=DataType.UUID,
                    description="Reference to user"
                ),
                Property(
                    name="conversation_id",
                    data_type=DataType.UUID,
                    description="Reference to conversation"
                ),
                Property(
                    name="timestamp",
                    data_type=DataType.DATE,
                    description="When context was created"
                ),
                Property(
                    name="health_topics",
                    data_type=DataType.TEXT_ARRAY,
                    description="Extracted health topics"
                ),
                Property(
                    name="sentiment",
                    data_type=DataType.TEXT,
                    description="Sentiment of conversation"
                ),
                Property(
                    name="relevance_score",
                    data_type=DataType.NUMBER,
                    description="Relevance score"
                ),
            ],
            "moduleConfig": {
                "text2vec-transformers": {
                    "vectorizePropertyName": False,
                    "model": "sentence-transformers/all-MiniLM-L6-v2"
                }
            }
        }

        # Create class if not exists
        try:
            self.client.collections.create_from_dict(user_health_context_class)
            print("UserHealthContext class created")
        except Exception as e:
            print(f"Class might already exist: {e}")

    async def add_context(
        self,
        user_id: str,
        conversation_id: str,
        content: str,
        summary: str,
        health_topics: List[str],
        sentiment: str
    ) -> str:
        """Add health context to Weaviate"""

        obj = {
            "content": content,
            "summary": summary,
            "user_id": user_id,
            "conversation_id": conversation_id,
            "timestamp": datetime.now().isoformat(),
            "health_topics": health_topics,
            "sentiment": sentiment,
            "relevance_score": 1.0
        }

        # Add to collection
        collection = self.client.collections.get("UserHealthContext")
        result = collection.data.insert(properties=obj)

        return result

    async def search_context(
        self,
        user_id: str,
        query: str,
        limit: int = 5,
        threshold: float = 0.6
    ) -> List[Dict[str, Any]]:
        """Search for relevant context using hybrid search"""

        collection = self.client.collections.get("UserHealthContext")

        # Hybrid search (keyword + semantic)
        results = collection.query.hybrid(
            query=query,
            limit=limit,
            where=f"user_id == '{user_id}'",
            alpha=0.5  # 50% keyword, 50% semantic
        )

        formatted_results = []
        for obj in results.objects:
            if hasattr(obj, 'metadata'):
                score = obj.metadata.score if hasattr(obj.metadata, 'score') else 1.0

                if score >= threshold:
                    formatted_results.append({
                        "id": obj.uuid,
                        "content": obj.properties.get("content"),
                        "summary": obj.properties.get("summary"),
                        "health_topics": obj.properties.get("health_topics", []),
                        "sentiment": obj.properties.get("sentiment"),
                        "timestamp": obj.properties.get("timestamp"),
                        "relevance_score": score
                    })

        return formatted_results

    async def delete_old_contexts(self, days: int = 90):
        """Clean up old contexts for privacy"""

        collection = self.client.collections.get("UserHealthContext")
        cutoff_date = (datetime.now() - timedelta(days=days)).isoformat()

        # Delete where timestamp < cutoff_date
        collection.data.delete_many(
            where=f"timestamp < '{cutoff_date}'"
        )
```

---

## Part 4: Testing Strategy

### 4.1 Backend Unit Tests

```python
# backend/tests/test_chat.py

import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.db.base import AsyncSessionLocal

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
async def test_user():
    """Create test user"""
    async with AsyncSessionLocal() as session:
        user = User(
            email="test@example.com",
            password_hash=hash_password("testpass123"),
            first_name="Test",
            last_name="User"
        )
        session.add(user)
        await session.commit()
        return user

def test_send_message(client, test_user):
    """Test sending a chat message"""

    access_token = generate_token(test_user.id)

    response = client.post(
        "/api/v1/conversations/test_conv/messages",
        headers={"Authorization": f"Bearer {access_token}"},
        json={
            "content": "Hello, how are you?",
            "message_type": "text"
        }
    )

    assert response.status_code == 201
    assert response.json()["user_message"]["content"] == "Hello, how are you?"
    assert "assistant_message" in response.json()

def test_retrieve_health_metrics(client, test_user):
    """Test retrieving health metrics"""

    access_token = generate_token(test_user.id)

    response = client.get(
        "/api/v1/health/metrics?days=7",
        headers={"Authorization": f"Bearer {access_token}"}
    )

    assert response.status_code == 200
    assert "metrics" in response.json()

@pytest.mark.asyncio
async def test_semantic_search(memory_service, test_user):
    """Test RAG semantic search"""

    results = await memory_service.semantic_search(
        user_id=str(test_user.id),
        query="medications",
        limit=5
    )

    assert isinstance(results, list)
    for result in results:
        assert "relevance_score" in result
        assert result["relevance_score"] > 0.6
```

### 4.2 Mobile Integration Tests

```typescript
// mobile/src/__tests__/services/apiClient.test.ts

import APIClient from '../../services/api/apiClient';
import AsyncStorage from '@react-native-async-storage/async-storage';
import axios from 'axios';

jest.mock('@react-native-async-storage/async-storage');
jest.mock('axios');

describe('APIClient', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  test('setAuth stores tokens', async () => {
    await APIClient.setAuth('test_access_token', 'test_refresh_token');

    expect(AsyncStorage.multiSet).toHaveBeenCalledWith([
      ['@smartai_access_token', 'test_access_token'],
      ['@smartai_refresh_token', 'test_refresh_token']
    ]);
  });

  test('loadAuth retrieves tokens from storage', async () => {
    (AsyncStorage.multiGet as jest.Mock).mockResolvedValue([
      ['@smartai_access_token', 'stored_access_token'],
      ['@smartai_refresh_token', 'stored_refresh_token']
    ]);

    const result = await APIClient.loadAuth();

    expect(result).toBe(true);
  });

  test('clearAuth removes all auth data', async () => {
    await APIClient.clearAuth();

    expect(AsyncStorage.removeItem).toHaveBeenCalled();
  });
});
```

---

## Part 5: Deployment

### 5.1 Docker Build

```dockerfile
# backend/Dockerfile

FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY app ./app
COPY alembic ./alembic
COPY alembic.ini .

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/health')" || exit 1

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 5.2 Kubernetes Service

```yaml
# backend/k8s/service.yaml
apiVersion: v1
kind: Service
metadata:
  name: smartai-api
  namespace: smartai
spec:
  type: LoadBalancer
  selector:
    app: smartai-api
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8000
    name: http
```

---

## Quick Checklist for Implementation

### Week 1 Tasks
- [ ] Set up PostgreSQL database
- [ ] Initialize FastAPI project structure
- [ ] Implement JWT authentication
- [ ] Create user registration and login
- [ ] Set up React Native project

### Week 2 Tasks
- [ ] Build chat API endpoints
- [ ] Integrate Claude API
- [ ] Set up Weaviate
- [ ] Implement message storage
- [ ] Create chat UI

### Week 3 Tasks
- [ ] Integrate speech-to-text
- [ ] Integrate text-to-speech
- [ ] Build health metrics API
- [ ] Add sentiment analysis
- [ ] Refine persona

### Week 4 Tasks
- [ ] Implement offline sync
- [ ] Set up local storage
- [ ] Build conflict resolution
- [ ] UI/UX refinements
- [ ] Security audit

---

This guide provides the foundation for the development team to implement Smart AI. Reference the main ARCHITECTURE.md for detailed specifications.
