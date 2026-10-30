import React from 'react';
import { Menu, Plus, PanelLeftOpen, Sparkles } from 'lucide-react';
import { PerplexityIcon } from './PerplexityIcon';

interface HeaderProps {
  onToggleSidebar: () => void;
  onNewChat: () => void;
  isSidebarOpen: boolean;
  isMobile: boolean;
  chatTitle?: string | null;
  proSearch?: boolean;
}

export const Header: React.FC<HeaderProps> = ({
  onToggleSidebar,
  onNewChat,
  isSidebarOpen,
  isMobile,
  chatTitle,
  proSearch,
}) => {
  return (
    <header className="sticky top-0 z-30 flex items-center justify-between px-4 py-3 bg-[#191A1A]/85 backdrop-blur-md border-b border-[#242727]/60">
      <div className="flex items-center gap-2.5">
        {/* Toggle sidebar button */}
        {(!isSidebarOpen || isMobile) && (
          <button
            onClick={onToggleSidebar}
            aria-label={isMobile ? "Открыть меню навигации" : "Показать боковую панель"}
            className="p-1.5 text-[#9B9C9E] hover:text-white rounded-lg hover:bg-[#202222] transition-colors focus:outline-none"
            title="Открыть меню"
          >
            {isMobile ? <Menu className="w-5 h-5" /> : <PanelLeftOpen className="w-5 h-5" />}
          </button>
        )}

        {/* Small Perplexity logo when sidebar is closed or on mobile */}
        {(!isSidebarOpen || isMobile) && (
          <div className="flex items-center gap-1.5 cursor-pointer" onClick={onNewChat}>
            <div className="w-6 h-6 rounded-md bg-[#20808D]/15 text-[#20808D] flex items-center justify-center">
              <PerplexityIcon size={16} />
            </div>
            <span className="font-semibold text-sm text-white tracking-tight">Perplexity</span>
          </div>
        )}

        {/* Current chat title if in a chat */}
        {chatTitle && (
          <span className="hidden sm:inline-block text-xs font-normal text-[#8A8D8F] max-w-xs truncate border-l border-[#2D3131] pl-2.5 ml-1">
            {chatTitle}
          </span>
        )}
      </div>

      <div className="flex items-center gap-2">
        {proSearch && (
          <div className="flex items-center gap-1 px-2.5 py-1 rounded-full bg-[#20808D]/15 border border-[#20808D]/30 text-[11px] font-medium text-[#20808D]">
            <Sparkles className="w-3 h-3" />
            <span>Pro Search</span>
          </div>
        )}

        {/* Mobile New Chat button */}
        <button
          onClick={onNewChat}
          className="flex items-center gap-1.5 px-3 py-1.5 rounded-full bg-[#202222] hover:bg-[#262828] border border-[#2D3131] text-xs font-medium text-[#E0E0E0] hover:text-white transition-all shadow-sm"
        >
          <Plus className="w-3.5 h-3.5 text-[#20808D]" />
          <span className="hidden xs:inline sm:inline">Новый чат</span>
        </button>
      </div>
    </header>
  );
};

