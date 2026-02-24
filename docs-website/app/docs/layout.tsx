import Link from 'next/link'
import { Separator } from '@/components/ui/separator'

export default function DocsLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <div className="min-h-screen">
      <nav className="border-b border-border/40 sticky top-0 glass z-50">
        <div className="max-w-7xl mx-auto px-6 py-4 flex justify-between items-center">
          <Link href="/" className="text-sm font-semibold tracking-tight hover:opacity-70 transition">
            SHANKS
          </Link>
          <div className="flex gap-6 text-sm">
            <Link href="/docs" className="text-muted-foreground hover:text-foreground transition">
              Docs
            </Link>
            <a href="https://github.com" className="text-muted-foreground hover:text-foreground transition">
              GitHub
            </a>
          </div>
        </div>
      </nav>
      
      <div className="max-w-7xl mx-auto px-6 py-12">
        <div className="flex gap-12">
          <aside className="w-64 flex-shrink-0">
            <nav className="sticky top-24 space-y-8">
              <div>
                <div className="text-xs text-muted-foreground/70 mb-4 font-semibold tracking-wider">GETTING STARTED</div>
                <div className="space-y-1">
                  <Link
                    href="/docs/getting-started"
                    className="block px-3 py-2 text-sm text-muted-foreground hover:text-foreground hover:bg-muted/50 rounded-lg transition"
                  >
                    Quick Start
                  </Link>
                  <Link
                    href="/docs/installation"
                    className="block px-3 py-2 text-sm text-muted-foreground hover:text-foreground hover:bg-muted/50 rounded-lg transition"
                  >
                    Installation
                  </Link>
                </div>
              </div>

              <Separator />

              <div>
                <div className="text-xs text-muted-foreground/70 mb-4 font-semibold tracking-wider">CORE CONCEPTS</div>
                <div className="space-y-1">
                  <Link
                    href="/docs/configuration"
                    className="block px-3 py-2 text-sm text-muted-foreground hover:text-foreground hover:bg-muted/50 rounded-lg transition"
                  >
                    Configuration
                  </Link>
                  <Link
                    href="/docs/routing"
                    className="block px-3 py-2 text-sm text-muted-foreground hover:text-foreground hover:bg-muted/50 rounded-lg transition"
                  >
                    Routing
                  </Link>
                  <Link
                    href="/docs/orm"
                    className="block px-3 py-2 text-sm text-muted-foreground hover:text-foreground hover:bg-muted/50 rounded-lg transition"
                  >
                    ORM
                  </Link>
                  <Link
                    href="/docs/caching"
                    className="block px-3 py-2 text-sm text-foreground font-medium bg-muted/50 rounded-lg transition"
                  >
                    Caching
                  </Link>
                  <Link
                    href="/docs/authentication"
                    className="block px-3 py-2 text-sm text-muted-foreground hover:text-foreground hover:bg-muted/50 rounded-lg transition"
                  >
                    Authentication
                  </Link>
                  <Link
                    href="/docs/middleware"
                    className="block px-3 py-2 text-sm text-muted-foreground hover:text-foreground hover:bg-muted/50 rounded-lg transition"
                  >
                    Middleware
                  </Link>
                </div>
              </div>

              <Separator />

              <div>
                <div className="text-xs text-muted-foreground/70 mb-4 font-semibold tracking-wider">TOOLS</div>
                <div className="space-y-1">
                  <Link
                    href="/docs/swagger"
                    className="block px-3 py-2 text-sm text-muted-foreground hover:text-foreground hover:bg-muted/50 rounded-lg transition"
                  >
                    Swagger
                  </Link>
                  <Link
                    href="/docs/cli"
                    className="block px-3 py-2 text-sm text-muted-foreground hover:text-foreground hover:bg-muted/50 rounded-lg transition"
                  >
                    CLI
                  </Link>
                </div>
              </div>
            </nav>
          </aside>
          
          <main className="flex-1 max-w-3xl pb-24 animate-in">
            <div className="prose prose-neutral dark:prose-invert max-w-none">
              {children}
            </div>
          </main>
        </div>
      </div>
    </div>
  )
}
