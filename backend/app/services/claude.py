"""Claude API service for AI conversations."""

from typing import List, Dict, Optional
import anthropic

from app.core.config import settings
from app.core.logging import get_logger

logger = get_logger(__name__)


class ClaudeService:
    """Service for interacting with Claude API."""

    def __init__(self):
        """Initialize Claude client."""
        if not settings.ANTHROPIC_API_KEY:
            logger.warning("ANTHROPIC_API_KEY not set - Claude API will not work")
            self.client = None
        else:
            self.client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)

    async def generate_response(
        self,
        user_message: str,
        conversation_history: Optional[List[Dict[str, str]]] = None,
        system_prompt: Optional[str] = None,
        max_tokens: int = 1024,
    ) -> tuple[str, int]:
        """
        Generate AI response using Claude.

        Args:
            user_message: The user's message
            conversation_history: List of previous messages [{"role": "user/assistant", "content": "..."}]
            system_prompt: System prompt for persona
            max_tokens: Maximum tokens in response

        Returns:
            Tuple of (response_text, tokens_used)
        """
        if not self.client:
            raise ValueError("Claude API key not configured")

        # Default nurse persona system prompt
        if not system_prompt:
            system_prompt = """You are a compassionate AI companion designed to support elderly individuals.
You have a warm, patient, and caring personality similar to a skilled nurse. You:
- Listen actively and show genuine interest in their well-being
- Use clear, simple language while being respectful
- Remember details from past conversations
- Gently inquire about their health and daily activities
- Provide emotional support and encouragement
- Never give medical diagnoses but encourage seeking professional help when needed
- Are observant of mood changes or health concerns

Always maintain a friendly, supportive tone and prioritize the user's comfort and well-being."""

        # Build messages array
        messages = []

        # Add conversation history if provided
        if conversation_history:
            messages.extend(conversation_history)

        # Add current user message
        messages.append({
            "role": "user",
            "content": user_message,
        })

        try:
            # Call Claude API
            # Updated to use latest Sonnet 3.5 model (2024-10-22)
            response = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",  # Latest Sonnet 3.5
                max_tokens=max_tokens,
                system=system_prompt,
                messages=messages,
            )

            # Extract response text
            response_text = response.content[0].text

            # Get token usage
            tokens_used = response.usage.input_tokens + response.usage.output_tokens

            logger.info(f"Claude response generated - tokens used: {tokens_used}")

            return response_text, tokens_used

        except anthropic.APIError as e:
            logger.error(f"Claude API error: {str(e)}")
            raise ValueError(f"Failed to generate AI response: {str(e)}")

    def format_conversation_history(
        self,
        messages: List[tuple[str, str]],  # [(sender, content), ...]
        max_messages: int = 10,
    ) -> List[Dict[str, str]]:
        """
        Format conversation history for Claude API.

        Args:
            messages: List of (sender, content) tuples
            max_messages: Maximum number of recent messages to include

        Returns:
            Formatted messages for Claude API
        """
        formatted = []

        # Take only recent messages
        recent_messages = messages[-max_messages:] if len(messages) > max_messages else messages

        for sender, content in recent_messages:
            role = "user" if sender == "user" else "assistant"
            formatted.append({
                "role": role,
                "content": content,
            })

        return formatted


# Global Claude service instance
claude_service = ClaudeService()
