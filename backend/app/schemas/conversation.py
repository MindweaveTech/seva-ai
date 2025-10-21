"""Conversation schemas for request/response validation."""

from datetime import datetime
from decimal import Decimal
from typing import Optional, List
from uuid import UUID

from pydantic import BaseModel, Field, ConfigDict


# Base schemas
class ConversationSessionBase(BaseModel):
    """Base conversation session schema."""

    title: Optional[str] = Field(None, max_length=255)


class ChatMessageBase(BaseModel):
    """Base chat message schema."""

    content: str = Field(..., min_length=1)


# Request schemas
class ConversationSessionCreate(ConversationSessionBase):
    """Schema for creating a conversation session."""

    pass


class ChatMessageCreate(ChatMessageBase):
    """Schema for creating a chat message."""

    session_id: Optional[UUID] = None  # If None, create new session


class ChatMessageSend(BaseModel):
    """Schema for sending a message (simplified)."""

    message: str = Field(..., min_length=1, max_length=5000)
    session_id: Optional[UUID] = None


# Response schemas
class ConversationSessionResponse(ConversationSessionBase):
    """Schema for conversation session response."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    user_id: UUID
    started_at: datetime
    ended_at: Optional[datetime] = None
    message_count: int
    is_active: bool
    metadata: dict = Field(default_factory=dict)


class ChatMessageResponse(ChatMessageBase):
    """Schema for chat message response."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    session_id: UUID
    user_id: UUID
    sender: str  # 'user' or 'ai'
    sentiment_score: Optional[Decimal] = None
    sentiment_label: Optional[str] = None
    health_signals: List[dict] = Field(default_factory=list)
    tokens_used: Optional[int] = None
    created_at: datetime
    metadata: dict = Field(default_factory=dict)


class ConversationSessionWithMessages(ConversationSessionResponse):
    """Schema for conversation session with messages."""

    messages: List[ChatMessageResponse] = Field(default_factory=list)


class ChatResponse(BaseModel):
    """Schema for chat API response."""

    session_id: UUID
    user_message: ChatMessageResponse
    ai_message: ChatMessageResponse


class ConversationSessionList(BaseModel):
    """Schema for paginated conversation sessions."""

    sessions: List[ConversationSessionResponse]
    total: int
    page: int
    page_size: int
