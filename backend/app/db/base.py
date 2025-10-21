"""Database base configuration."""

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# Import all models here for Alembic to detect them
from app.models.user import User, UserProfile, Device  # noqa: F401, E402
from app.models.conversation import ConversationSession, ChatMessage  # noqa: F401, E402
