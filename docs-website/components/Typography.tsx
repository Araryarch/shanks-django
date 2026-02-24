import { ReactNode } from 'react'

export function H1({ children, className }: { children: ReactNode; className?: string }) {
  return (
    <h1 className={`text-4xl font-bold tracking-tight mb-6 ${className || ''}`}>
      {children}
    </h1>
  )
}

export function H2({ children, className }: { children: ReactNode; className?: string }) {
  return (
    <h2 className={`text-2xl font-semibold mb-4 mt-12 first:mt-0 ${className || ''}`}>
      {children}
    </h2>
  )
}

export function H3({ children, className }: { children: ReactNode; className?: string }) {
  return (
    <h3 className={`text-lg font-semibold mb-3 mt-8 ${className || ''}`}>
      {children}
    </h3>
  )
}

export function P({ children, className }: { children: ReactNode; className?: string }) {
  return (
    <p className={`text-base text-muted-foreground mb-4 leading-relaxed ${className || ''}`}>
      {children}
    </p>
  )
}

export function Lead({ children }: { children: ReactNode }) {
  return (
    <p className="text-lg text-muted-foreground mb-8 leading-relaxed">
      {children}
    </p>
  )
}

export function Code({ children }: { children: ReactNode }) {
  return (
    <code className="text-sm text-accent bg-muted px-1.5 py-0.5 rounded font-mono">
      {children}
    </code>
  )
}

export function InlineCode({ children }: { children: ReactNode }) {
  return (
    <code className="text-sm text-accent bg-muted px-1.5 py-0.5 rounded font-mono">
      {children}
    </code>
  )
}

export function CodeBlock({ 
  children, 
  language,
  title
}: { 
  children: ReactNode
  language?: string
  title?: string
}) {
  return (
    <div className="border border-border rounded-lg overflow-hidden mb-6 bg-card">
      {(language || title) && (
        <div className="border-b border-border px-4 py-2 bg-muted/30">
          <div className="text-xs text-muted-foreground">{title || language}</div>
        </div>
      )}
      <pre className="p-4 overflow-x-auto text-sm leading-relaxed">
        <code className="font-mono">{children}</code>
      </pre>
    </div>
  )
}

export function SimpleCodeBlock({ children }: { children: ReactNode }) {
  return (
    <div className="border border-border rounded-lg p-4 mb-6 bg-card">
      <code className="text-sm font-mono">{children}</code>
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
    info: 'border-border bg-muted/30',
    success: 'border-accent bg-accent/10',
    warning: 'border-border bg-muted/30'
  }
  
  return (
    <div className={`border-l-2 pl-6 py-4 mb-6 ${styles[type]}`}>
      {children}
    </div>
  )
}

export function List({ children }: { children: ReactNode }) {
  return (
    <ul className="space-y-2 mb-4">
      {children}
    </ul>
  )
}

export function ListItem({ children }: { children: ReactNode }) {
  return (
    <li className="flex items-start gap-2 text-muted-foreground">
      <span className="text-accent mt-0.5">→</span>
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
    <div className="grid grid-cols-2 gap-4 mb-6">
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
    <div className="border border-border rounded-lg p-4 bg-card">
      <code className="text-accent text-sm">{title}</code>
      <p className="text-muted-foreground text-sm mt-2">{description}</p>
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
      className="block p-6 border border-border rounded-lg hover:border-accent/50 bg-card hover:bg-muted/30 transition"
    >
      <div className="flex items-start justify-between mb-2">
        <div className="text-xs text-muted-foreground font-semibold tracking-wider">{badge}</div>
        <div className="text-muted-foreground">→</div>
      </div>
      <h2 className="text-lg font-semibold mb-1">{title}</h2>
      <p className="text-sm text-muted-foreground">{description}</p>
    </a>
  )
}
