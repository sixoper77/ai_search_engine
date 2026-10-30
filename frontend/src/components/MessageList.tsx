import React from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { ExternalLink, Globe, Sparkles } from 'lucide-react';
import { MessageOut } from '../types';
import { CodeBlock } from './CodeBlock';
import { FourCardsGrid } from './FourCardsGrid';

interface MessageListProps {
  messages: MessageOut[];
  activeStreamingMessage?: string;
  streamingPhotos?: string[];
  isLoadingPhotos?: boolean;
  onSelectImage?: (photoUrl: string) => void;
}

export const MessageList: React.FC<MessageListProps> = ({
  messages,
  activeStreamingMessage,
  streamingPhotos,
  isLoadingPhotos,
  onSelectImage,
}) => {
  return (
    <div className="w-full max-w-3xl space-y-8 py-6">
      {messages.map((msg, index) => {
        const isUser = msg.role === 'user';

        if (isUser) {
          return (
            <div key={msg.id || index} className="pt-4 border-t border-[#262929] first:border-none">
              <h2 className="text-xl sm:text-2xl font-medium text-white tracking-tight leading-snug">
                {msg.content}
              </h2>
            </div>
          );
        }

        // AI Answer
        return (
          <div key={msg.id || index} className="space-y-4">
            {/* Sources section if present */}
            {msg.steps && msg.steps.length > 0 && (
              <div>
                <div className="flex items-center gap-1.5 text-xs font-semibold text-[#8E9092] uppercase tracking-wider mb-2.5">
                  <Globe className="w-3.5 h-3.5 text-[#20808D]" />
                  <span>Источники</span>
                </div>
                <div className="flex flex-wrap gap-2">
                  {msg.steps.map((st, sIdx) => {
                    let hostname = st.url;
                    try {
                      hostname = new URL(st.url).hostname.replace('www.', '');
                    } catch {
                      // ignore
                    }
                    return (
                      <a
                        key={sIdx}
                        href={st.url}
                        target="_blank"
                        rel="noreferrer"
                        className="group flex items-center gap-2 px-3 py-1.5 rounded-xl bg-[#202222] hover:bg-[#272A2A] border border-[#2D3131] hover:border-[#3E4343] text-xs text-[#BABABA] hover:text-white transition-all max-w-[220px]"
                        title={st.title || st.url}
                      >
                        <div className="w-4 h-4 rounded-full bg-[#181A1A] flex items-center justify-center text-[10px] text-[#20808D] font-mono flex-shrink-0">
                          {sIdx + 1}
                        </div>
                        <span className="truncate">{st.title || hostname}</span>
                        <ExternalLink className="w-3 h-3 text-[#6E7173] group-hover:text-white flex-shrink-0 ml-auto" />
                      </a>
                    );
                  })}
                </div>
              </div>
            )}

            {/* Photos if stored in message */}
            {msg.photos && msg.photos.length > 0 && (
              <FourCardsGrid
                photos={msg.photos}
                onSelectImage={onSelectImage}
              />
            )}

            {/* Answer body with Markdown & Syntax Highlighting */}
            <div className="text-[15px] text-[#D8D8D8] leading-relaxed markdown-content">
              <ReactMarkdown
                remarkPlugins={[remarkGfm]}
                components={{
                  code({ node, inline, className, children, ...props }: any) {
                    const match = /language-(\w+)/.exec(className || '');
                    const codeString = String(children).replace(/\n$/, '');

                    if (!inline && (match || codeString.includes('\n'))) {
                      return (
                        <CodeBlock
                          code={codeString}
                          language={match ? match[1] : undefined}
                        />
                      );
                    }

                    return (
                      <code
                        className="px-1.5 py-0.5 rounded-md bg-[#252828] text-[#38BDF8] text-[13px] font-mono"
                        {...props}
                      >
                        {children}
                      </code>
                    );
                  },
                  p({ children }) {
                    return <p className="mb-4 last:mb-0">{children}</p>;
                  },
                  ul({ children }) {
                    return <ul className="list-disc pl-5 mb-4 space-y-1">{children}</ul>;
                  },
                  ol({ children }) {
                    return <ol className="list-decimal pl-5 mb-4 space-y-1">{children}</ol>;
                  },
                  li({ children }) {
                    return <li className="pl-1">{children}</li>;
                  },
                  h1({ children }) {
                    return <h1 className="text-xl font-semibold text-white mt-6 mb-3">{children}</h1>;
                  },
                  h2({ children }) {
                    return <h2 className="text-lg font-semibold text-white mt-5 mb-2.5">{children}</h2>;
                  },
                  h3({ children }) {
                    return <h3 className="text-base font-semibold text-white mt-4 mb-2">{children}</h3>;
                  },
                  blockquote({ children }) {
                    return (
                      <blockquote className="border-l-2 border-[#20808D] pl-4 italic text-[#A3A3A3] my-4">
                        {children}
                      </blockquote>
                    );
                  },
                  table({ children }) {
                    return (
                      <div className="overflow-x-auto my-4 rounded-xl border border-[#2D3131]">
                        <table className="w-full text-left text-sm">{children}</table>
                      </div>
                    );
                  },
                  th({ children }) {
                    return (
                      <th className="px-4 py-2 bg-[#202222] font-medium text-white border-b border-[#2D3131]">
                        {children}
                      </th>
                    );
                  },
                  td({ children }) {
                    return (
                      <td className="px-4 py-2 border-b border-[#2D3131]/60 text-[#BABABA]">
                        {children}
                      </td>
                    );
                  },
                }}
              >
                {msg.content}
              </ReactMarkdown>
            </div>
          </div>
        );
      })}

      {/* Actively streaming response */}
      {activeStreamingMessage !== undefined && (
        <div className="space-y-4 pt-2">
          {/* Display 4 photos before/above streamed answer */}
          {(streamingPhotos?.length || isLoadingPhotos) ? (
            <FourCardsGrid
              photos={streamingPhotos}
              isLoadingPhotos={isLoadingPhotos}
              onSelectImage={onSelectImage}
            />
          ) : null}

          {/* Streamed Answer with Markdown and Code Syntax Detection */}
          {activeStreamingMessage ? (
            <div className="text-[15px] text-[#D8D8D8] leading-relaxed markdown-content">
              <ReactMarkdown
                remarkPlugins={[remarkGfm]}
                components={{
                  code({ node, inline, className, children, ...props }: any) {
                    const match = /language-(\w+)/.exec(className || '');
                    const codeString = String(children).replace(/\n$/, '');

                    if (!inline && (match || codeString.includes('\n'))) {
                      return (
                        <CodeBlock
                          code={codeString}
                          language={match ? match[1] : undefined}
                        />
                      );
                    }

                    return (
                      <code
                        className="px-1.5 py-0.5 rounded-md bg-[#252828] text-[#38BDF8] text-[13px] font-mono"
                        {...props}
                      >
                        {children}
                      </code>
                    );
                  },
                  p({ children }) {
                    return <p className="mb-4 last:mb-0">{children}</p>;
                  },
                  ul({ children }) {
                    return <ul className="list-disc pl-5 mb-4 space-y-1">{children}</ul>;
                  },
                  ol({ children }) {
                    return <ol className="list-decimal pl-5 mb-4 space-y-1">{children}</ol>;
                  },
                  li({ children }) {
                    return <li className="pl-1">{children}</li>;
                  },
                }}
              >
                {activeStreamingMessage}
              </ReactMarkdown>
              {/* Typing cursor */}
              <span className="inline-block w-2 h-4 bg-[#20808D] animate-pulse ml-1 align-middle" />
            </div>
          ) : null}
        </div>
      )}
    </div>
  );
};

