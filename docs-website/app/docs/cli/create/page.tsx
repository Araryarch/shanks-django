import { DocPage, CodeBlock, Callout } from '@/components/DocPage';

export default function CLICreatePage() {
  return (
    <DocPage title="shanks create" description="Generate CRUD endpoints and authentication boilerplate instantly.">

      <h2>CRUD Generator</h2>
      <CodeBlock
        language="bash"
        code={`shanks create posts --crud

# Generates:
# entity/posts.py              (Model)
# internal/controller/posts.py (Controller)
# internal/routes/posts.py     (Routes)`}
      />

      <h2>Generated Routes</h2>
      <CodeBlock
        filename="internal/routes/posts.py"
        code={`from shanks import App, Response
from entity.posts import Post

app = App()

@app.get('api/posts')
def list_posts(req):
    page  = int(req.query.get('page', 1))
    limit = int(req.query.get('limit', 10))
    posts = Post.find_many()
    return {'posts': posts, 'page': page, 'limit': limit}

@app.get('api/posts/<post_id>')
def get_post(req, post_id):
    post = Post.find_unique(id=post_id)
    if not post:
        return Response().status_code(404).json({'error': 'Not found'})
    return {'post': post.__dict__}

@app.post('api/posts')
def create_post(req):
    post = Post.create(**req.body)
    return Response().status_code(201).json({'id': post.id})

@app.put('api/posts/<post_id>')
def update_post(req, post_id):
    post = Post.find_unique(id=post_id)
    post.update_self(**req.body)
    return {'updated': True}

@app.delete('api/posts/<post_id>')
def delete_post(req, post_id):
    Post.find_unique(id=post_id).delete_self()
    return {'deleted': True}

router = app`}
      />

      <h2>Auth Generator</h2>
      <CodeBlock
        language="bash"
        code={`# Simple: login, register, /me
shanks create auth --simple

# Complete: + email verification + resend
shanks create auth --complete`}
      />

      <Callout type="info">
        After generating, register the router in <code>internal/routes/__init__.py</code>:{' '}
        <code>app.include(posts.router)</code>
      </Callout>
    </DocPage>
  );
}
