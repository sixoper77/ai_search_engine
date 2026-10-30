import React, { useEffect } from 'react';
import { X, ExternalLink } from 'lucide-react';

interface ImageLightboxProps {
  imageUrl: string | null;
  onClose: () => void;
}

export const ImageLightbox: React.FC<ImageLightboxProps> = ({ imageUrl, onClose }) => {
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'Escape') onClose();
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [onClose]);

  if (!imageUrl) return null;

  return (
    <div
      role="dialog"
      aria-modal="true"
      aria-label="Просмотр изображения"
      className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/85 backdrop-blur-md animate-fade-in"
      onClick={onClose}
    >
      <div
        className="relative max-w-4xl max-h-[90vh] bg-[#1E2020] rounded-2xl overflow-hidden border border-[#2D3131] shadow-2xl flex flex-col"
        onClick={(e) => e.stopPropagation()}
      >
        <div className="flex items-center justify-between p-3 border-b border-[#2D3131] bg-[#181A1A]">
          <span className="text-xs text-[#9B9C9E] truncate max-w-md px-2">
            {imageUrl}
          </span>
          <div className="flex items-center gap-2">
            <a
              href={imageUrl}
              target="_blank"
              rel="noreferrer"
              className="p-1.5 text-[#9B9C9E] hover:text-white rounded-lg hover:bg-[#252828] transition-colors"
              title="Открыть оригинал"
            >
              <ExternalLink className="w-4 h-4" />
            </a>
            <button
              onClick={onClose}
              className="p-1.5 text-[#9B9C9E] hover:text-white rounded-lg hover:bg-[#252828] transition-colors"
              title="Закрыть"
            >
              <X className="w-4 h-4" />
            </button>
          </div>
        </div>

        <div className="flex-1 flex items-center justify-center p-4 bg-black/40 overflow-auto">
          <img
            src={imageUrl}
            alt="Search preview"
            className="max-w-full max-h-[75vh] object-contain rounded-lg"
          />
        </div>
      </div>
    </div>
  );
};

