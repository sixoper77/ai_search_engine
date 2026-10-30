import React, { useState, useEffect, useCallback, useRef } from 'react';
import {
  fetchChats,
  fetchChatHistory,
  fetchProviders,
  streamSearch,
} from './api';
import {
  ChatItem,
  MessageOut,
  ResearchStep,
  SiteSource,
  SSEEvent,
} from './types';
import { Sidebar } from './components/Sidebar';
import { Header } from './components/Header';
import { PerplexityHero } from './components/PerplexityHero';
import { SearchInput } from './components/SearchInput';
import { FourCardsGrid } from './components/FourCardsGrid';
import { ResearchProgress } from './components/ResearchProgress';
import { MessageList } from './components/MessageList';
import { ImageLightbox } from './components/ImageLightbox';

export const App: React.FC = () => {
  // Navigation & responsive state
  const [isMobile, setIsMobile] = useState<boolean>(() => {
    return typeof window !== 'undefined' ? window.innerWidth < 768 : false;
  });
  const [isSidebarOpen, setIsSidebarOpen] = useState<boolean>(() => {
    return typeof window !== 'undefined' ? window.innerWidth >= 768 : true;
  });

  // Chats state
  const [chats, setChats] = useState<ChatItem[]>([]);
  const [activeChatId, setActiveChatId] = useState<string | undefined>(undefined);
  const [activeChatName, setActiveChatName] = useState<string | null>(null);
  const [isLoadingMoreChats, setIsLoadingMoreChats] = useState<boolean>(false);
  const [hasMoreChats, setHasMoreChats] = useState<boolean>(true);

  // Messages in current chat
  const [messages, setMessages] = useState<MessageOut[]>([]);
  const [isLoadingHistory, setIsLoadingHistory] = useState<boolean>(false);

  // Query & search controls
  const [query, setQuery] = useState<string>('');
  const [proSearch, setProSearch] = useState<boolean>(false);
  const [provider, setProvider] = useState<string>(() => {
    try {
      return (typeof window !== 'undefined' && window.localStorage?.getItem('ai_search_provider')) || 'tavily';
    } catch {
      return 'tavily';
    }
  });
  const [availableProviders, setAvailableProviders] = useState<string[]>([
    'tavily',
    'serper',
    'searxng',
  ]);
  const [isSearching, setIsSearching] = useState<boolean>(false);

  // Active streaming state
  const [activeStreamingMessage, setActiveStreamingMessage] = useState<string | undefined>(undefined);
  const [streamingPhotos, setStreamingPhotos] = useState<string[]>([]);
  const [isLoadingPhotos, setIsLoadingPhotos] = useState<boolean>(false);
  const [researchSteps, setResearchSteps] = useState<ResearchStep[]>([]);
  const [researchSites, setResearchSites] = useState<SiteSource[]>([]);
  const [researchDoneMessage, setResearchDoneMessage] = useState<string | undefined>(undefined);

  // Lightbox preview image
  const [lightboxImage, setLightboxImage] = useState<string | null>(null);

  const abortControllerRef = useRef<AbortController | null>(null);
  const chatBottomRef = useRef<HTMLDivElement>(null);
  const typewriterTimerRef = useRef<any>(null);

  // Load available providers from backend
  useEffect(() => {
    fetchProviders()
      .then((data) => {
        if (data.providers?.length) {
          setAvailableProviders(data.providers);
        }
        try {
          const saved = typeof window !== 'undefined' && window.localStorage?.getItem('ai_search_provider');
          if (!saved && data.default) {
            setProvider(data.default);
          }
        } catch {
          if (data.default) setProvider(data.default);
        }
      })
      .catch((err) => console.warn('Failed to load providers:', err));
  }, []);

  const handleSelectProvider = useCallback((newProv: string) => {
    setProvider(newProv);
    try {
      if (typeof window !== 'undefined' && window.localStorage) {
        window.localStorage.setItem('ai_search_provider', newProv);
      }
    } catch {
      // ignore
    }
  }, []);

  // Handle window resizing for mobile detection
  useEffect(() => {
    const handleResize = () => {
      const mobile = window.innerWidth < 768;
      setIsMobile(mobile);
      if (mobile && isSidebarOpen) {
        setIsSidebarOpen(false);
      }
    };
    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, [isSidebarOpen]);

  // Load initial chats list
  const loadInitialChats = useCallback(async () => {
    try {
      const initial = await fetchChats();
      setChats(initial);
      setHasMoreChats(initial.length >= 20);
    } catch (e) {
      console.error('Failed to load initial chats:', e);
    }
  }, []);

  useEffect(() => {
    loadInitialChats();
  }, [loadInitialChats]);

  // Infinite scroll: load more chats using cursor
  const handleLoadMoreChats = useCallback(async () => {
    if (isLoadingMoreChats || !hasMoreChats || chats.length === 0) return;

    setIsLoadingMoreChats(true);
    try {
      const lastChat = chats[chats.length - 1];
      const olderChats = await fetchChats(lastChat.updated_at, lastChat.id);

      if (olderChats.length === 0) {
        setHasMoreChats(false);
      } else {
        setChats((prev) => [...prev, ...olderChats]);
        if (olderChats.length < 20) {
          setHasMoreChats(false);
        }
      }
    } catch (err) {
      console.error('Failed to load more chats:', err);
    } finally {
      setIsLoadingMoreChats(false);
    }
  }, [chats, hasMoreChats, isLoadingMoreChats]);

  // Switch to a new empty chat
  const handleNewChat = useCallback(() => {
    if (abortControllerRef.current) {
      abortControllerRef.current.abort();
    }
    if (typewriterTimerRef.current) {
      clearInterval(typewriterTimerRef.current);
      typewriterTimerRef.current = null;
    }
    setActiveChatId(undefined);
    setActiveChatName(null);
    setMessages([]);
    setQuery('');
    setActiveStreamingMessage(undefined);
    setStreamingPhotos([]);
    setIsLoadingPhotos(false);
    setResearchSteps([]);
    setResearchSites([]);
    setResearchDoneMessage(undefined);
    if (isMobile) setIsSidebarOpen(false);
  }, [isMobile]);

  // Select an existing chat
  const handleSelectChat = useCallback(
    async (chatId: string) => {
      if (activeChatId === chatId) return;
      if (abortControllerRef.current) {
        abortControllerRef.current.abort();
      }
      if (typewriterTimerRef.current) {
        clearInterval(typewriterTimerRef.current);
        typewriterTimerRef.current = null;
      }

      const selected = chats.find((c) => c.id === chatId);
      setActiveChatId(chatId);
      setActiveChatName(selected?.name || null);
      setQuery('');
      setActiveStreamingMessage(undefined);
      setStreamingPhotos([]);
      setIsLoadingPhotos(false);
      setResearchSteps([]);
      setResearchSites([]);
      setResearchDoneMessage(undefined);

      if (isMobile) setIsSidebarOpen(false);

      setIsLoadingHistory(true);
      try {
        const history = await fetchChatHistory(chatId);
        setMessages(history);
      } catch (err) {
        console.error('Failed to load chat history:', err);
      } finally {
        setIsLoadingHistory(false);
      }
    },
    [activeChatId, chats, isMobile]
  );

  // Auto-scroll to bottom of chat when streaming
  useEffect(() => {
    if (isSearching || activeStreamingMessage !== undefined) {
      chatBottomRef.current?.scrollIntoView({ behavior: 'smooth' });
    }
  }, [isSearching, activeStreamingMessage, streamingPhotos, researchSteps]);

  // Execute Search query
  const handleSearchSubmit = useCallback(
    async (submittedQuery?: string) => {
      const q = (submittedQuery || query).trim();
      if (!q || isSearching) return;

      setQuery('');
      setIsSearching(true);
      setIsLoadingPhotos(true);
      setStreamingPhotos([]);
      setActiveStreamingMessage('');
      setResearchSteps([]);
      setResearchSites([]);
      setResearchDoneMessage(undefined);

      // Append user query to UI message list immediately
      const tempUserMsg: MessageOut = {
        id: Date.now(),
        chat_id: activeChatId || 'temp',
        role: 'user',
        content: q,
        steps: [],
      };
      setMessages((prev) => [...prev, tempUserMsg]);

      const controller = new AbortController();
      abortControllerRef.current = controller;

      let currentChatId = activeChatId;
      let targetFullText = '';
      let displayedLength = 0;
      let isStreamFinished = false;
      const gatheredPhotos: string[] = [];
      const gatheredSites: SiteSource[] = [];

      if (typewriterTimerRef.current) {
        clearInterval(typewriterTimerRef.current);
      }

      const tickTypewriter = (forceAll = false) => {
        if (forceAll) {
          displayedLength = targetFullText.length;
          setActiveStreamingMessage(targetFullText);
          if (typewriterTimerRef.current) {
            clearInterval(typewriterTimerRef.current);
            typewriterTimerRef.current = null;
          }
          return;
        }

        const remaining = targetFullText.length - displayedLength;
        if (remaining <= 0) {
          if (isStreamFinished && typewriterTimerRef.current) {
            clearInterval(typewriterTimerRef.current);
            typewriterTimerRef.current = null;
          }
          return;
        }

        let step = 1;
        if (remaining > 100) step = Math.ceil(remaining / 4);
        else if (remaining > 40) step = 4;
        else if (remaining > 15) step = 2;

        displayedLength = Math.min(displayedLength + step, targetFullText.length);
        setActiveStreamingMessage(targetFullText.slice(0, displayedLength));
      };

      typewriterTimerRef.current = setInterval(() => {
        tickTypewriter(false);
      }, 15);

      await streamSearch({
        q,
        proSearch,
        providerName: provider,
        chatId: currentChatId,
        signal: controller.signal,
        onEvent: (event: SSEEvent) => {
          switch (event.type) {
            case 'chat_id': {
              currentChatId = event.chat_id;
              setActiveChatId(event.chat_id);
              break;
            }
            case 'chat_name': {
              setActiveChatName(event.name);
              setChats((prev) =>
                prev.map((c) =>
                  c.id === currentChatId ? { ...c, name: event.name } : c
                )
              );
              break;
            }
            case 'step_start': {
              setResearchSteps((prev) => [
                ...prev,
                { step: event.step, message: event.messgae },
              ]);
              break;
            }
            case 'sites_info': {
              gatheredSites.push(...event.sources);
              setResearchSites((prev) => [...prev, ...event.sources]);
              break;
            }
            case 'info': {
              setResearchSteps((prev) => {
                if (prev.length === 0) return prev;
                const copy = [...prev];
                copy[copy.length - 1] = {
                  ...copy[copy.length - 1],
                  info: event.message,
                };
                return copy;
              });
              break;
            }
            case 'need_more_data': {
              setResearchSteps((prev) => {
                if (prev.length === 0) return prev;
                const copy = [...prev];
                copy[copy.length - 1] = {
                  ...copy[copy.length - 1],
                  reason: event.reason,
                  newQueries: event.new_queries,
                };
                return copy;
              });
              break;
            }
            case 'done': {
              setResearchDoneMessage(event.message);
              break;
            }
            case 'photos': {
              // 4 Photos arrive BEFORE token stream!
              setIsLoadingPhotos(false);
              const newPhotos = event.photos || [];
              gatheredPhotos.push(...newPhotos);
              setStreamingPhotos(newPhotos);
              break;
            }
            case 'token': {
              targetFullText += event.token;
              tickTypewriter(false);
              break;
            }
            case 'error': {
              console.error('SSE Error:', event.message);
              break;
            }
          }
        },
        onDone: () => {
          isStreamFinished = true;
          const finalize = () => {
            if (typewriterTimerRef.current) {
              clearInterval(typewriterTimerRef.current);
              typewriterTimerRef.current = null;
            }
            if (targetFullText.trim()) {
              const aiMsg: MessageOut = {
                id: Date.now() + 1,
                chat_id: currentChatId || '',
                role: 'ai',
                content: targetFullText,
                steps: gatheredSites.map((s, idx) => ({
                  id: idx,
                  title: s.title,
                  url: s.url,
                  step_number: idx + 1,
                  message_id: 0,
                })),
                photos: gatheredPhotos.length > 0 ? gatheredPhotos : undefined,
              };
              setMessages((prev) => [...prev, aiMsg]);
            }

            setIsSearching(false);
            setActiveStreamingMessage(undefined);
            setStreamingPhotos([]);
            setIsLoadingPhotos(false);
            loadInitialChats();
          };

          const remaining = targetFullText.length - displayedLength;
          if (remaining > 0 && remaining < 60) {
            setTimeout(finalize, 120);
          } else {
            tickTypewriter(true);
            finalize();
          }
        },
        onError: (err) => {
          if (typewriterTimerRef.current) {
            clearInterval(typewriterTimerRef.current);
            typewriterTimerRef.current = null;
          }
          console.error('Search error:', err);
          setIsSearching(false);
          setActiveStreamingMessage(undefined);
          setIsLoadingPhotos(false);
        },
      });
    },
    [activeChatId, isSearching, loadInitialChats, proSearch, provider, query]
  );

  const hasMessages = messages.length > 0 || activeStreamingMessage !== undefined;

  return (
    <div className="flex h-screen w-screen overflow-hidden bg-[#191A1A] text-[#EBEBEB] font-sans antialiased">
      {/* Sidebar with Infinite Scroll */}
      <Sidebar
        chats={chats}
        activeChatId={activeChatId}
        onSelectChat={handleSelectChat}
        onNewChat={handleNewChat}
        isLoadingMore={isLoadingMoreChats}
        hasMoreChats={hasMoreChats}
        onLoadMoreChats={handleLoadMoreChats}
        isOpen={isSidebarOpen}
        onToggleSidebar={() => setIsSidebarOpen(!isSidebarOpen)}
        isMobile={isMobile}
      />

      {/* Main Content Area */}
      <div className="flex flex-col flex-1 h-full min-w-0 overflow-hidden relative">
        {/* Sticky Mobile/Desktop Top Header */}
        <Header
          onToggleSidebar={() => setIsSidebarOpen(!isSidebarOpen)}
          onNewChat={handleNewChat}
          isSidebarOpen={isSidebarOpen}
          isMobile={isMobile}
          chatTitle={activeChatName}
          proSearch={proSearch}
        />

        {/* Scrollable Center View */}
        <main className="flex-1 overflow-y-auto px-4 py-4 sm:px-6 md:px-8 flex flex-col items-center custom-scrollbar">
          {!hasMessages ? (
            /* Home / Initial Empty Chat State */
            <div className="w-full max-w-3xl flex flex-col items-center my-auto py-8">
              <PerplexityHero />

              <SearchInput
                query={query}
                onChangeQuery={setQuery}
                onSubmit={() => handleSearchSubmit()}
                isLoading={isSearching}
                proSearch={proSearch}
                onToggleProSearch={() => setProSearch(!proSearch)}
                provider={provider}
                onSelectProvider={handleSelectProvider}
                availableProviders={availableProviders}
              />

              {/* 4 Cards Grid (matches screenshot) */}
              <FourCardsGrid
                onSelectPrompt={(p) => {
                  setQuery(p);
                  handleSearchSubmit(p);
                }}
              />
            </div>
          ) : (
            /* Active Chat View */
            <div className="w-full max-w-3xl flex flex-col flex-1 pb-24">
              <MessageList
                messages={messages}
                activeStreamingMessage={activeStreamingMessage}
                streamingPhotos={streamingPhotos}
                isLoadingPhotos={isLoadingPhotos}
                onSelectImage={(url) => setLightboxImage(url)}
              />

              {/* Active Research Progress */}
              {isSearching && (
                <ResearchProgress
                  steps={researchSteps}
                  allSites={researchSites}
                  isSearching={isSearching}
                  doneMessage={researchDoneMessage}
                />
              )}

              <div ref={chatBottomRef} />
            </div>
          )}

          {/* Sticky Bottom Search Input when in chat mode */}
          {hasMessages && (
            <div className="sticky bottom-0 w-full max-w-3xl pb-4 pt-2 bg-gradient-to-t from-[#191A1A] via-[#191A1A]/95 to-transparent z-20">
              <SearchInput
                query={query}
                onChangeQuery={setQuery}
                onSubmit={() => handleSearchSubmit()}
                isLoading={isSearching}
                proSearch={proSearch}
                onToggleProSearch={() => setProSearch(!proSearch)}
                provider={provider}
                onSelectProvider={handleSelectProvider}
                availableProviders={availableProviders}
                placeholder="Задайте уточняющий вопрос..."
              />
            </div>
          )}
        </main>
      </div>

      {/* Image Lightbox Modal */}
      <ImageLightbox
        imageUrl={lightboxImage}
        onClose={() => setLightboxImage(null)}
      />
    </div>
  );
};

export default App;
