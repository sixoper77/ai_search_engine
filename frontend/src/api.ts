import { ChatItem, MessageOut, SSEEvent } from './types';

const API_BASE = '/api';

export async function fetchChats(
  beforeUpdatedAt?: string,
  beforeId?: string
): Promise<ChatItem[]> {
  const params = new URLSearchParams();
  if (beforeUpdatedAt) params.set('before_updated_at', beforeUpdatedAt);
  if (beforeId) params.set('before_id', beforeId);

  const url = `${API_BASE}/chats/${params.toString() ? `?${params.toString()}` : ''}`;
  const response = await fetch(url);
  if (!response.ok) {
    throw new Error(`Failed to fetch chats: ${response.statusText}`);
  }
  return response.json();
}

export async function fetchChatHistory(chatId: string): Promise<MessageOut[]> {
  const response = await fetch(`${API_BASE}/chat/${chatId}`);
  if (!response.ok) {
    throw new Error(`Failed to fetch chat history: ${response.statusText}`);
  }
  return response.json();
}

export async function fetchProviders(): Promise<{ providers: string[]; default: string }> {
  try {
    const response = await fetch(`${API_BASE}/providers/`);
    if (!response.ok) {
      return { providers: ['tavily', 'serper', 'searxng'], default: 'tavily' };
    }
    return response.json();
  } catch {
    return { providers: ['tavily', 'serper', 'searxng'], default: 'tavily' };
  }
}

export interface StreamSearchParams {
  q: string;
  proSearch: boolean;
  providerName?: string;
  chatId?: string;
  signal?: AbortSignal;
  onEvent: (event: SSEEvent) => void;
  onDone: () => void;
  onError: (error: Error) => void;
}

export async function streamSearch({
  q,
  proSearch,
  providerName,
  chatId,
  signal,
  onEvent,
  onDone,
  onError,
}: StreamSearchParams): Promise<void> {
  const params = new URLSearchParams();
  params.set('q', q);
  params.set('pro_search', String(proSearch));
  if (providerName) params.set('provider_name', providerName);
  if (chatId) params.set('chat_id', chatId);

  const url = `${API_BASE}/search/?${params.toString()}`;

  try {
    const response = await fetch(url, {
      method: 'GET',
      headers: {
        Accept: 'text/event-stream',
      },
      signal,
    });

    if (!response.ok) {
      throw new Error(`Search request failed with status ${response.status}`);
    }

    const headerChatId = response.headers.get('X-Chat-Id');
    if (headerChatId) {
      onEvent({ type: 'chat_id', chat_id: headerChatId });
    }

    if (!response.body) {
      throw new Error('Response body is null');
    }

    const reader = response.body.getReader();
    const decoder = new TextDecoder('utf-8');
    let buffer = '';

    while (true) {
      const { value, done } = await reader.read();
      if (done) break;

      buffer += decoder.decode(value, { stream: true });
      const lines = buffer.split('\n\n');
      // Keep incomplete trailing chunk in buffer
      buffer = lines.pop() || '';

      for (const block of lines) {
        const trimmed = block.trim();
        if (!trimmed) continue;

        // Process SSE lines
        const dataLines = trimmed
          .split('\n')
          .filter((line) => line.startsWith('data:'))
          .map((line) => line.replace(/^data:\s*/, ''));

        for (const dataStr of dataLines) {
          if (!dataStr) continue;
          try {
            const parsed = JSON.parse(dataStr) as SSEEvent;
            onEvent(parsed);
          } catch (e) {
            console.warn('Failed to parse SSE line:', dataStr, e);
          }
        }
      }
    }

    // Flush any remaining buffer if present
    if (buffer.trim()) {
      const dataLines = buffer
        .trim()
        .split('\n')
        .filter((line) => line.startsWith('data:'))
        .map((line) => line.replace(/^data:\s*/, ''));

      for (const dataStr of dataLines) {
        if (!dataStr) continue;
        try {
          const parsed = JSON.parse(dataStr) as SSEEvent;
          onEvent(parsed);
        } catch (e) {
          console.warn('Failed to parse final SSE buffer:', dataStr, e);
        }
      }
    }

    onDone();
  } catch (err: any) {
    if (signal?.aborted) {
      return;
    }
    onError(err instanceof Error ? err : new Error(String(err)));
  }
}

