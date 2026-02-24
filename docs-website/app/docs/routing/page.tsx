import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';

export default function RoutingPage() {
  return (
    <div className="space-y-12">
      <div className="space-y-4">
        <h1 className="text-4xl font-bold tracking-tight">Routing</h1>
        <p className="text-xl text-muted-foreground">
          Express.js-like routing with grouping support. No more Django urls.py complexity.
        </p>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Basic Routes</CardTitle>
          <CardDescription>
            Define routes with decorators - just like Express.js.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <pre className="bg-background border border-border rounded-lg p-4 overflow-x-auto">
            <code className="text-sm">{`from shanks import App

app = App()

@app.get("api/posts")
def list_posts(req):
    return {"posts": []}

@app.post("api/posts")
def create_post(req):
    return {"post": {}}

@app.get("api/posts/<int:id>")
def get_post(req, id):
    return {"post": {"id": id}}

@app.put("api/posts/<int:id>")
def update_post(req, id):
    return {"updated": True}

@app.delete("api/posts/<int:id>")
def delete_post(req, id):
    return {"deleted": True}

urlpatterns = app.get_urls()`}</code>
          </pre>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Route Grouping</CardTitle>
          <CardDescription>
            Group routes with prefixes like Gin/Express - clean and organized.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <pre className="bg-background border border-border rounded-lg p-4 overflow-x-auto">
            <code className="text-sm">{`from shanks import App

app = App()

# Create route groups
api = app.group("api")
v1 = api.group("v1")

# All routes in v1 will have prefix "api/v1"
@v1.get("users")
def list_users(req):
    return {"users": []}  # GET /api/v1/users

@v1.get("posts")
def list_posts(req):
    return {"posts": []}  # GET /api/v1/posts

# Nested grouping
admin = v1.group("admin")

@admin.get("stats")
def get_stats(req):
    return {"stats": {}}  # GET /api/v1/admin/stats

urlpatterns = app.get_urls()`}</code>
          </pre>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Multiple Routers</CardTitle>
          <CardDescription>
            Organize routes in separate files for better structure.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-6">
            <div>
              <h3 className="text-lg font-semibold mb-2">internal/routes/auth.py</h3>
              <pre className="bg-background border border-border rounded-lg p-3 overflow-x-auto">
                <code className="text-sm">{`from shanks import App

router = App()

@router.post("api/auth/login")
def login(req):
    return {"token": "..."}

@router.post("api/auth/register")
def register(req):
    return {"user": {...}}`}</code>
              </pre>
            </div>

            <div>
              <h3 className="text-lg font-semibold mb-2">internal/routes/posts.py</h3>
              <pre className="bg-background border border-border rounded-lg p-3 overflow-x-auto">
                <code className="text-sm">{`from shanks import App

router = App()

@router.get("api/posts")
def list_posts(req):
    return {"posts": []}

@router.post("api/posts")
def create_post(req):
    return {"post": {...}}`}</code>
              </pre>
            </div>

            <div>
              <h3 className="text-lg font-semibold mb-2">internal/routes/__init__.py</h3>
              <pre className="bg-background border border-border rounded-lg p-3 overflow-x-auto">
                <code className="text-sm">{`from shanks import App
from . import auth, posts

app = App()

# Include all routers
app.include(auth.router, posts.router)

urlpatterns = app.get_urls()`}</code>
              </pre>
            </div>
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>URL Parameters</CardTitle>
          <CardDescription>
            Capture dynamic values from URLs.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <pre className="bg-background border border-border rounded-lg p-4 overflow-x-auto">
            <code className="text-sm">{`# Integer parameter
@app.get("api/users/<int:user_id>")
def get_user(req, user_id):
    return {"id": user_id}

# String parameter (slug)
@app.get("api/posts/<slug:slug>")
def get_post(req, slug):
    return {"slug": slug}

# Path parameter (captures slashes)
@app.get("api/files/<path:filepath>")
def get_file(req, filepath):
    return {"path": filepath}

# Multiple parameters
@app.get("api/users/<int:user_id>/posts/<int:post_id>")
def get_user_post(req, user_id, post_id):
    return {"user_id": user_id, "post_id": post_id}`}</code>
          </pre>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Query Parameters</CardTitle>
          <CardDescription>
            Access query string parameters from the request.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <pre className="bg-background border border-border rounded-lg p-4 overflow-x-auto">
            <code className="text-sm">{`@app.get("api/search")
def search(req):
    # /api/search?q=django&page=2&limit=20
    query = req.query.get('q')
    page = int(req.query.get('page', 1))
    limit = int(req.query.get('limit', 10))
    
    return {
        'query': query,
        'page': page,
        'limit': limit,
        'results': [...]
    }

@app.get("api/posts")
def list_posts(req):
    # /api/posts?published=true&author=john
    published = req.query.get('published') == 'true'
    author = req.query.get('author')
    
    posts = Post.find_many(
        published=published,
        author__username=author
    )
    return {"posts": [...]}`}</code>
          </pre>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Request Object</CardTitle>
          <CardDescription>
            Access all request data - body, headers, cookies, files, and more.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <pre className="bg-background border border-border rounded-lg p-4 overflow-x-auto">
            <code className="text-sm">{`@app.post("api/posts")
def create_post(req):
    # JSON body
    title = req.body.get('title')
    content = req.body.get('content')
    
    # Query parameters
    draft = req.query.get('draft', 'false') == 'true'
    
    # Headers
    auth = req.headers.get('Authorization')
    content_type = req.headers.get('Content-Type')
    
    # Cookies
    session = req.cookies.get('session')
    
    # Uploaded files
    image = req.files.get('image')
    
    # Authenticated user (Django)
    user = req.user
    is_authenticated = req.user.is_authenticated
    
    # HTTP method and path
    method = req.method  # POST
    path = req.path      # /api/posts
    
    # Full Django request
    django_req = req.django
    
    return {"created": True}`}</code>
          </pre>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Response Object</CardTitle>
          <CardDescription>
            Return JSON, set status codes, headers, cookies, and more.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <pre className="bg-background border border-border rounded-lg p-4 overflow-x-auto">
            <code className="text-sm">{`from shanks import App, Response

app = App()

# Simple JSON (auto-converts)
@app.get("api/data")
def get_data(req):
    return {"data": "value"}

# Custom status code
@app.post("api/posts")
def create_post(req):
    return Response().status_code(201).json({
        "created": True
    })

# Set headers
@app.get("api/custom")
def custom(req):
    return (Response()
        .header('X-Custom-Header', 'value')
        .header('X-API-Version', '1.0')
        .json({"ok": True}))

# Set cookies
@app.post("api/login")
def login(req):
    return (Response()
        .cookie('token', 'abc123', max_age=3600)
        .cookie('refresh', 'xyz789', max_age=86400)
        .json({"logged_in": True}))

# Redirect
@app.get("old-url")
def old_url(req):
    return Response().redirect('/new-url')

# File download
@app.get("api/download")
def download(req):
    return Response().file('/path/to/file.pdf', 'document.pdf')`}</code>
          </pre>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Complete CRUD Example</CardTitle>
          <CardDescription>
            Full REST API with all CRUD operations.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <pre className="bg-background border border-border rounded-lg p-4 overflow-x-auto">
            <code className="text-sm">{`from shanks import App, Response, Model, CharField, TextField

# Model
class Post(Model):
    title = CharField(max_length=200)
    content = TextField()

# Routes
app = App()

# List all
@app.get("api/posts")
def list_posts(req):
    page = int(req.query.get('page', 1))
    limit = int(req.query.get('limit', 10))
    
    posts = Post.find_many()
    return {
        "posts": [{"id": p.id, "title": p.title} for p in posts],
        "page": page,
        "limit": limit
    }

# Get by ID
@app.get("api/posts/<int:id>")
def get_post(req, id):
    post = Post.find_unique(id=id)
    if not post:
        return Response().status_code(404).json({
            "error": "Post not found"
        })
    return {
        "id": post.id,
        "title": post.title,
        "content": post.content
    }

# Create
@app.post("api/posts")
def create_post(req):
    post = Post.create(
        title=req.body.get('title'),
        content=req.body.get('content')
    )
    return Response().status_code(201).json({
        "id": post.id
    })

# Update
@app.put("api/posts/<int:id>")
def update_post(req, id):
    post = Post.find_unique(id=id)
    if not post:
        return Response().status_code(404).json({
            "error": "Not found"
        })
    
    post.update_self(
        title=req.body.get('title'),
        content=req.body.get('content')
    )
    return {"updated": True}

# Delete
@app.delete("api/posts/<int:id>")
def delete_post(req, id):
    post = Post.find_unique(id=id)
    if not post:
        return Response().status_code(404).json({
            "error": "Not found"
        })
    
    post.delete_self()
    return {"deleted": True}

urlpatterns = app.get_urls()`}</code>
          </pre>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>No urls.py Needed!</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <p className="text-muted-foreground">
              In settings.py, just point to your routes:
            </p>
            <pre className="bg-background border border-border rounded-lg p-3 overflow-x-auto">
              <code className="text-sm">{`ROOT_URLCONF = "internal.routes"`}</code>
            </pre>
            <p className="text-muted-foreground">
              That's it! No need to create urls.py files. Your routes export urlpatterns directly.
            </p>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
