import Link from 'next/link'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Separator } from '@/components/ui/separator'

export default function Home() {
  return (
    <div className="min-h-screen">
      {/* Header */}
      <nav className="border-b border-border/40 sticky top-0 glass z-50">
        <div className="max-w-7xl mx-auto px-6 py-4 flex justify-between items-center">
          <Link href="/" className="text-sm font-semibold tracking-tight">
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

      {/* Hero */}
      <div className="max-w-7xl mx-auto px-6 pt-32 pb-24 animate-in">
        <div className="max-w-3xl">
          <div className="inline-flex items-center gap-2 px-3 py-1.5 mb-8 text-xs font-medium bg-muted/50 border border-border/50 rounded-full">
            <div className="w-1.5 h-1.5 rounded-full bg-foreground animate-pulse"></div>
            Django Framework
          </div>
          <h1 className="text-6xl md:text-7xl font-bold tracking-tight mb-6 leading-[1.1] gradient-text">
            Express.js-like<br />routing for Django
          </h1>
          <p className="text-xl text-muted-foreground mb-10 leading-relaxed max-w-2xl">
            No urls.py. No complexity. Just clean, simple routing with Prisma-like ORM and built-in caching. 10x faster out of the box.
          </p>
          <div className="flex gap-3">
            <Button asChild size="lg">
              <Link href="/docs/getting-started">
                Get Started →
              </Link>
            </Button>
            <Button asChild variant="outline" size="lg">
              <Link href="/docs">
                Documentation
              </Link>
            </Button>
          </div>
        </div>
      </div>

      {/* Code Example */}
      <div className="max-w-7xl mx-auto px-6 pb-24">
        <Card className="max-w-3xl overflow-hidden">
          <CardHeader className="border-b border-border/50 bg-muted/30">
            <div className="flex items-center gap-3">
              <div className="flex gap-1.5">
                <div className="w-3 h-3 rounded-full bg-muted-foreground/20"></div>
                <div className="w-3 h-3 rounded-full bg-muted-foreground/20"></div>
                <div className="w-3 h-3 rounded-full bg-muted-foreground/20"></div>
              </div>
              <CardDescription className="text-xs">internal/routes/__init__.py</CardDescription>
            </div>
          </CardHeader>
          <CardContent className="p-6">
            <pre className="text-sm leading-relaxed border-0 p-0 bg-transparent">
              <code>
                <span className="text-muted-foreground">from</span> <span className="text-foreground">shanks</span> <span className="text-muted-foreground">import</span> <span className="text-foreground">App, auto_cache</span>{'\n\n'}
                <span className="text-muted-foreground/70">app = App()</span>{'\n'}
                <span className="text-muted-foreground/70">app.use(auto_cache)  </span><span className="text-muted-foreground/40"># 10x faster!</span>{'\n\n'}
                <span className="text-muted-foreground">@app.get</span><span className="text-muted-foreground/70">(</span><span className="text-foreground/80">"api/posts"</span><span className="text-muted-foreground/70">)</span>{'\n'}
                <span className="text-muted-foreground">def</span> <span className="text-foreground">list_posts</span><span className="text-muted-foreground/70">(req):</span>{'\n'}
                {'    '}<span className="text-muted-foreground">return</span> <span className="text-muted-foreground/70">{'{'}</span><span className="text-foreground/80">"posts"</span><span className="text-muted-foreground/70">: []{'}'}</span>
              </code>
            </pre>
          </CardContent>
        </Card>
      </div>

      {/* Features */}
      <div className="max-w-7xl mx-auto px-6 py-24">
        <Separator className="mb-24" />
        <div className="grid md:grid-cols-3 gap-6">
          <Card className="hover:border-foreground/20 transition-colors">
            <CardHeader>
              <div className="text-xs text-muted-foreground mb-3 font-semibold tracking-wider">ROUTING</div>
              <CardTitle className="text-lg">Simple & Clean</CardTitle>
            </CardHeader>
            <CardContent>
              <CardDescription className="leading-relaxed">
                Express.js-like routing with grouping. No more Django urls.py complexity.
              </CardDescription>
            </CardContent>
          </Card>

          <Card className="border-foreground/20 bg-muted/30 hover:border-foreground/30 transition-colors">
            <CardHeader>
              <div className="text-xs text-foreground mb-3 font-semibold tracking-wider">CACHING</div>
              <CardTitle className="text-lg">10x Faster</CardTitle>
            </CardHeader>
            <CardContent>
              <CardDescription className="leading-relaxed">
                Built-in auto-caching for GET requests. Zero configuration, instant performance boost.
              </CardDescription>
            </CardContent>
          </Card>

          <Card className="hover:border-foreground/20 transition-colors">
            <CardHeader>
              <div className="text-xs text-muted-foreground mb-3 font-semibold tracking-wider">DATABASE</div>
              <CardTitle className="text-lg">Prisma-like ORM</CardTitle>
            </CardHeader>
            <CardContent>
              <CardDescription className="leading-relaxed">
                Clean ORM syntax with find_many(), find_unique(), create() and more.
              </CardDescription>
            </CardContent>
          </Card>
        </div>
      </div>

      {/* Why Section */}
      <div className="max-w-7xl mx-auto px-6 py-24">
        <Separator className="mb-24" />
        <h2 className="text-3xl font-bold tracking-tight mb-16">Why Shanks?</h2>
        <div className="grid md:grid-cols-2 gap-8 max-w-4xl">
          {[
            {
              title: "Built-in Caching",
              description: "Auto-cache GET requests with smart invalidation. 10x faster responses out of the box."
            },
            {
              title: "No urls.py",
              description: "Routes are auto-configured. Just export urlpatterns from your routes module."
            },
            {
              title: "CLI Generator",
              description: "Generate CRUD & Auth endpoints with one command. Go-like project architecture."
            },
            {
              title: "Express.js Middleware",
              description: "Familiar middleware pattern with req, res, next. Easy to understand and use."
            }
          ].map((item, i) => (
            <div key={i} className="border-l-2 border-border pl-6 hover:border-foreground/50 transition-colors">
              <h3 className="text-base font-semibold mb-2">{item.title}</h3>
              <p className="text-sm text-muted-foreground leading-relaxed">
                {item.description}
              </p>
            </div>
          ))}
        </div>
      </div>

      {/* Footer */}
      <footer className="border-t border-border/40 mt-24">
        <div className="max-w-7xl mx-auto px-6 py-8">
          <div className="text-xs text-muted-foreground">
            © 2024 SHANKS DJANGO. MIT LICENSE.
          </div>
        </div>
      </footer>
    </div>
  )
}
