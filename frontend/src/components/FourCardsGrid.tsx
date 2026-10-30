import React from 'react';
import { Search, Monitor, Sparkles, Code2, ZoomIn, Image as ImageIcon } from 'lucide-react';

interface FourCardsGridProps {
  photos?: string[];
  isLoadingPhotos?: boolean;
  onSelectPrompt?: (prompt: string) => void;
  onSelectImage?: (photoUrl: string) => void;
}

export const FourCardsGrid: React.FC<FourCardsGridProps> = ({
  photos = [],
  isLoadingPhotos = false,
  onSelectPrompt,
  onSelectImage,
}) => {
  const hasPhotos = photos && photos.length > 0;

  // If photos are loading or available, display the 4 search images!
  if (isLoadingPhotos || hasPhotos) {
    const displayPhotos = photos.slice(0, 4);

    return (
      <div className="w-full max-w-3xl my-6 animate-fade-in" data-testid="four-images-grid">
        <div className="flex items-center gap-2 mb-3 text-xs font-medium text-[#9B9C9E]">
          <ImageIcon className="w-3.5 h-3.5 text-[#20808D]" />
          <span>Найденные изображения ({displayPhotos.length} из 4)</span>
          {isLoadingPhotos && (
            <span className="inline-block w-1.5 h-1.5 rounded-full bg-[#20808D] animate-ping ml-1" />
          )}
        </div>

        <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
          {[0, 1, 2, 3].map((index) => {
            const photo = displayPhotos[index];

            if (!photo) {
              return (
                <div
                  key={index}
                  className="h-32 sm:h-36 rounded-xl border border-[#2D3131] bg-[#1E2020]/60 animate-pulse flex flex-col items-center justify-center p-3 text-[#65686A]"
                >
                  <ImageIcon className="w-6 h-6 stroke-1 mb-1 opacity-50" />
                  <span className="text-[11px]">Поиск фото...</span>
                </div>
              );
            }

            return (
              <div
                key={index}
                onClick={() => onSelectImage?.(photo)}
                className="group relative h-32 sm:h-36 rounded-xl overflow-hidden border border-[#2D3131] bg-[#1E2020] hover:border-[#20808D] transition-all duration-200 cursor-pointer shadow-sm hover:shadow-md"
              >
                <img
                  src={photo}
                  alt={`Search result ${index + 1}`}
                  loading="lazy"
                  className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
                  onError={(e) => {
                    // Fallback placeholder if image link is broken
                    (e.target as HTMLImageElement).src =
                      'https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?auto=format&fit=crop&w=400&q=80';
                  }}
                />
                <div className="absolute inset-0 bg-gradient-to-t from-black/70 via-transparent to-transparent opacity-0 group-hover:opacity-100 transition-opacity flex items-end p-2.5">
                  <span className="text-[11px] text-white flex items-center gap-1 font-medium">
                    <ZoomIn className="w-3.5 h-3.5" /> Увеличить
                  </span>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    );
  }

  // Initial State: 4 interactive Perplexity cards (2x2 grid)
  const defaultCards = [
    {
      icon: Search,
      title: 'Искать что угодно',
      description: 'Получайте быстрые и точные ответы из самых надёжных источников.',
      prompt: 'Расскажи последние новости в мире искусственного интеллекта за 2026 год',
      badge: null,
      gradient: 'from-[#1a3835]/40 to-[#202222]',
      borderHover: 'hover:border-[#20808D]/60',
    },
    {
      icon: Monitor,
      title: 'Выполняйте задачи с Computer',
      description: 'Передавайте свои проекты, чтобы получать безупречные и надёжные результаты круглосуточно.',
      prompt: 'Помоги написать архитектуру для распределенного микросервиса на Go',
      badge: 'НОВОЕ',
      gradient: 'from-[#192b3a]/40 to-[#202222]',
      borderHover: 'hover:border-[#38bdf8]/60',
    },
    {
      icon: Sparkles,
      title: 'Глубокое исследование',
      description: 'Многошаговый агентный поиск с проверкой фактов и синтезом первоисточников в Pro Search.',
      prompt: 'Проведи глубокий сравнительный анализ квантовых вычислений и классических суперкомпьютеров',
      badge: 'PRO',
      gradient: 'from-[#2e263d]/40 to-[#202222]',
      borderHover: 'hover:border-[#a855f7]/60',
    },
    {
      icon: Code2,
      title: 'Пишите и форматируйте код',
      description: 'Генерация, отладка и автоматическое определение языков программирования с подсветкой синтаксиса.',
      prompt: 'Напиши конкурентный веб-парсер на Go с использованием goroutines и channels',
      badge: null,
      gradient: 'from-[#2d2218]/40 to-[#202222]',
      borderHover: 'hover:border-[#f97316]/60',
    },
  ];

  return (
    <div className="w-full max-w-3xl my-6" data-testid="four-cards-grid">
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-3.5">
        {defaultCards.map((card, idx) => {
          const Icon = card.icon;
          return (
            <button
              key={idx}
              onClick={() => onSelectPrompt?.(card.prompt)}
              className={`group text-left p-4 rounded-xl border border-[#2D3131] bg-gradient-to-br ${card.gradient} ${card.borderHover} transition-all duration-200 hover:-translate-y-0.5 shadow-sm hover:shadow-lg focus:outline-none focus:ring-1 focus:ring-[#20808D] flex flex-col justify-between min-h-[115px]`}
            >
              <div>
                <div className="flex items-center justify-between mb-2">
                  <div className="flex items-center gap-2">
                    <Icon className="w-4 h-4 text-[#20808D] group-hover:scale-110 transition-transform" />
                    <span className="text-sm font-medium text-white group-hover:text-[#E0F2FE] transition-colors">
                      {card.title}
                    </span>
                  </div>
                  {card.badge && (
                    <span className="text-[10px] font-semibold tracking-wider px-1.5 py-0.5 rounded bg-[#20808D]/20 text-[#20808D] border border-[#20808D]/30">
                      {card.badge}
                    </span>
                  )}
                </div>
                <p className="text-xs text-[#9B9C9E] group-hover:text-[#BABABA] transition-colors line-clamp-2 leading-relaxed">
                  {card.description}
                </p>
              </div>
            </button>
          );
        })}
      </div>
    </div>
  );
};

