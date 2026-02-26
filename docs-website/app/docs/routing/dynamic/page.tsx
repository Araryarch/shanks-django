import { DocPage, CodeBlock, Callout } from '@/components/DocPage';

export default function RoutingDynamicPage() {
  return (
    <DocPage title="Dynamic Routes" description="Shanks auto-detects parameter types — no need to write <int:id> by hand.">

      <h2>Auto-Type Detection</h2>
      <p>
        Shanks inspects parameter names and infers their type automatically:
      </p>
      <CodeBlock
        code={`# Ends with _id → treated as int
@app.get('api/posts/<post_id>')
def get_post(req, post_id):
    return {'id': post_id}   # post_id is an int

# Other names → treated as string
@app.get('api/users/<username>')
def get_user(req, username):
    return {'username': username}  # string`}
      />

      <Callout type="info" title="Detection Rules">
        Parameters ending in <code>_id</code> or exactly <code>id</code> → <code>int</code>.
        All other parameter names → <code>str</code>.
      </Callout>

      <h2>Explicit Types</h2>
      <p>You can still force a type when needed:</p>
      <CodeBlock
        code={`@app.get('api/posts/<slug:slug>')      # force slug
def get_by_slug(req, slug):
    return {'slug': slug}

@app.get('api/items/<uuid:item_id>')   # force uuid
def get_item(req, item_id):
    return {'id': str(item_id)}`}
      />

      <h2>Multiple Parameters</h2>
      <CodeBlock
        code={`@app.get('api/users/<user_id>/posts/<post_id>')
def get_user_post(req, user_id, post_id):
    post = Post.find_unique(id=post_id, author_id=user_id)
    if not post:
        return Response().status_code(404).json({'error': 'Not found'})
    return {'post': post.__dict__}`}
      />
    </DocPage>
  );
}
