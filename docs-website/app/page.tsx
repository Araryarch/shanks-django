import Link from 'next/link'

export default function Home() {
  return (
    <div className="min-h-screen bg-black text-white">
      {/* Header */}
      <nav className="border-b border-neutral-900">
        <div className="max-w-7xl mx-auto px-6 py-4 flex justify-between items-center">
          <Link href="/" className="text-sm font-medium tracking-tight">SHANKS</Link>
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

      {/* Hero */}
      <div className="max-w-7xl mx-auto px-6 pt-32 pb-24">
        <div className="max-w-3xl">
          <div className="inline-block px-3 py-1 mb-6 text-[10px] tracking-widest bg-red-600/10 text-red-500 border border-red-600/20">
            DJANGO FRAMEWORK
          </div>
          <h1 className="text-6xl font-light tracking-tight mb-6 leading-[1.1]">
            Express.js-like<br />routing for Django
          </h1>
          <p className="text-lg text-neutral-500 mb-10 leading-relaxed font-light">
            No urls.py. No complexity. Just clean, simple routing with Prisma-like ORM.
          </p>
          <div className="flex gap-3">
            <Link 
              href="/docs/getting-started"
              className="px-6 py-3 bg-white text-black text-xs font-medium hover:bg-neutral-200 transition"
            >
              Get Started
            </Link>
            <Link 
              href="/docs"
              className="px-6 py-3 border border-neutral-800 text-xs font-medium hover:border-neutral-700 hover:bg-neutral-950 transition"
            >
              Documentation
            </Link>
          </div>
        </div>
      </div>

      {/* Code Example */}
      <div className="max-w-7xl mx-auto px-6 pb-24">
        <div className="max-w-3xl border border-neutral-900 bg-neutral-950/50">
          <div className="border-b border-neutral-900 px-4 py-2 flex items-center gap-2">
            <div className="w-3 h-3 border border-neutral-800"></div>
            <div className="text-[10px] text-neutral-600 tracking-wider">app/routes/__init__.py</div>
          </div>
          <pre className="p-6 overflow-x-auto text-[13px] leading-relaxed">
            <code>
              <span className="text-red-500">from</span> <span className="text-white">shanks</span> <span className="text-red-500">import</span> <span className="text-white">App</span>{'\n\n'}
              <span className="text-neutral-600">app = App()</span>{'\n\n'}
              <span className="text-red-500">@app.get</span><span className="text-neutral-500">(</span><span className="text-neutral-400">"api/posts"</span><span className="text-neutral-500">)</span>{'\n'}
              <span className="text-red-500">def</span> <span className="text-white">list_posts</span><span className="text-neutral-500">(</span><span className="text-neutral-600">req</span><span className="text-neutral-500">)</span><span className="text-neutral-500">:</span>{'\n'}
              {'    '}<span className="text-red-500">return</span> <span className="text-neutral-500">{'{'}</span><span className="text-neutral-400">"posts"</span><span className="text-neutral-500">:</span> <span className="text-neutral-500">[]{'}'}</span>{'\n\n'}
              <span className="text-neutral-600">urlpatterns = app.get_urls()</span>
            </code>
          </pre>
        </div>
      </div>

      {/* Features */}
      <div className="max-w-7xl mx-auto px-6 py-24 border-t border-neutral-900">
        <div className="grid md:grid-cols-3 gap-12">
          <div>
            <div className="text-[10px] text-red-500 mb-3 tracking-widest">ROUTING</div>
            <h3 className="text-base font-medium mb-2">Simple & Clean</h3>
            <p className="text-sm text-neutral-500 leading-relaxed font-light">
              Express.js-like routing with grouping. No more Django urls.py complexity.
            </p>
          </div>

          <div>
            <div className="text-[10px] text-red-500 mb-3 tracking-widest">DATABASE</div>
            <h3 className="text-base font-medium mb-2">Prisma-like ORM</h3>
            <p className="text-sm text-neutral-500 leading-relaxed font-light">
              Clean ORM syntax with find_many(), find_unique(), create() and more.
            </p>
          </div>

          <div>
            <div className="text-[10px] text-red-500 mb-3 tracking-widest">DOCUMENTATION</div>
            <h3 className="text-base font-medium mb-2">Auto Swagger</h3>
            <p className="text-sm text-neutral-500 leading-relaxed font-light">
              Automatic API documentation with Swagger UI. Zero configuration needed.
            </p>
          </div>
        </div>
      </div>

      {/* Why Section */}
      <div className="max-w-7xl mx-auto px-6 py-24 border-t border-neutral-900">
        <h2 className="text-2xl font-light tracking-tight mb-16">Why Shanks?</h2>
        <div className="grid md:grid-cols-2 gap-x-12 gap-y-8 max-w-4xl">
          <div className="border-l border-red-600 pl-6">
            <h3 className="text-sm font-medium mb-2">No urls.py</h3>
            <p className="text-sm text-neutral-500 leading-relaxed font-light">
              Routes are auto-configured. Just export urlpatterns from your routes module.
            </p>
          </div>
          <div className="border-l border-neutral-800 pl-6">
            <h3 className="text-sm font-medium mb-2">Route Grouping</h3>
            <p className="text-sm text-neutral-500 leading-relaxed font-light">
              Group routes with prefixes like Gin/Express. Clean and organized.
            </p>
          </div>
          <div className="border-l border-neutral-800 pl-6">
            <h3 className="text-sm font-medium mb-2">Built-in Auth</h3>
            <p className="text-sm text-neutral-500 leading-relaxed font-light">
              JWT authentication middleware included. Secure by default.
            </p>
          </div>
          <div className="border-l border-neutral-800 pl-6">
            <h3 className="text-sm font-medium mb-2">Database Agnostic</h3>
            <p className="text-sm text-neutral-500 leading-relaxed font-light">
              Works with PostgreSQL, MySQL, SQLite. Easy database URL configuration.
            </p>
          </div>
        </div>
      </div>

      {/* Footer */}
      <footer className="border-t border-neutral-900 mt-24">
        <div className="max-w-7xl mx-auto px-6 py-8">
          <div className="text-[10px] text-neutral-700 tracking-wider">
            © 2024 SHANKS DJANGO. MIT LICENSE.
          </div>
        </div>
      </footer>
    </div>
  )
}
