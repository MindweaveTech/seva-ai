/**
 * Chat API service
 */

import apiClient from './client';

export interface ChatMessage {
  id: string;
  session_id: string;
  user_id: string;
  content: string;
  sender: 'user' | 'ai';
  sentiment_score: number | null;
  sentiment_label: string | null;
  health_signals: any[];
  tokens_used: number | null;
  created_at: string;
  metadata: Record<string, any>;
}

export interface ConversationSession {
  id: string;
  user_id: string;
  title: string | null;
  started_at: string;
  ended_at: string | null;
  message_count: number;
  is_active: boolean;
  metadata: Record<string, any>;
}

export interface ConversationSessionWithMessages extends ConversationSession {
  messages: ChatMessage[];
}

export interface ChatResponse {
  session_id: string;
  user_message: ChatMessage;
  ai_message: ChatMessage;
}

export interface SessionListResponse {
  sessions: ConversationSession[];
  total: number;
  page: number;
  page_size: number;
}

export interface SendMessageData {
  message: string;
  session_id?: string;
}

class ChatService {
  /**
   * Send a message and get AI response
   */
  async sendMessage(data: SendMessageData): Promise<ChatResponse> {
    const response = await apiClient.post<ChatResponse>('/chat/send', data);
    return response.data;
  }

  /**
   * Get list of conversation sessions
   */
  async getSessions(page: number = 1, pageSize: number = 20): Promise<SessionListResponse> {
    const response = await apiClient.get<SessionListResponse>('/chat/sessions', {
      params: { page, page_size: pageSize },
    });
    return response.data;
  }

  /**
   * Get a specific session with messages
   */
  async getSession(sessionId: string): Promise<ConversationSessionWithMessages> {
    const response = await apiClient.get<ConversationSessionWithMessages>(
      `/chat/sessions/${sessionId}`
    );
    return response.data;
  }

  /**
   * Delete a conversation session
   */
  async deleteSession(sessionId: string): Promise<void> {
    await apiClient.delete(`/chat/sessions/${sessionId}`);
  }
}

export default new ChatService();
