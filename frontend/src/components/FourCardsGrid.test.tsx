import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import { FourCardsGrid } from './FourCardsGrid';

describe('FourCardsGrid Component', () => {
  it('renders 4 feature cards in idle state matching user screenshot', () => {
    const onSelectPrompt = vi.fn();

    render(<FourCardsGrid onSelectPrompt={onSelectPrompt} />);

    expect(screen.getByText('Искать что угодно')).toBeInTheDocument();
    expect(screen.getByText('Выполняйте задачи с Computer')).toBeInTheDocument();
    expect(screen.getByText('Глубокое исследование')).toBeInTheDocument();
    expect(screen.getByText('Пишите и форматируйте код')).toBeInTheDocument();

    // Click first card
    fireEvent.click(screen.getByText('Искать что угодно'));
    expect(onSelectPrompt).toHaveBeenCalledTimes(1);
  });

  it('renders 4 search images when photos are provided before/during streaming', () => {
    const mockPhotos = [
      'https://example.com/photo1.jpg',
      'https://example.com/photo2.jpg',
      'https://example.com/photo3.jpg',
      'https://example.com/photo4.jpg',
    ];
    const onSelectImage = vi.fn();

    render(
      <FourCardsGrid
        photos={mockPhotos}
        isLoadingPhotos={false}
        onSelectImage={onSelectImage}
      />
    );

    const imagesGrid = screen.getByTestId('four-images-grid');
    expect(imagesGrid).toBeInTheDocument();

    const renderedImages = screen.getAllByRole('img');
    expect(renderedImages.length).toBe(4);
    expect(renderedImages[0]).toHaveAttribute('src', mockPhotos[0]);

    fireEvent.click(renderedImages[0]);
    expect(onSelectImage).toHaveBeenCalledWith(mockPhotos[0]);
  });
});

