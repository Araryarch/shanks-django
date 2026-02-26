import { DocPage, CodeBlock, Callout } from '@/components/DocPage';

export default function CacheInvalidationPage() {
  return (
    <DocPage title="Cache Invalidation" description="How Shanks automatically and manually clears cache on writes.">

      <h2>Automatic Invalidation</h2>
      <p>
        Every <code>POST</code>, <code>PUT</code>, <code>PATCH</code>, and <code>DELETE</code> request
        automatically triggers cache invalidation using pattern matching:
      </p>

      <CodeBlock
        language="text"
        code={`Request: DELETE /api/posts/42

Shanks invalidates:
  ✓ /api/posts/42      (exact match)
  ✓ /api/posts         (parent path)
  — /api/users         (unrelated, untouched)`}
      />

      <Callout type="info">
        Pattern matching is path-prefix based. <code>/api/posts/42</code> invalidates all cache entries
        whose key starts with <code>/api/posts</code>.
      </Callout>

      <h2>Manual Invalidation</h2>
      <CodeBlock
        code={`from shanks import invalidate_cache

# Invalidate a specific path pattern
invalidate_cache('/api/posts')

# Invalidate everything
invalidate_cache()`}
      />

      <h2>Selective Invalidation Example</h2>
      <CodeBlock
        filename="internal/routes/posts.py"
        code={`from shanks import App, Response, invalidate_cache

app = App()

@app.put('api/posts/<post_id>')
def update_post(req, post_id):
    post = Post.find_unique(id=post_id)
    if not post:
        return Response().status_code(404).json({'error': 'Not found'})
    post.update_self(**req.body)
    # Auto-invalidation handles this, but you can be explicit:
    invalidate_cache(f'/api/posts/{post_id}')
    invalidate_cache('/api/posts')
    return {'updated': True}`}
      />
    </DocPage>
  );
}
