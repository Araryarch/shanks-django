import { DocPage, CodeBlock, Callout } from '@/components/DocPage';

export default function BlogExamplePage() {
  return (
    <DocPage title="Blog API Example" description="A complete blog REST API with posts, comments, JWT auth, and pagination.">

      <h2>Setup</h2>
      <CodeBlock
        language="bash"
        code={`shanks new blog-api
cd blog-api
shanks create posts --crud
shanks create comments --crud
shanks create auth --simple
sorm db push
shanks run`}
      />

      <h2>Post Model</h2>
      <CodeBlock
        filename="entity/post.py"
        code={`from django.db import models

class Post(models.Model):
    title      = models.CharField(max_length=255)
    content    = models.TextField()
    author     = models.ForeignKey('entity.User', on_delete=models.CASCADE, related_name='posts')
    published  = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = 'entity'
        ordering  = ['-created_at']`}
      />

      <h2>Posts Routes</h2>
      <CodeBlock
        filename="internal/routes/posts.py"
        code={`from shanks import App, Response
from entity.post import Post
from internal.middleware.auth import jwt_required

app = App()

@app.get('api/posts')
def list_posts(req):
    page  = int(req.query.get('page', 1))
    limit = int(req.query.get('limit', 10))
    posts = Post.find_many(published=True)
    start = (page - 1) * limit
    return {
        'posts': [{'id': p.id, 'title': p.title} for p in posts[start:start+limit]],
        'total': len(posts),
        'page': page,
    }

@app.post('api/posts', jwt_required)
def create_post(req):
    post = Post.create(author_id=req.user.id, **req.body)
    return Response().status_code(201).json({'id': post.id})

@app.delete('api/posts/<post_id>', jwt_required)
def delete_post(req, post_id):
    post = Post.find_unique(id=post_id)
    if not post or post.author_id != req.user.id:
        return Response().status_code(403).json({'error': 'Forbidden'})
    post.delete_self()
    return {'deleted': True}

router = app`}
      />

      <Callout type="info">
        After running <code>shanks run</code> visit{' '}
        <code>http://localhost:8000/docs</code> to see the auto-generated Swagger UI.
      </Callout>

      <h2>API Endpoints</h2>
      <CodeBlock
        language="text"
        code={`GET    /api/posts              List published posts (paginated)
GET    /api/posts/<id>         Get a single post
POST   /api/posts              Create post (JWT required)
PUT    /api/posts/<id>         Update post (author only)
DELETE /api/posts/<id>         Delete post (author only)

POST   /api/auth/register      Register user
POST   /api/auth/login         Login → JWT token
GET    /api/auth/me            Current user (JWT required)`}
      />
    </DocPage>
  );
}
