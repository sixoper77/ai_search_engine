import React from 'react';
import { PerplexityIcon } from './PerplexityIcon';

export const PerplexityHero: React.FC = () => {
  return (
    <div className="flex flex-col items-center justify-center text-center my-6 select-none animate-fade-in">
      {/* Central Asterisk Logo */}
      <div className="w-12 h-12 rounded-2xl bg-[#202222]/80 border border-[#2D3131] flex items-center justify-center text-[#20808D] shadow-lg mb-6 hover:scale-105 transition-transform duration-300">
        <PerplexityIcon size={28} />
      </div>

      {/* Main Perplexity Title */}
      <h1 className="text-3xl sm:text-4xl md:text-[40px] font-normal text-white tracking-[-0.02em] font-sans">
        Что вы хотите узнать?
      </h1>
    </div>
  );
};

