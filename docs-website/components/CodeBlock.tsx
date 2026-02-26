'use client';

import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import type { CSSProperties } from 'react';

// Custom red-dark theme matching the SHANKS design
const shanksTheme: Record<string, CSSProperties> = {
  'code[class*="language-"]': {
    color: '#e2e8f0',
    background: 'none',
    fontFamily: 'var(--font-mono), JetBrains Mono, Fira Code, monospace',
    fontSize: '0.875rem',
    textAlign: 'left',
    whiteSpace: 'pre',
    wordSpacing: 'normal',
    wordBreak: 'normal',
    wordWrap: 'normal',
    lineHeight: '1.8',
    tabSize: 4,
    hyphens: 'none',
  },
  'pre[class*="language-"]': {
    color: '#e2e8f0',
    background: '#0d0608',
    fontFamily: 'var(--font-mono), JetBrains Mono, Fira Code, monospace',
    textAlign: 'left',
    whiteSpace: 'pre',
    wordSpacing: 'normal',
    wordBreak: 'normal',
    wordWrap: 'normal',
    lineHeight: '1.8',
    tabSize: 4,
    hyphens: 'none',
    padding: '1.5rem',
    margin: 0,
    overflow: 'auto',
  },
  // Keywords: from, import, def, return, class, if, else, etc.
  'keyword': { color: '#fb7185' },            // rose-400
  'keyword.import': { color: '#fb7185' },
  // Builtin / decorator
  'decorator': { color: '#f0abfc' },          // fuchsia-300
  'builtin': { color: '#f0abfc' },
  // Operator
  'operator': { color: '#94a3b8' },
  // Punctuation
  'punctuation': { color: '#64748b' },
  // Strings
  'string': { color: '#34d399' },             // emerald-400
  'string.interpolated': { color: '#6ee7b7' },
  // Numbers
  'number': { color: '#fbbf24' },             // amber-400
  // Comments
  'comment': { color: '#475569', fontStyle: 'italic' },
  // Functions / method names
  'function': { color: '#fdba74' },           // orange-300
  // Class names
  'class-name': { color: '#fda4af' },         // rose-300
  // Variables / identifiers
  'variable': { color: '#e2e8f0' },
  // Boolean / None
  'boolean': { color: '#fb7185' },
  'constant': { color: '#fbbf24' },
  // Parameters
  'parameter': { color: '#bfdbfe' },          // blue-200
  // atrule (e.g. @app decorators in a broader sense handled by decorator)
  'atrule': { color: '#f0abfc' },
};

interface CodeBlockProps {
  code: string;
  language?: string;
  filename?: string;
  showLineNumbers?: boolean;
}

export function CodeBlock({ code, language = 'python', filename, showLineNumbers = false }: CodeBlockProps) {
  return (
    <div className="relative rounded-xl overflow-hidden border border-white/10 shadow-2xl shadow-black/40 my-6">
      {/* Subtle glow */}
      <div className="absolute inset-0 bg-gradient-to-br from-rose-600/5 to-transparent pointer-events-none rounded-xl" />

      {/* Titlebar */}
      <div className="flex items-center justify-between px-4 py-3 bg-white/5 border-b border-white/8">
        <div className="flex gap-1.5">
          <div className="w-3 h-3 rounded-full bg-[#ff5f56] border border-black/20" />
          <div className="w-3 h-3 rounded-full bg-[#febc2e] border border-black/20" />
          <div className="w-3 h-3 rounded-full bg-[#28c840] border border-black/20" />
        </div>
        {filename && (
          <span className="text-[11px] font-medium text-white/30 font-mono tracking-wide">{filename}</span>
        )}
        <div className={filename ? 'w-16' : 'w-full'} />
      </div>

      {/* Highlighted code */}
      <SyntaxHighlighter
        language={language}
        style={shanksTheme}
        showLineNumbers={showLineNumbers}
        lineNumberStyle={{ color: '#334155', minWidth: '2.5em', paddingRight: '1em', userSelect: 'none' }}
        customStyle={{
          margin: 0,
          borderRadius: 0,
          background: '#0d0608',
          fontSize: '0.875rem',
        }}
        codeTagProps={{ style: { fontFamily: 'inherit' } }}
      >
        {code.trim()}
      </SyntaxHighlighter>
    </div>
  );
}
