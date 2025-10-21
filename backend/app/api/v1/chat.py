"""Chat endpoints for conversations."""

from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.api.deps import get_db, get_current_user
from app.core.logging import get_logger
from app.models.user import User
from app.models.conversation import ConversationSession, ChatMessage
from app.schemas.conversation import (
    ChatMessageSend,
    ChatResponse,
    ConversationSessionResponse,
    ConversationSessionWithMessages,
    ConversationSessionList,
)
from app.services.claude import claude_service

router = APIRouter()
logger = get_logger(__name__)


@router.post("/send", response_model=ChatResponse)
async def send_message(
    message_data: ChatMessageSend,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Send a message and get AI response."""
    # Get or create session
    if message_data.session_id:
        # Get existing session
        result = await db.execute(
            select(ConversationSession)
            .where(
                ConversationSession.id == message_data.session_id,
                ConversationSession.user_id == current_user.id,
            )
        )
        session = result.scalar_one_or_none()

        if not session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Conversation session not found",
            )
    else:
        # Create new session
        session = ConversationSession(
            user_id=current_user.id,
            title=message_data.message[:50] + "..." if len(message_data.message) > 50 else message_data.message,
            is_active=True,
        )
        db.add(session)
        await db.flush()

    # Save user message
    user_message = ChatMessage(
        session_id=session.id,
        user_id=current_user.id,
        content=message_data.message,
        sender="user",
    )
    db.add(user_message)
    await db.flush()

    # Get conversation history for context
    history_result = await db.execute(
        select(ChatMessage)
        .where(ChatMessage.session_id == session.id)
        .order_by(ChatMessage.created_at)
        .limit(20)  # Last 20 messages for context
    )
    history_messages = history_result.scalars().all()

    # Format history for Claude (excluding the current message)
    conversation_history = claude_service.format_conversation_history(
        [(msg.sender, msg.content) for msg in history_messages[:-1]],
        max_messages=10,
    )

    try:
        # Generate AI response
        ai_response_text, tokens_used = await claude_service.generate_response(
            user_message=message_data.message,
            conversation_history=conversation_history,
        )

        # Save AI message
        ai_message = ChatMessage(
            session_id=session.id,
            user_id=current_user.id,
            content=ai_response_text,
            sender="ai",
            tokens_used=tokens_used,
        )
        db.add(ai_message)

        await db.commit()
        await db.refresh(user_message)
        await db.refresh(ai_message)
        await db.refresh(session)

        logger.info(f"Message sent in session {session.id} - tokens used: {tokens_used}")

        return ChatResponse(
            session_id=session.id,
            user_message=user_message,
            ai_message=ai_message,
        )

    except Exception as e:
        await db.rollback()
        logger.error(f"Error generating AI response: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate AI response: {str(e)}",
        )


@router.get("/sessions", response_model=ConversationSessionList)
async def get_sessions(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
):
    """Get user's conversation sessions."""
    # Get total count
    count_result = await db.execute(
        select(ConversationSession)
        .where(ConversationSession.user_id == current_user.id)
    )
    total = len(count_result.scalars().all())

    # Get paginated sessions
    offset = (page - 1) * page_size
    result = await db.execute(
        select(ConversationSession)
        .where(ConversationSession.user_id == current_user.id)
        .order_by(desc(ConversationSession.started_at))
        .limit(page_size)
        .offset(offset)
    )
    sessions = result.scalars().all()

    return ConversationSessionList(
        sessions=sessions,
        total=total,
        page=page,
        page_size=page_size,
    )


@router.get("/sessions/{session_id}", response_model=ConversationSessionWithMessages)
async def get_session(
    session_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get a conversation session with messages."""
    result = await db.execute(
        select(ConversationSession)
        .options(selectinload(ConversationSession.messages))
        .where(
            ConversationSession.id == session_id,
            ConversationSession.user_id == current_user.id,
        )
    )
    session = result.scalar_one_or_none()

    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation session not found",
        )

    return session


@router.delete("/sessions/{session_id}")
async def delete_session(
    session_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Delete a conversation session."""
    result = await db.execute(
        select(ConversationSession)
        .where(
            ConversationSession.id == session_id,
            ConversationSession.user_id == current_user.id,
        )
    )
    session = result.scalar_one_or_none()

    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation session not found",
        )

    await db.delete(session)
    await db.commit()

    logger.info(f"Session deleted: {session_id}")

    return {"message": "Session deleted successfully"}
