import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import { SearchInput } from './SearchInput';

describe('SearchInput Component', () => {
  it('renders input with only Pro Search switch, provider selector and submit button (no model dropdown or mic)', () => {
    const onToggleProSearch = vi.fn();
    const onSubmit = vi.fn();
    const onChangeQuery = vi.fn();
    const onSelectProvider = vi.fn();

    render(
      <SearchInput
        query=""
        onChangeQuery={onChangeQuery}
        onSubmit={onSubmit}
        isLoading={false}
        proSearch={false}
        onToggleProSearch={onToggleProSearch}
        provider="tavily"
        onSelectProvider={onSelectProvider}
      />
    );

    // Check textarea
    expect(screen.getByPlaceholderText('Задайте любой вопрос...')).toBeInTheDocument();

    // Check Pro Search switch exists
    const proSearchBtn = screen.getByText('Pro Search');
    expect(proSearchBtn).toBeInTheDocument();

    // Check provider selector exists
    expect(screen.getByText('Tavily AI')).toBeInTheDocument();

    // Check submit button
    const submitBtn = screen.getByLabelText('Отправить запрос');
    expect(submitBtn).toBeInTheDocument();

    // Verify model dropdown and mic are NOT present
    expect(screen.queryByText(/выбор модели/i)).not.toBeInTheDocument();
    expect(screen.queryByText(/gpt/i)).not.toBeInTheDocument();
    expect(screen.queryByLabelText(/voice/i)).not.toBeInTheDocument();
  });

  it('opens provider dropdown and allows selecting a different provider', () => {
    const onSelectProvider = vi.fn();

    render(
      <SearchInput
        query=""
        onChangeQuery={vi.fn()}
        onSubmit={vi.fn()}
        isLoading={false}
        proSearch={false}
        onToggleProSearch={vi.fn()}
        provider="tavily"
        onSelectProvider={onSelectProvider}
        availableProviders={['tavily', 'serper', 'searxng']}
      />
    );

    // Open provider menu
    const providerPill = screen.getByTitle('Выбор поискового провайдера');
    fireEvent.click(providerPill);

    // Check options appear
    expect(screen.getByText('Google Serper')).toBeInTheDocument();
    expect(screen.getByText('SearXNG')).toBeInTheDocument();

    // Select Google Serper
    fireEvent.click(screen.getByText('Google Serper'));
    expect(onSelectProvider).toHaveBeenCalledWith('serper');
  });

  it('toggles Pro Search when switch is clicked', () => {
    const onToggleProSearch = vi.fn();

    render(
      <SearchInput
        query=""
        onChangeQuery={vi.fn()}
        onSubmit={vi.fn()}
        isLoading={false}
        proSearch={false}
        onToggleProSearch={onToggleProSearch}
      />
    );

    const proSearchBtn = screen.getByText('Pro Search').closest('button');
    expect(proSearchBtn).toBeInTheDocument();
    fireEvent.click(proSearchBtn!);
    expect(onToggleProSearch).toHaveBeenCalledTimes(1);
  });

  it('submits on Enter key when input is non-empty', () => {
    const onSubmit = vi.fn();

    render(
      <SearchInput
        query="Тестовый поисковый запрос"
        onChangeQuery={vi.fn()}
        onSubmit={onSubmit}
        isLoading={false}
        proSearch={false}
        onToggleProSearch={vi.fn()}
      />
    );

    const textarea = screen.getByPlaceholderText('Задайте любой вопрос...');
    fireEvent.keyDown(textarea, { key: 'Enter', shiftKey: false });
    expect(onSubmit).toHaveBeenCalledTimes(1);
  });
});
