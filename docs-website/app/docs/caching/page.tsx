import { DocPage, CodeBlock, Callout } from '@/components/DocPage';
import Link from 'next/link';

export default function CachingPage() {
  return (
    <DocPage title="Caching" description="Shanks caches all GET requests automatically — zero configuration, 10× faster responses.">

      <Callout type="success" title="Enabled by Default">
        You don't need to do anything. Auto-caching is active the moment you create an <code>App()</code> instance.
      </Callout>

      <h2>How It Works</h2>
      <p>
        Every <code>GET</code> request is automatically cached in memory. The first request hits your database and stores the result.
        Subsequent identical requests are served straight from cache — no DB round-trip.
      </p>
      <p>
        Writes (<code>POST</code>, <code>PUT</code>, <code>DELETE</code>) automatically invalidate the related cache using
        pattern matching, so you never serve stale data.
      </p>

      <h2>Basic Example</h2>
      <CodeBlock
        filename="internal/routes/__init__.py"
        code={`from shanks import App

app = App()

@app.get('api/posts')
def list_posts(req):
    # First request: DB query, result cached
    # Next requests: served from cache (10x faster!)
    posts = Post.find_many()
    return {'posts': [p.__dict__ for p in posts]}

@app.post('api/posts')
def create_post(req):
    # Automatically invalidates /api/posts cache
    post = Post.create(**req.body)
    return {'id': post.id}`}
      />

      <h2>Cache TTL</h2>
      <p>Default TTL is <strong>5 minutes</strong>. You can change it globally or per route group:</p>
      <CodeBlock
        code={`# Change global TTL (seconds)
app.cache_config(ttl=600)   # 10 minutes

# Cache only GET and HEAD
app.cache_config(ttl=300, methods=['GET', 'HEAD'])

# Per-group config
api_v1 = app.group('api/v1')
api_v1.cache_config(ttl=60)   # 1 minute`}
      />

      <h2>Disable Cache for a Group</h2>
      <CodeBlock
        code={`# Real-time endpoints should bypass cache
realtime = app.group('api/realtime')
realtime.disable_cache()

@realtime.get('feed')
def live_feed(req):
    return {'events': []}   # Always fresh`}
      />

      <h2>Sub-pages</h2>
      <div className="not-prose grid gap-3 sm:grid-cols-3 my-6">
        {[
          { href: '/docs/caching/auto', title: 'Auto Cache', desc: 'Default behaviour' },
          { href: '/docs/caching/manual', title: 'Manual Cache', desc: 'Direct cache control' },
          { href: '/docs/caching/invalidation', title: 'Invalidation', desc: 'How invalidation works' },
        ].map(l => (
          <Link key={l.href} href={l.href} className="block rounded-xl border border-white/10 bg-white/3 hover:bg-white/6 p-4 transition-all hover:-translate-y-0.5">
            <p className="font-semibold text-white/90">{l.title}</p>
            <p className="text-sm text-white/40">{l.desc}</p>
          </Link>
        ))}
      </div>
    </DocPage>
  );
}
