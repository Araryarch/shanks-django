import { DocPage, CodeBlock, Callout } from '@/components/DocPage';

export default function AutoCachePage() {
  return (
    <DocPage title="Auto Cache" description="GET requests are cached automatically — no code changes needed.">

      <h2>Default Behaviour</h2>
      <p>
        When you create an <code>App()</code> instance, auto-caching is active. Every <code>GET</code> request is cached
        after the first response. Cache entries expire after 5 minutes by default.
      </p>

      <CodeBlock
        filename="internal/routes/__init__.py"
        code={`from shanks import App

app = App()  # Auto-cache enabled

@app.get('api/products')
def list_products(req):
    # Request 1 → DB query + cached
    # Request 2+ → served from cache
    return {'products': Product.find_many()}`}
      />

      <Callout type="info" title="Cache Key">
        The cache key is the full request URL including query parameters.
        <code>GET /api/posts?page=1</code> and <code>GET /api/posts?page=2</code> are cached separately.
      </Callout>

      <h2>Cache Invalidation on Writes</h2>
      <p>
        When a <code>POST</code>, <code>PUT</code>, or <code>DELETE</code> request succeeds on a path,
        Shanks pattern-matches and clears related cache entries automatically:
      </p>
      <CodeBlock
        code={`# DELETE /api/posts/42
# ↳ invalidates /api/posts  (parent path)
# ↳ invalidates /api/posts/42  (exact match)`}
        language="text"
      />

      <h2>Configuring TTL</h2>
      <CodeBlock
        code={`app.cache_config(ttl=300)    # 5 minutes (default)
app.cache_config(ttl=3600)   # 1 hour
app.cache_config(ttl=0)      # Disable expiry (until invalidated)`}
      />
    </DocPage>
  );
}
