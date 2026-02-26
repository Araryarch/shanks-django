import { DocPage, CodeBlock, Callout } from '@/components/DocPage';
import Link from 'next/link';

export default function RoutingBasicPage() {
  return (
    <DocPage title="Basic Routes" description="Define GET, POST, PUT, DELETE, and PATCH routes with clean Python decorators.">

      <h2>HTTP Method Decorators</h2>
      <CodeBlock
        filename="internal/routes/__init__.py"
        code={`from shanks import App, Response

app = App()

@app.get('api/posts')
def list_posts(req):
    return {'posts': []}

@app.post('api/posts')
def create_post(req):
    data = req.body  # Parsed JSON
    post = Post.create(**data)
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

@app.patch('api/posts/<post_id>')
def patch_post(req, post_id):
    post = Post.find_unique(id=post_id)
    post.update_self(**req.body)
    return {'patched': True}

urlpatterns = app.get_urls()`}
      />

      <h2>The Request Object</h2>
      <CodeBlock
        code={`def handler(req):
    req.method      # 'GET', 'POST', etc.
    req.path        # '/api/posts'
    req.body        # Parsed JSON dict (POST/PUT/PATCH)
    req.query       # Query params: req.query.get('page', 1)
    req.headers     # Request headers
    req.user        # Authenticated User object (or None)
    req.session     # Django session
    req.cookies     # Cookies dict
    req.files       # Uploaded files`}
      />

      <h2>Custom Responses</h2>
      <CodeBlock
        code={`from shanks import Response

# Set status code
return Response().status_code(201).json({'id': 1})

# 404 Not Found
return Response().status_code(404).json({'error': 'Not found'})

# 400 Bad Request
return Response().status_code(400).json({'error': 'Invalid data'})`}
      />

      <Callout type="info">
        Returning a plain <code>dict</code> automatically becomes a <code>200 OK</code> JSON response.
      </Callout>

      <h2>Query Parameters</h2>
      <CodeBlock
        code={`@app.get('api/posts')
def list_posts(req):
    page  = int(req.query.get('page', 1))
    limit = int(req.query.get('limit', 10))
    posts = Post.find_many()
    return {'posts': posts, 'page': page, 'limit': limit}`}
      />
    </DocPage>
  );
}
