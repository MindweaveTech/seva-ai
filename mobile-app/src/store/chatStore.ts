/**
 * Chat state management with Zustand
 */

import { create } from 'zustand';
import chatService, {
  ChatMessage,
  ConversationSession,
  ConversationSessionWithMessages,
  ChatResponse,
} from '../services/api/chat';

interface ChatState {
  currentSession: ConversationSessionWithMessages | null;
  sessions: ConversationSession[];
  messages: ChatMessage[];
  isLoading: boolean;
  isSending: boolean;
  error: string | null;

  // Actions
  sendMessage: (message: string, sessionId?: string) => Promise<ChatResponse>;
  loadSessions: (page?: number) => Promise<void>;
  loadSession: (sessionId: string) => Promise<void>;
  deleteSession: (sessionId: string) => Promise<void>;
  startNewSession: () => void;
  clearError: () => void;
}

export const useChatStore = create<ChatState>((set, get) => ({
  currentSession: null,
  sessions: [],
  messages: [],
  isLoading: false,
  isSending: false,
  error: null,

  sendMessage: async (message: string, sessionId?: string) => {
    set({ isSending: true, error: null });

    try {
      const response = await chatService.sendMessage({
        message,
        session_id: sessionId,
      });

      // Update current session if it matches
      const currentSession = get().currentSession;

      if (currentSession && currentSession.id === response.session_id) {
        set({
          currentSession: {
            ...currentSession,
            messages: [
              ...currentSession.messages,
              response.user_message,
              response.ai_message,
            ],
            message_count: currentSession.message_count + 2,
          },
          messages: [
            ...get().messages,
            response.user_message,
            response.ai_message,
          ],
          isSending: false,
        });
      } else {
        // New session created or different session
        set({
          messages: [response.user_message, response.ai_message],
          isSending: false,
        });
      }

      return response;
    } catch (error: any) {
      const errorMessage =
        error.response?.data?.detail || error.message || 'Failed to send message';

      set({
        error: errorMessage,
        isSending: false,
      });

      throw error;
    }
  },

  loadSessions: async (page: number = 1) => {
    set({ isLoading: true, error: null });

    try {
      const response = await chatService.getSessions(page, 20);

      set({
        sessions: response.sessions,
        isLoading: false,
      });
    } catch (error: any) {
      const errorMessage =
        error.response?.data?.detail || error.message || 'Failed to load sessions';

      set({
        error: errorMessage,
        isLoading: false,
      });
    }
  },

  loadSession: async (sessionId: string) => {
    set({ isLoading: true, error: null });

    try {
      const session = await chatService.getSession(sessionId);

      set({
        currentSession: session,
        messages: session.messages,
        isLoading: false,
      });
    } catch (error: any) {
      const errorMessage =
        error.response?.data?.detail || error.message || 'Failed to load session';

      set({
        error: errorMessage,
        isLoading: false,
      });
    }
  },

  deleteSession: async (sessionId: string) => {
    try {
      await chatService.deleteSession(sessionId);

      // Remove from sessions list
      set({
        sessions: get().sessions.filter((s) => s.id !== sessionId),
      });

      // Clear current session if it was deleted
      if (get().currentSession?.id === sessionId) {
        set({
          currentSession: null,
          messages: [],
        });
      }
    } catch (error: any) {
      const errorMessage =
        error.response?.data?.detail || error.message || 'Failed to delete session';

      set({ error: errorMessage });
      throw error;
    }
  },

  startNewSession: () => {
    set({
      currentSession: null,
      messages: [],
    });
  },

  clearError: () => set({ error: null }),
}));
