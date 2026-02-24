import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';

export default function CachingPage() {
  return (
    <div className="space-y-12">
      <div className="space-y-4">
        <h1 className="text-4xl font-bold tracking-tight">Built-in Caching</h1>
        <p className="text-xl text-muted-foreground">
          Shanks includes automatic caching for GET requests - 10x faster responses with zero configuration.
        </p>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Auto-Cache</CardTitle>
          <CardDescription>
            All GET requests are automatically cached for 5 minutes. No code changes needed!
          </CardDescription>
        </CardHeader>
        <CardContent>
          <pre className="bg-background border border-border rounded-lg p-4 overflow-x-auto">
            <code className="text-sm">{`from shanks import App, auto_cache

app = App()

# Enable auto-caching (enabled by default in new projects)
app.use(auto_cache)

@app.get("api/posts")
def list_posts(req):
    # First request: fetches from DB, caches result
    # Subsequent requests: served from cache (10x faster!)
    return {"posts": [...]}`}</code>
          </pre>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Smart Cache Invalidation</CardTitle>
          <CardDescription>
            Cache is automatically cleared when you POST/PUT/DELETE. No manual invalidation needed!
          </CardDescription>
        </CardHeader>
        <CardContent>
          <pre className="bg-background border border-border rounded-lg p-4 overflow-x-auto">
            <code className="text-sm">{`from shanks import smart_cache_invalidation

app.use(smart_cache_invalidation)

@app.post("api/posts")
def create_post(req):
    # This automatically invalidates /api/posts cache
    post = Post.create(**req.body)
    return {"id": post.id}`}</code>
          </pre>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Custom TTL</CardTitle>
          <CardDescription>
            Set custom cache duration per endpoint using the @cache decorator.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <pre className="bg-background border border-border rounded-lg p-4 overflow-x-auto">
            <code className="text-sm">{`from shanks import cache

@app.get("api/posts")
@cache(ttl=600)  # Cache for 10 minutes
def list_posts(req):
    return {"posts": [...]}

@app.get("api/stats")
@cache(ttl=3600)  # Cache for 1 hour
def get_stats(req):
    return {"stats": {...}}`}</code>
          </pre>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Manual Cache Control</CardTitle>
          <CardDescription>
            For advanced use cases, you can manually control the cache.
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-6">
          <div>
            <h3 className="text-lg font-semibold mb-3">Invalidate Cache</h3>
            <pre className="bg-background border border-border rounded-lg p-4 overflow-x-auto">
              <code className="text-sm">{`from shanks import invalidate_cache

# Clear all cache
invalidate_cache()

# Clear specific pattern
invalidate_cache("/api/posts")

# In your endpoint
@app.post("api/posts")
def create_post(req):
    post = Post.create(**req.body)
    invalidate_cache("/api/posts")  # Manual invalidation
    return {"id": post.id}`}</code>
            </pre>
          </div>

          <div>
            <h3 className="text-lg font-semibold mb-3">Direct Cache Access</h3>
            <pre className="bg-background border border-border rounded-lg p-4 overflow-x-auto">
              <code className="text-sm">{`from shanks import get_cache

cache = get_cache()

# Set value
cache.set("my_key", "my_value", ttl=300)

# Get value
value = cache.get("my_key")

# Delete value
cache.delete("my_key")

# Clear all
cache.clear()

# Invalidate pattern
cache.invalidate_pattern("/api/posts")`}</code>
            </pre>
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>How It Works</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-3">
            <div className="flex items-start gap-3">
              <span className="text-primary font-mono font-bold">1.</span>
              <p className="text-muted-foreground">First GET request → Fetches from database, caches result</p>
            </div>
            <div className="flex items-start gap-3">
              <span className="text-primary font-mono font-bold">2.</span>
              <p className="text-muted-foreground">Subsequent GET requests → Served from cache (10x faster!)</p>
            </div>
            <div className="flex items-start gap-3">
              <span className="text-primary font-mono font-bold">3.</span>
              <p className="text-muted-foreground">POST/PUT/DELETE → Automatically invalidates related cache</p>
            </div>
            <div className="flex items-start gap-3">
              <span className="text-primary font-mono font-bold">4.</span>
              <p className="text-muted-foreground">Next GET request → Fresh data fetched and cached again</p>
            </div>
          </div>
        </CardContent>
      </Card>

      <div className="space-y-4">
        <h2 className="text-2xl font-bold">Performance</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <Card>
            <CardHeader>
              <CardTitle className="text-primary">Without Cache</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-4xl font-mono font-bold mb-2">~50ms</p>
              <p className="text-sm text-muted-foreground">Database query time</p>
            </CardContent>
          </Card>
          <Card>
            <CardHeader>
              <CardTitle className="text-primary">With Cache</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-4xl font-mono font-bold mb-2">~5ms</p>
              <p className="text-sm text-muted-foreground">Memory access time</p>
            </CardContent>
          </Card>
        </div>
        <Card className="bg-primary text-primary-foreground">
          <CardContent className="pt-6">
            <p className="text-2xl font-bold text-center">10x Faster!</p>
          </CardContent>
        </Card>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Benefits</CardTitle>
        </CardHeader>
        <CardContent>
          <ul className="space-y-3">
            <li className="flex items-start gap-3">
              <span className="text-xl">⚡</span>
              <span className="text-muted-foreground">10x faster response times for cached requests</span>
            </li>
            <li className="flex items-start gap-3">
              <span className="text-xl">🔄</span>
              <span className="text-muted-foreground">Automatic - no code changes needed</span>
            </li>
            <li className="flex items-start gap-3">
              <span className="text-xl">🧠</span>
              <span className="text-muted-foreground">Smart invalidation on write operations</span>
            </li>
            <li className="flex items-start gap-3">
              <span className="text-xl">💾</span>
              <span className="text-muted-foreground">Memory efficient with TTL-based expiration</span>
            </li>
            <li className="flex items-start gap-3">
              <span className="text-xl">🎯</span>
              <span className="text-muted-foreground">Pattern-based cache invalidation</span>
            </li>
          </ul>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Disable Caching</CardTitle>
          <CardDescription>
            To disable caching for specific routes, create a separate router without the cache middleware.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <pre className="bg-background border border-border rounded-lg p-4 overflow-x-auto">
            <code className="text-sm">{`# Create router without caching
no_cache_router = App()

@no_cache_router.get("api/realtime")
def realtime_data(req):
    return {"timestamp": time.time()}

# Include without cache middleware
app.include(no_cache_router)`}</code>
          </pre>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Configuration</CardTitle>
          <CardDescription>
            Default settings work for most use cases, but you can customize:
          </CardDescription>
        </CardHeader>
        <CardContent>
          <ul className="space-y-3">
            <li className="flex items-start gap-3">
              <span className="text-primary">•</span>
              <span className="text-muted-foreground"><code className="text-sm bg-muted px-1.5 py-0.5 rounded">ttl</code> - Time to live in seconds (default: 300 = 5 minutes)</span>
            </li>
            <li className="flex items-start gap-3">
              <span className="text-primary">•</span>
              <span className="text-muted-foreground"><code className="text-sm bg-muted px-1.5 py-0.5 rounded">methods</code> - HTTP methods to cache (default: ['GET'])</span>
            </li>
          </ul>
        </CardContent>
      </Card>
    </div>
  );
}
