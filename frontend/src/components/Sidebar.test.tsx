import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import { Sidebar } from './Sidebar';
import { ChatItem } from '../types';

describe('Sidebar Component', () => {
  const mockChats: ChatItem[] = [
    { id: '1', name: 'ИИ поиск в 2026', updated_at: '2026-10-30T10:00:00Z' },
    { id: '2', name: 'Микросервисы на Golang', updated_at: '2026-10-29T10:00:00Z' },
  ];

  it('renders "Новый чат" button instead of "Новое"', () => {
    const onNewChat = vi.fn();
    render(
      <Sidebar
        chats={[]}
        onSelectChat={vi.fn()}
        onNewChat={onNewChat}
        isLoadingMore={false}
        hasMoreChats={false}
        onLoadMoreChats={vi.fn()}
        isOpen={true}
        onToggleSidebar={vi.fn()}
        isMobile={false}
      />
    );

    const newChatButton = screen.getByText('Новый чат');
    expect(newChatButton).toBeInTheDocument();
    expect(screen.queryByText('Новое')).not.toBeInTheDocument();

    fireEvent.click(newChatButton);
    expect(onNewChat).toHaveBeenCalledTimes(1);
  });

  it('renders standard Perplexity navigation items', () => {
    render(
      <Sidebar
        chats={[]}
        onSelectChat={vi.fn()}
        onNewChat={vi.fn()}
        isLoadingMore={false}
        hasMoreChats={false}
        onLoadMoreChats={vi.fn()}
        isOpen={true}
        onToggleSidebar={vi.fn()}
        isMobile={false}
      />
    );

    expect(screen.getByText('Компьютер')).toBeInTheDocument();
    expect(screen.getByText('Автоматизации')).toBeInTheDocument();
    expect(screen.getByText('Артефакты')).toBeInTheDocument();
    expect(screen.getByText('Настройка')).toBeInTheDocument();
    expect(screen.getByText('Посмотреть планы')).toBeInTheDocument();
    expect(screen.getByText('Войдите')).toBeInTheDocument();
  });

  it('renders recent chats list and handles chat selection', () => {
    const onSelectChat = vi.fn();
    render(
      <Sidebar
        chats={mockChats}
        activeChatId="1"
        onSelectChat={onSelectChat}
        onNewChat={vi.fn()}
        isLoadingMore={false}
        hasMoreChats={false}
        onLoadMoreChats={vi.fn()}
        isOpen={true}
        onToggleSidebar={vi.fn()}
        isMobile={false}
      />
    );

    expect(screen.getByText('ИИ поиск в 2026')).toBeInTheDocument();
    expect(screen.getByText('Микросервисы на Golang')).toBeInTheDocument();

    fireEvent.click(screen.getByText('Микросервисы на Golang'));
    expect(onSelectChat).toHaveBeenCalledWith('2');
  });

  it('triggers infinite scroll when scrolling recent chats container', () => {
    const onLoadMoreChats = vi.fn();
    render(
      <Sidebar
        chats={mockChats}
        onSelectChat={vi.fn()}
        onNewChat={vi.fn()}
        isLoadingMore={false}
        hasMoreChats={true}
        onLoadMoreChats={onLoadMoreChats}
        isOpen={true}
        onToggleSidebar={vi.fn()}
        isMobile={false}
      />
    );

    const scrollContainer = screen.getByTestId('sidebar-chats-scroll');
    Object.defineProperty(scrollContainer, 'scrollHeight', { value: 1000, configurable: true });
    Object.defineProperty(scrollContainer, 'clientHeight', { value: 300, configurable: true });
    Object.defineProperty(scrollContainer, 'scrollTop', { value: 650, configurable: true });

    fireEvent.scroll(scrollContainer);
    expect(onLoadMoreChats).toHaveBeenCalled();
  });
});

