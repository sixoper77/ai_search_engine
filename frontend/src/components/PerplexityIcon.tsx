import React from 'react';

interface PerplexityIconProps {
  className?: string;
  size?: number;
}

export const PerplexityIcon: React.FC<PerplexityIconProps> = ({
  className = 'w-5 h-5',
  size = 20,
}) => {
  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="1.8"
      strokeLinecap="round"
      strokeLinejoin="round"
      className={className}
    >
      {/* Perplexity Asterisk Geometry */}
      <line x1="12" y1="2" x2="12" y2="22" />
      <line x1="3.34" y1="7" x2="20.66" y2="17" />
      <line x1="3.34" y1="17" x2="20.66" y2="7" />
      {/* Central ring intersection accents */}
      <circle cx="12" cy="12" r="2.5" fill="currentColor" fillOpacity="0.15" />
    </svg>
  );
};

