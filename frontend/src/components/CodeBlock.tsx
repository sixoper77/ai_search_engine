import React, { useState, useMemo } from 'react';
import hljs from 'highlight.js';
import { Check, Copy, Terminal } from 'lucide-react';

interface CodeBlockProps {
  code: string;
  language?: string;
}

// Friendly display names for programming languages
const LANGUAGE_NAMES: Record<string, string> = {
  go: 'Go (Golang)',
  golang: 'Go (Golang)',
  python: 'Python',
  py: 'Python',
  typescript: 'TypeScript',
  ts: 'TypeScript',
  javascript: 'JavaScript',
  js: 'JavaScript',
  rust: 'Rust',
  rs: 'Rust',
  cpp: 'C++',
  c: 'C',
  csharp: 'C#',
  cs: 'C#',
  java: 'Java',
  kotlin: 'Kotlin',
  swift: 'Swift',
  php: 'PHP',
  ruby: 'Ruby',
  bash: 'Bash / Shell',
  sh: 'Shell',
  shell: 'Shell',
  sql: 'SQL',
  json: 'JSON',
  yaml: 'YAML',
  yml: 'YAML',
  html: 'HTML',
  css: 'CSS',
  xml: 'XML',
  markdown: 'Markdown',
  md: 'Markdown',
  dockerfile: 'Dockerfile',
};

// Language detection hints for common languages
function detectLanguage(code: string, hintedLang?: string): { lang: string; displayName: string } {
  const normalizedHint = hintedLang?.toLowerCase().trim();

  // If a valid language hint is provided, use it
  if (normalizedHint && hljs.getLanguage(normalizedHint)) {
    return {
      lang: normalizedHint,
      displayName: LANGUAGE_NAMES[normalizedHint] || normalizedHint.toUpperCase(),
    };
  }

  // Auto-detect using highlight.js heuristic analysis
  try {
    const subset = [
      'go',
      'python',
      'typescript',
      'javascript',
      'rust',
      'cpp',
      'c',
      'csharp',
      'java',
      'bash',
      'sql',
      'json',
      'html',
      'css',
      'yaml',
    ];
    const autoResult = hljs.highlightAuto(code, subset);
    if (autoResult.language) {
      const detected = autoResult.language.toLowerCase();
      return {
        lang: detected,
        displayName: LANGUAGE_NAMES[detected] || detected.toUpperCase(),
      };
    }
  } catch (e) {
    console.debug('Language auto-detection error:', e);
  }

  return {
    lang: 'plaintext',
    displayName: 'Plain Text',
  };
}

function escapeHtml(text: string): string {
  return text
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#039;');
}

export const CodeBlock: React.FC<CodeBlockProps> = ({ code, language }) => {
  const [copied, setCopied] = useState(false);

  const { lang, displayName } = useMemo(
    () => detectLanguage(code, language),
    [code, language]
  );

  const highlightedHtml = useMemo(() => {
    try {
      if (hljs.getLanguage(lang)) {
        return hljs.highlight(code, { language: lang, ignoreIllegals: true }).value;
      }
      return hljs.highlightAuto(code).value;
    } catch {
      return escapeHtml(code);
    }
  }, [code, lang]);

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(code);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch (err) {
      console.error('Failed to copy text:', err);
    }
  };

  return (
    <div className="relative my-4 rounded-xl overflow-hidden border border-[#2D3131] bg-[#161717] font-mono text-[13px] shadow-sm">
      {/* Header bar */}
      <div className="flex items-center justify-between px-4 py-2 bg-[#1B1D1D] border-b border-[#262929] select-none">
        <div className="flex items-center gap-2">
          <Terminal className="w-3.5 h-3.5 text-[#20808D]" />
          <span className="text-xs font-medium text-[#A3A3A3] tracking-wide">
            {displayName}
          </span>
        </div>

        <button
          onClick={handleCopy}
          aria-label={copied ? "Скопировано" : "Скопировать код"}
          className="flex items-center gap-1.5 px-2.5 py-1 text-xs text-[#9B9C9E] hover:text-white rounded-md hover:bg-[#252828] transition-colors focus:outline-none"
        >
          {copied ? (
            <>
              <Check className="w-3.5 h-3.5 text-emerald-400" />
              <span className="text-emerald-400">Скопировано</span>
            </>
          ) : (
            <>
              <Copy className="w-3.5 h-3.5" />
              <span>Копировать</span>
            </>
          )}
        </button>
      </div>

      {/* Code body */}
      <div className="p-4 overflow-x-auto text-[#E2E8F0] leading-relaxed font-mono">
        <pre className="m-0 p-0">
          <code
            dangerouslySetInnerHTML={{ __html: highlightedHtml }}
            className={`hljs language-${lang}`}
          />
        </pre>
      </div>
    </div>
  );
};
