export type Role = 'user' | 'ai';

export interface StepItem {
  id: number;
  title: string;
  url: string;
  step_number: number | null;
  message_id: number;
}

export interface MessageOut {
  id: number;
  chat_id: string;
  role: Role;
  content: string;
  steps: StepItem[];
  photos?: string[];
}

export interface ChatItem {
  id: string;
  name: string | null;
  updated_at: string;
}

export interface SiteSource {
  url: string;
  title: string;
}

// SSE Event types from backend
export type SSEEvent =
  | { type: 'chat_id'; chat_id: string }
  | { type: 'chat_name'; name: string }
  | { type: 'photos'; photos: string[] }
  | { type: 'token'; token: string }
  | { type: 'step_start'; messgae: string; step: number }
  | { type: 'sites_info'; sources: SiteSource[] }
  | { type: 'info'; message: string }
  | { type: 'done'; total_steps: number; total_sources: number; message: string }
  | { type: 'need_more_data'; reason: string; new_queries: string[] }
  | { type: 'error'; message: string; step?: number; recoverable?: boolean };

export interface ResearchStep {
  step: number;
  message: string;
  reason?: string;
  newQueries?: string[];
  info?: string;
  sites?: SiteSource[];
  completed?: boolean;
}

