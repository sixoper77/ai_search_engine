import React, { useRef, useEffect, useState } from 'react';
import { ArrowUp, Check, ChevronDown, Globe, Loader2, Sparkles } from 'lucide-react';

export interface ProviderOption {
  id: string;
  name: string;
  desc: string;
}

export const PROVIDER_OPTIONS: Record<string, { name: string; desc: string }> = {
  tavily: {
    name: 'Tavily AI',
    desc: 'Оптимизированный AI-поиск',
  },
  serper: {
    name: 'Google Serper',
    desc: 'Выдача Google Search',
  },
  searxng: {
    name: 'SearXNG',
    desc: 'Локальный метапоисковик',
  },
};

interface SearchInputProps {
  query: string;
  onChangeQuery: (value: string) => void;
  onSubmit: () => void;
  isLoading: boolean;
  proSearch: boolean;
  onToggleProSearch: () => void;
  provider?: string;
  onSelectProvider?: (provider: string) => void;
  availableProviders?: string[];
  placeholder?: string;
}

export const SearchInput: React.FC<SearchInputProps> = ({
  query,
  onChangeQuery,
  onSubmit,
  isLoading,
  proSearch,
  onToggleProSearch,
  provider = 'tavily',
  onSelectProvider,
  availableProviders = ['tavily', 'serper', 'searxng'],
  placeholder = 'Задайте любой вопрос...',
}) => {
  const textareaRef = useRef<HTMLTextAreaElement>(null);
  const [isProviderMenuOpen, setIsProviderMenuOpen] = useState(false);
  const providerMenuRef = useRef<HTMLDivElement>(null);

  // Auto-resize textarea height to fit content up to 200px
  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
      const scrollHeight = textareaRef.current.scrollHeight;
      textareaRef.current.style.height = `${Math.min(scrollHeight, 200)}px`;
    }
  }, [query]);

  // Click outside to close provider menu
  useEffect(() => {
    const handleClickOutside = (e: MouseEvent) => {
      if (
        providerMenuRef.current &&
        !providerMenuRef.current.contains(e.target as Node)
      ) {
        setIsProviderMenuOpen(false);
      }
    };
    if (isProviderMenuOpen) {
      document.addEventListener('mousedown', handleClickOutside);
    }
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, [isProviderMenuOpen]);

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      if (query.trim() && !isLoading) {
        onSubmit();
      }
    }
  };

  const canSubmit = Boolean(query.trim()) && !isLoading;
  const currentProviderInfo = PROVIDER_OPTIONS[provider] || {
    name: provider,
    desc: 'Поисковый провайдер',
  };

  return (
    <div className="w-full max-w-3xl">
      <div className="relative rounded-2xl border border-[#2D3131] bg-[#202222] shadow-xl focus-within:border-[#3E4343] transition-all duration-200">
        {/* Main Textarea */}
        <textarea
          ref={textareaRef}
          value={query}
          onChange={(e) => onChangeQuery(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder={placeholder}
          rows={2}
          className="w-full resize-none bg-transparent px-4 pt-3.5 pb-2 text-[15px] text-[#EBEBEB] placeholder-[#6E7173] focus:outline-none leading-relaxed"
          style={{ minHeight: '60px' }}
        />

        {/* Bottom bar with Pro Search Switch, Provider Selector and Submit Button */}
        <div className="flex items-center justify-between px-3.5 pb-3 pt-1">
          <div className="flex items-center gap-2">
            {/* Pro Search Switch Box */}
            <button
              type="button"
              onClick={onToggleProSearch}
              aria-pressed={proSearch}
              className={`group flex items-center gap-2 px-3 py-1.5 rounded-full text-xs font-medium border transition-all duration-200 select-none ${
                proSearch
                  ? 'bg-[#20808D]/15 border-[#20808D] text-[#20808D] shadow-[0_0_12px_rgba(32,128,141,0.25)]'
                  : 'bg-[#181A1A] border-[#2D3131] text-[#9B9C9E] hover:border-[#3E4343] hover:text-[#D1D5DB]'
              }`}
              title="Переключить глубокий поиск Pro Search"
            >
              <Sparkles
                className={`w-3.5 h-3.5 transition-transform ${
                  proSearch ? 'scale-110 text-[#20808D]' : 'text-[#6E7173]'
                }`}
              />
              <span>Pro Search</span>
              {/* Custom switch slider indicator */}
              <div
                className={`w-7 h-4 rounded-full p-0.5 transition-colors duration-200 flex items-center ${
                  proSearch
                    ? 'bg-[#20808D] justify-end'
                    : 'bg-[#2D3131] justify-start'
                }`}
              >
                <div className="w-3 h-3 rounded-full bg-white shadow-sm transition-transform" />
              </div>
            </button>

            {/* Provider Selector Pill & Dropdown */}
            {onSelectProvider && (
              <div className="relative" ref={providerMenuRef}>
                <button
                  type="button"
                  onClick={() => setIsProviderMenuOpen(!isProviderMenuOpen)}
                  className="flex items-center gap-1.5 px-2.5 py-1.5 rounded-full bg-[#181A1A] hover:bg-[#252828] border border-[#2D3131] hover:border-[#3E4343] text-xs font-medium text-[#9B9C9E] hover:text-white transition-all select-none"
                  title="Выбор поискового провайдера"
                >
                  <Globe className="w-3.5 h-3.5 text-[#20808D]" />
                  <span>{currentProviderInfo.name}</span>
                  <ChevronDown
                    className={`w-3 h-3 transition-transform ${
                      isProviderMenuOpen ? 'rotate-180' : ''
                    }`}
                  />
                </button>

                {/* Dropdown Menu */}
                {isProviderMenuOpen && (
                  <div className="absolute left-0 bottom-full mb-2 z-50 w-56 rounded-xl bg-[#1C1E1E] border border-[#2D3131] shadow-2xl py-1 animate-fade-in">
                    <div className="px-3 py-1.5 text-[11px] font-semibold uppercase tracking-wider text-[#6E7173] border-b border-[#262929]">
                      Поисковый провайдер
                    </div>
                    {availableProviders.map((provKey) => {
                      const info = PROVIDER_OPTIONS[provKey] || {
                        name: provKey,
                        desc: '',
                      };
                      const isSelected = provider === provKey;

                      return (
                        <button
                          key={provKey}
                          type="button"
                          onClick={() => {
                            onSelectProvider(provKey);
                            setIsProviderMenuOpen(false);
                          }}
                          className={`w-full flex items-center justify-between px-3 py-2 text-left hover:bg-[#252828] transition-colors ${
                            isSelected ? 'bg-[#222525]' : ''
                          }`}
                        >
                          <div>
                            <div className="text-xs font-medium text-white flex items-center gap-1.5">
                              <span>{info.name}</span>
                            </div>
                            {info.desc && (
                              <div className="text-[11px] text-[#8A8D8F]">
                                {info.desc}
                              </div>
                            )}
                          </div>
                          {isSelected && (
                            <Check className="w-3.5 h-3.5 text-[#20808D] flex-shrink-0" />
                          )}
                        </button>
                      );
                    })}
                  </div>
                )}
              </div>
            )}
          </div>

          {/* Submit Button */}
          <button
            type="button"
            onClick={onSubmit}
            disabled={!canSubmit}
            aria-label="Отправить запрос"
            className={`flex items-center justify-center w-8 h-8 rounded-full transition-all duration-200 focus:outline-none ${
              canSubmit
                ? 'bg-[#20808D] text-white hover:bg-[#1B6E7A] shadow-md hover:scale-105 active:scale-95'
                : 'bg-[#2B2D2D] text-[#6E7173] cursor-not-allowed opacity-60'
            }`}
          >
            {isLoading ? (
              <Loader2 className="w-4 h-4 animate-spin" />
            ) : (
              <ArrowUp className="w-4 h-4 stroke-[2.5]" />
            )}
          </button>
        </div>
      </div>
    </div>
  );
};
