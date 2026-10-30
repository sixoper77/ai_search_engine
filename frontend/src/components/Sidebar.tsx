import React, { useRef, useEffect, useCallback } from 'react';
import {
  Plus,
  Monitor,
  Compass,
  Layers,
  Settings,
  ChevronDown,
  MessageSquare,
  Sparkles,
  User,
  PanelLeftClose,
  PanelLeft,
  Loader2,
  X,
  Search,
} from 'lucide-react';
import { ChatItem } from '../types';
import { PerplexityIcon } from './PerplexityIcon';

interface SidebarProps {
  chats: ChatItem[];
  activeChatId?: string;
  onSelectChat: (chatId: string) => void;
  onNewChat: () => void;
  isLoadingMore: boolean;
  hasMoreChats: boolean;
  onLoadMoreChats: () => void;
  isOpen: boolean;
  onToggleSidebar: () => void;
  isMobile: boolean;
}

export const Sidebar: React.FC<SidebarProps> = ({
  chats,
  activeChatId,
  onSelectChat,
  onNewChat,
  isLoadingMore,
  hasMoreChats,
  onLoadMoreChats,
  isOpen,
  onToggleSidebar,
  isMobile,
}) => {
  const scrollContainerRef = useRef<HTMLDivElement>(null);

  // Infinite scroll trigger: when user scrolls near the bottom of recent chats list
  const handleScroll = useCallback(() => {
    const el = scrollContainerRef.current;
    if (!el || isLoadingMore || !hasMoreChats) return;

    const scrollBottom = el.scrollHeight - el.scrollTop - el.clientHeight;
    // Trigger when within 80px from bottom
    if (scrollBottom < 80) {
      onLoadMoreChats();
    }
  }, [isLoadingMore, hasMoreChats, onLoadMoreChats]);

  useEffect(() => {
    const el = scrollContainerRef.current;
    if (!el) return;
    el.addEventListener('scroll', handleScroll, { passive: true });
    return () => el.removeEventListener('scroll', handleScroll);
  }, [handleScroll]);

  // Sidebar container classes for desktop and mobile slide-over
  const sidebarClasses = isMobile
    ? `fixed inset-y-0 left-0 z-50 w-72 bg-[#191A1A] border-r border-[#262929] flex flex-col transition-transform duration-300 ease-in-out ${
        isOpen ? 'translate-x-0' : '-translate-x-full'
      }`
    : `relative flex flex-col w-64 bg-[#191A1A] border-r border-[#242727] flex-shrink-0 transition-all duration-300 ease-in-out select-none ${
        isOpen ? 'w-64' : 'w-0 overflow-hidden border-none'
      }`;

  return (
    <>
      {/* Mobile backdrop overlay */}
      {isMobile && isOpen && (
        <div
          className="fixed inset-0 z-40 bg-black/60 backdrop-blur-sm transition-opacity"
          onClick={onToggleSidebar}
        />
      )}

      <aside className={sidebarClasses}>
        {/* Top Header: Logo & action icons */}
        <div className="flex items-center justify-between p-3.5 pb-2">
          <div className="flex items-center gap-2 cursor-pointer" onClick={onNewChat}>
            <div className="w-8 h-8 rounded-lg bg-[#202222] border border-[#2D3131] flex items-center justify-center text-[#20808D] hover:scale-105 transition-transform">
              <PerplexityIcon size={20} />
            </div>
            <span className="font-semibold text-[15px] tracking-tight text-white">
              Perplexity
            </span>
          </div>

          <div className="flex items-center gap-1">
            <button
              onClick={onNewChat}
              className="p-1.5 text-[#9B9C9E] hover:text-white rounded-lg hover:bg-[#252828] transition-colors"
              title="Поиск / Новый чат"
            >
              <Search className="w-4 h-4" />
            </button>
            <button
              onClick={onToggleSidebar}
              className="p-1.5 text-[#9B9C9E] hover:text-white rounded-lg hover:bg-[#252828] transition-colors"
              title={isMobile ? 'Закрыть меню' : 'Скрыть панель'}
            >
              {isMobile ? <X className="w-4 h-4" /> : <PanelLeftClose className="w-4 h-4" />}
            </button>
          </div>
        </div>

        {/* Primary Action Button: "Новый чат" */}
        <div className="px-3 py-2">
          <button
            onClick={onNewChat}
            className="w-full flex items-center gap-2 px-3.5 py-2.5 rounded-full bg-[#202222] hover:bg-[#282B2B] border border-[#2D3131] hover:border-[#3E4343] text-sm font-medium text-white shadow-sm transition-all duration-150 group"
          >
            <Plus className="w-4 h-4 text-[#20808D] group-hover:scale-110 transition-transform" />
            <span className="tracking-tight">Новый чат</span>
          </button>
        </div>

        {/* Main Navigation Links */}
        <div className="px-3 py-1 space-y-0.5">
          <button className="w-full flex items-center gap-3 px-3 py-2 rounded-xl text-xs font-medium text-[#A3A3A3] hover:text-white hover:bg-[#202222] transition-colors">
            <Monitor className="w-4 h-4 text-[#8A8D8F]" />
            <span>Компьютер</span>
          </button>
          <button className="w-full flex items-center gap-3 px-3 py-2 rounded-xl text-xs font-medium text-[#A3A3A3] hover:text-white hover:bg-[#202222] transition-colors">
            <Compass className="w-4 h-4 text-[#8A8D8F]" />
            <span>Автоматизации</span>
          </button>
          <button className="w-full flex items-center gap-3 px-3 py-2 rounded-xl text-xs font-medium text-[#A3A3A3] hover:text-white hover:bg-[#202222] transition-colors">
            <Layers className="w-4 h-4 text-[#8A8D8F]" />
            <span>Артефакты</span>
          </button>
          <button className="w-full flex items-center gap-3 px-3 py-2 rounded-xl text-xs font-medium text-[#A3A3A3] hover:text-white hover:bg-[#202222] transition-colors">
            <Settings className="w-4 h-4 text-[#8A8D8F]" />
            <span>Настройка</span>
          </button>
        </div>

        {/* Separator Line */}
        <div className="mx-3 my-2 border-t border-[#242727]" />

        {/* Scrollable Chats Container (Infinite Scroll) */}
        <div
          ref={scrollContainerRef}
          data-testid="sidebar-chats-scroll"
          className="flex-1 overflow-y-auto px-3 py-1 space-y-3 custom-scrollbar"
        >
          {/* Projects Collapsible Section */}
          <div>
            <button className="w-full flex items-center justify-between py-1 text-xs font-medium text-[#6E7173] hover:text-[#9B9C9E] transition-colors">
              <span>Проекты</span>
              <ChevronDown className="w-3.5 h-3.5" />
            </button>
            <p className="text-[11px] text-[#55585A] py-1 px-1">Нет проектов</p>
          </div>

          {/* Recent Chats Section ("Недавние") */}
          <div>
            <div className="flex items-center justify-between py-1 text-xs font-medium text-[#6E7173]">
              <span>Недавние</span>
              <ChevronDown className="w-3.5 h-3.5" />
            </div>

            {chats.length === 0 && !isLoadingMore ? (
              <p className="text-[11px] text-[#55585A] py-1 px-1">Нет недавних сессий</p>
            ) : (
              <div className="space-y-0.5 mt-1">
                {chats.map((chat) => {
                  const isActive = chat.id === activeChatId;
                  const chatTitle = chat.name || 'Новый поиск';

                  return (
                    <button
                      key={chat.id}
                      onClick={() => onSelectChat(chat.id)}
                      className={`w-full text-left px-2.5 py-1.5 rounded-lg text-xs truncate transition-all duration-150 flex items-center gap-2 ${
                        isActive
                          ? 'bg-[#202222] text-white font-medium border border-[#2D3131]'
                          : 'text-[#A3A3A3] hover:text-[#E0E0E0] hover:bg-[#1E2020]'
                      }`}
                      title={chatTitle}
                    >
                      <MessageSquare className={`w-3.5 h-3.5 flex-shrink-0 ${isActive ? 'text-[#20808D]' : 'text-[#6E7173]'}`} />
                      <span className="truncate">{chatTitle}</span>
                    </button>
                  );
                })}
              </div>
            )}

            {/* Loading indicator for infinite scroll */}
            {isLoadingMore && (
              <div className="flex items-center justify-center py-3 text-[#20808D]">
                <Loader2 className="w-4 h-4 animate-spin" />
              </div>
            )}
          </div>
        </div>

        {/* Bottom Section: Plans & User Profile */}
        <div className="p-3 border-t border-[#242727] space-y-1">
          <button className="w-full flex items-center gap-2.5 px-3 py-2 rounded-xl text-xs font-medium text-[#A3A3A3] hover:text-white hover:bg-[#202222] transition-colors">
            <Sparkles className="w-4 h-4 text-[#20808D]" />
            <span>Посмотреть планы</span>
          </button>

          <button className="w-full flex items-center justify-between px-3 py-2 rounded-xl text-xs font-medium text-white hover:bg-[#202222] transition-colors">
            <div className="flex items-center gap-2.5">
              <div className="w-6 h-6 rounded-full bg-[#20808D]/20 border border-[#20808D]/40 flex items-center justify-center text-[#20808D]">
                <User className="w-3.5 h-3.5" />
              </div>
              <span>Войдите</span>
            </div>
            <span className="text-[#6E7173] text-[11px]">&gt;</span>
          </button>
        </div>
      </aside>
    </>
  );
};

