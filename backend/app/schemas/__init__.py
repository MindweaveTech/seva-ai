"""Pydantic schemas for request/response validation."""

from app.schemas.user import (
    UserRegister,
    UserLogin,
    UserUpdate,
    UserResponse,
    UserProfileResponse,
    UserProfileUpdate,
    UserWithProfile,
    Token,
    TokenPayload,
    RefreshTokenRequest,
)
from app.schemas.conversation import (
    ConversationSessionCreate,
    ConversationSessionResponse,
    ConversationSessionWithMessages,
    ConversationSessionList,
    ChatMessageCreate,
    ChatMessageSend,
    ChatMessageResponse,
    ChatResponse,
)

__all__ = [
    # User schemas
    "UserRegister",
    "UserLogin",
    "UserUpdate",
    "UserResponse",
    "UserProfileResponse",
    "UserProfileUpdate",
    "UserWithProfile",
    "Token",
    "TokenPayload",
    "RefreshTokenRequest",
    # Conversation schemas
    "ConversationSessionCreate",
    "ConversationSessionResponse",
    "ConversationSessionWithMessages",
    "ConversationSessionList",
    "ChatMessageCreate",
    "ChatMessageSend",
    "ChatMessageResponse",
    "ChatResponse",
]
