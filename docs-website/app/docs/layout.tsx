import Link from 'next/link'

const navigation = [
  { name: 'Getting Started', href: '/docs/getting-started' },
  { name: 'Installation', href: '/docs/installation' },
  { name: 'Routing', href: '/docs/routing' },
  { name: 'ORM', href: '/docs/orm' },
  { name: 'Authentication', href: '/docs/authentication' },
  { name: 'Middleware', href: '/docs/middleware' },
  { name: 'Swagger', href: '/docs/swagger' },
  { name: 'CLI', href: '/docs/cli' },
]

export default function DocsLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <div className="min-h-screen bg-black text-white">
      <nav className="border-b border-neutral-900 sticky top-0 bg-black/95 backdrop-blur z-50">
        <div className="max-w-7xl mx-auto px-6 py-4 flex justify-between items-center">
          <Link href="/" className="text-sm font-medium tracking-tight">
            SHANKS
          </Link>
          <div className="flex gap-6 text-xs">
            <Link href="/docs" className="text-neutral-500 hover:text-white transition">
              Documentation
            </Link>
            <a href="https://github.com" className="text-neutral-500 hover:text-white transition">
              GitHub
            </a>
          </div>
        </div>
      </nav>
      
      <div className="max-w-7xl mx-auto px-6 py-12">
        <div className="flex gap-12">
          <aside className="w-56 flex-shrink-0">
            <nav className="sticky top-24 space-y-6">
              <div>
                <div className="text-[10px] text-neutral-600 mb-3 tracking-widest">GETTING STARTED</div>
                <div className="space-y-1">
                  <Link
                    href="/docs/getting-started"
                    className="block px-3 py-1.5 text-xs text-neutral-500 hover:text-white transition"
                  >
                    Quick Start
                  </Link>
                  <Link
                    href="/docs/installation"
                    className="block px-3 py-1.5 text-xs text-neutral-500 hover:text-white transition"
                  >
                    Installation
                  </Link>
                </div>
              </div>

              <div>
                <div className="text-[10px] text-neutral-600 mb-3 tracking-widest">CORE CONCEPTS</div>
                <div className="space-y-1">
                  <Link
                    href="/docs/configuration"
                    className="block px-3 py-1.5 text-xs text-neutral-500 hover:text-white transition"
                  >
                    Configuration
                  </Link>
                  <Link
                    href="/docs/routing"
                    className="block px-3 py-1.5 text-xs text-neutral-500 hover:text-white transition"
                  >
                    Routing
                  </Link>
                  <Link
                    href="/docs/orm"
                    className="block px-3 py-1.5 text-xs text-neutral-500 hover:text-white transition"
                  >
                    ORM
                  </Link>
                  <Link
                    href="/docs/authentication"
                    className="block px-3 py-1.5 text-xs text-neutral-500 hover:text-white transition"
                  >
                    Authentication
                  </Link>
                  <Link
                    href="/docs/middleware"
                    className="block px-3 py-1.5 text-xs text-neutral-500 hover:text-white transition"
                  >
                    Middleware
                  </Link>
                </div>
              </div>

              <div>
                <div className="text-[10px] text-neutral-600 mb-3 tracking-widest">TOOLS</div>
                <div className="space-y-1">
                  <Link
                    href="/docs/swagger"
                    className="block px-3 py-1.5 text-xs text-neutral-500 hover:text-white transition"
                  >
                    Swagger
                  </Link>
                  <Link
                    href="/docs/cli"
                    className="block px-3 py-1.5 text-xs text-neutral-500 hover:text-white transition"
                  >
                    CLI
                  </Link>
                </div>
              </div>
            </nav>
          </aside>
          
          <main className="flex-1 max-w-3xl pb-24">
            {children}
          </main>
        </div>
      </div>
    </div>
  )
}
