import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import { App } from './App';
import * as api from './api';

describe('App Main Component', () => {
  beforeEach(() => {
    vi.spyOn(api, 'fetchChats').mockResolvedValue([
      { id: 'chat-1', name: 'Перплексити поиск', updated_at: '2026-10-30T10:00:00Z' },
    ]);
  });

  it('renders initial hero "Что вы хотите узнать?" and main components', async () => {
    render(<App />);

    // Check main title
    expect(screen.getByText('Что вы хотите узнать?')).toBeInTheDocument();

    // Check "Новый чат" button
    expect(screen.getAllByText('Новый чат').length).toBeGreaterThan(0);

    // Check Pro Search switch
    expect(screen.getByText('Pro Search')).toBeInTheDocument();

    // Check 4 cards
    expect(screen.getByText('Искать что угодно')).toBeInTheDocument();
    expect(screen.getByText('Выполняйте задачи с Computer')).toBeInTheDocument();

    // Check chats loaded in sidebar
    await waitFor(() => {
      expect(screen.getByText('Перплексити поиск')).toBeInTheDocument();
    });
  });
});

