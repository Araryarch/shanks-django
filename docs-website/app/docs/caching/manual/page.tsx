import { DocPage, CodeBlock } from '@/components/DocPage';

export default function ManualCachePage() {
  return (
    <DocPage title="Manual Cache" description="Access the cache directly using get_cache() for fine-grained control.">

      <h2>Cache API</h2>
      <CodeBlock
        code={`from shanks import get_cache, invalidate_cache

cache = get_cache()

# Store a value (ttl in seconds)
cache.set('my_key', {'data': 'value'}, ttl=300)

# Retrieve a value (None if missing/expired)
value = cache.get('my_key')

# Delete a specific key
cache.delete('my_key')

# Clear ALL cache
invalidate_cache()

# Clear by URL pattern
invalidate_cache('/api/posts')`}
      />

      <h2>Use Case: Expensive Computation</h2>
      <CodeBlock
        filename="internal/routes/stats.py"
        code={`from shanks import App, get_cache

app = App()
cache = get_cache()

@app.get('api/stats')
def get_stats(req):
    cached = cache.get('global_stats')
    if cached:
        return cached

    # Expensive aggregation
    stats = compute_heavy_stats()
    cache.set('global_stats', stats, ttl=3600)
    return stats`}
      />

      <h2>Invalidate on Write</h2>
      <CodeBlock
        code={`@app.post('api/orders')
def create_order(req):
    order = Order.create(**req.body)
    # Clear stats since they changed
    invalidate_cache('/api/stats')
    return {'id': order.id}`}
      />
    </DocPage>
  );
}
