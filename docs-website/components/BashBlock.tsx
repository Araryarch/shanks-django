'use client';

import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import type { CSSProperties } from 'react';

const bashTheme: Record<string, CSSProperties> = {
  'code[class*="language-"]': {
    color: '#cbd5e1',
    background: 'none',
    fontFamily: 'inherit',
    fontSize: '0.875rem',
    whiteSpace: 'pre',
    lineHeight: '2',
  },
  'pre[class*="language-"]': {
    color: '#cbd5e1',
    background: '#0d0608',
    fontFamily: 'inherit',
    padding: '1.25rem 1.5rem',
    margin: 0,
    overflow: 'auto',
    lineHeight: '2',
  },
  'function': { color: '#fb7185' },
  'keyword': { color: '#fb7185' },
  'string': { color: '#34d399' },
  'comment': { color: '#475569', fontStyle: 'italic' },
  'operator': { color: '#94a3b8' },
  'punctuation': { color: '#64748b' },
  'variable': { color: '#fdba74' },
  'builtin': { color: '#f0abfc' },
};

interface BashBlockProps {
  code: string;
}

export function BashBlock({ code }: BashBlockProps) {
  return (
    <div className="relative rounded-xl overflow-hidden border border-white/10 shadow-xl shadow-black/30">
      <div className="absolute inset-0 bg-gradient-to-r from-rose-600/8 to-orange-600/5 pointer-events-none" />
      {/* Titlebar */}
      <div className="flex items-center gap-2 px-4 py-2.5 bg-white/5 border-b border-white/8">
        <div className="flex gap-1.5">
          <div className="w-2.5 h-2.5 rounded-full bg-[#ff5f56]" />
          <div className="w-2.5 h-2.5 rounded-full bg-[#febc2e]" />
          <div className="w-2.5 h-2.5 rounded-full bg-[#28c840]" />
        </div>
        <span className="text-[11px] text-white/30 font-mono ml-1">bash</span>
      </div>
      <SyntaxHighlighter
        language="bash"
        style={bashTheme}
        customStyle={{
          margin: 0,
          borderRadius: 0,
          background: '#0d0608',
          fontSize: '0.875rem',
        }}
        codeTagProps={{ style: { fontFamily: 'var(--font-mono), JetBrains Mono, monospace' } }}
      >
        {code.trim()}
      </SyntaxHighlighter>
    </div>
  );
}
