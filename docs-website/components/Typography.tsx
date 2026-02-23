import { ReactNode } from 'react'

export function H1({ children }: { children: ReactNode }) {
  return (
    <h1 className="text-4xl font-light tracking-tight mb-4 text-white">
      {children}
    </h1>
  )
}

export function H2({ children }: { children: ReactNode }) {
  return (
    <h2 className="text-xl font-medium mb-4 tracking-tight text-white mt-12 first:mt-0">
      {children}
    </h2>
  )
}

export function H3({ children }: { children: ReactNode }) {
  return (
    <h3 className="text-sm font-medium mb-2 text-white">
      {children}
    </h3>
  )
}

export function P({ children }: { children: ReactNode }) {
  return (
    <p className="text-sm text-neutral-500 mb-4 leading-relaxed font-light">
      {children}
    </p>
  )
}

export function Lead({ children }: { children: ReactNode }) {
  return (
    <p className="text-sm text-neutral-500 mb-12 leading-relaxed font-light">
      {children}
    </p>
  )
}

export function InlineCode({ children }: { children: ReactNode }) {
  return (
    <code className="text-xs text-red-500 bg-red-950/30 px-1.5 py-0.5 border border-red-900/30">
      {children}
    </code>
  )
}

export function CodeBlock({ 
  children, 
  title 
}: { 
  children: ReactNode
  title?: string 
}) {
  return (
    <div className="border border-neutral-900 bg-neutral-950/50 mb-4">
      {title && (
        <div className="border-b border-neutral-900 px-4 py-2">
          <div className="text-[10px] text-neutral-600 tracking-wider">{title}</div>
        </div>
      )}
      <pre className="p-4 overflow-x-auto text-xs leading-relaxed">
        <code>{children}</code>
      </pre>
    </div>
  )
}

export function SimpleCodeBlock({ children }: { children: ReactNode }) {
  return (
    <div className="border border-neutral-900 bg-neutral-950/50 p-4 mb-4">
      <code className="text-xs text-neutral-400">{children}</code>
    </div>
  )
}

export function Alert({ 
  children, 
  type = 'info' 
}: { 
  children: ReactNode
  type?: 'info' | 'success' | 'warning'
}) {
  const styles = {
    info: 'border-neutral-800 bg-neutral-950/30',
    success: 'border-red-600 bg-red-950/10',
    warning: 'border-neutral-800 bg-neutral-950/30'
  }
  
  return (
    <div className={`border-l-2 pl-6 py-4 ${styles[type]}`}>
      {children}
    </div>
  )
}

export function List({ children }: { children: ReactNode }) {
  return (
    <ul className="space-y-2 text-sm text-neutral-500 mb-4">
      {children}
    </ul>
  )
}

export function ListItem({ children }: { children: ReactNode }) {
  return (
    <li className="flex items-start gap-2">
      <span className="text-red-500 mt-0.5">→</span>
      <span>{children}</span>
    </li>
  )
}

export function Section({ children }: { children: ReactNode }) {
  return (
    <section className="mb-12">
      {children}
    </section>
  )
}

export function Grid({ children }: { children: ReactNode }) {
  return (
    <div className="grid grid-cols-2 gap-3 text-xs mb-4">
      {children}
    </div>
  )
}

export function GridItem({ 
  title, 
  description 
}: { 
  title: string
  description: string 
}) {
  return (
    <div className="border border-neutral-900 bg-neutral-950/30 p-3">
      <code className="text-red-500">{title}</code>
      <p className="text-neutral-600 mt-1">{description}</p>
    </div>
  )
}

export function Card({ 
  href, 
  badge, 
  title, 
  description 
}: { 
  href: string
  badge: string
  title: string
  description: string
}) {
  return (
    <a 
      href={href} 
      className="block p-6 border border-neutral-900 hover:border-neutral-800 bg-neutral-950/30 hover:bg-neutral-950/50 transition"
    >
      <div className="flex items-start justify-between mb-2">
        <div className="text-[10px] text-neutral-600 tracking-widest">{badge}</div>
        <div className="text-neutral-600">→</div>
      </div>
      <h2 className="text-base font-medium mb-1 text-white">{title}</h2>
      <p className="text-xs text-neutral-500 font-light">{description}</p>
    </a>
  )
}
