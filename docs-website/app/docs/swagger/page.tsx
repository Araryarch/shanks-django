import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';

export default function SwaggerPage() {
  return (
    <div className="space-y-12">
      <div className="space-y-4">
        <h1 className="text-4xl font-bold tracking-tight">Swagger / OpenAPI</h1>
        <p className="text-xl text-muted-foreground">
          Auto-generated API documentation with Swagger UI. Zero configuration needed.
        </p>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Quick Start (Middleware Style)</CardTitle>
          <CardDescription>
            Enable Swagger with one line - all endpoints automatically documented!
          </CardDescription>
        </CardHeader>
        <CardContent>
          <pre className="bg-background border border-border rounded-lg p-4 overflow-x-auto">
            <code className="text-sm">{`from shanks import App, swagger

app = App()

# Enable Swagger - that's it!
app.use(swagger(
    title="My API",
    version="1.0.0",
    description="Complete API documentation"
))

# All routes automatically documented
@app.get("api/users")
def get_users(req):
    return {"users": []}

@app.post("api/users")
def create_user(req):
    return {"created": True}

urlpatterns = app.get_urls()

# Visit: http://localhost:8000/docs`}</code>
          </pre>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Configuration Options</CardTitle>
          <CardDescription>
            Customize your API documentation.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <pre className="bg-background border border-border rounded-lg p-4 overflow-x-auto">
            <code className="text-sm">{`app.use(swagger(
    title="My API",
    version="1.0.0",
    description="Complete API documentation",
    terms_of_service="https://example.com/terms",
    contact={
        "name": "API Support",
        "email": "support@example.com",
        "url": "https://example.com/support"
    },
    license={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT"
    }
))`}</code>
          </pre>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Legacy Style (Still Supported)</CardTitle>
          <CardDescription>
            Use SwaggerUI class for more control.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <pre className="bg-background border border-border rounded-lg p-4 overflow-x-auto">
            <code className="text-sm">{`from shanks import App, SwaggerUI

app = App()

# Enable Swagger UI at /docs
SwaggerUI.enable(app,
    title="My API",
    version="1.0.0",
    description="Complete API documentation"
)

@app.get("api/users")
def get_users(req):
    return {"users": []}`}</code>
          </pre>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Document Routes (Optional)</CardTitle>
          <CardDescription>
            Add detailed documentation to specific endpoints.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <pre className="bg-background border border-border rounded-lg p-4 overflow-x-auto">
            <code className="text-sm">{`from shanks import App, SwaggerUI, Response

app = App()
SwaggerUI.enable(app, title="My API")

@app.get("api/users/<int:user_id>")
@SwaggerUI.doc(
    summary="Get user by ID",
    description="Returns a single user with all details",
    tags=["Users"],
    parameters=[{
        "name": "user_id",
        "in": "path",
        "required": True,
        "schema": {"type": "integer"},
        "description": "User ID"
    }],
    responses={
        200: {
            "description": "Success",
            "content": {
                "application/json": {
                    "schema": {
                        "type": "object",
                        "properties": {
                            "id": {"type": "integer"},
                            "username": {"type": "string"},
                            "email": {"type": "string"}
                        }
                    }
                }
            }
        },
        404: {"description": "User not found"}
    }
)
def get_user(req, user_id):
    user = User.find_unique(id=user_id)
    if not user:
        return Response().status_code(404).json({
            'error': 'Not found'
        })
    return {
        'id': user.id,
        'username': user.username,
        'email': user.email
    }`}</code>
          </pre>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Document POST with Request Body</CardTitle>
          <CardDescription>
            Define request body schema for POST/PUT endpoints.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <pre className="bg-background border border-border rounded-lg p-4 overflow-x-auto">
            <code className="text-sm">{`@app.post("api/users")
@SwaggerUI.doc(
    summary="Create user",
    tags=["Users"],
    request_body={
        "required": True,
        "content": {
            "application/json": {
                "schema": {
                    "type": "object",
                    "required": ["username", "email", "password"],
                    "properties": {
                        "username": {
                            "type": "string",
                            "minLength": 3,
                            "maxLength": 50
                        },
                        "email": {
                            "type": "string",
                            "format": "email"
                        },
                        "password": {
                            "type": "string",
                            "minLength": 8
                        }
                    }
                }
            }
        }
    },
    responses={
        201: {
            "description": "User created",
            "content": {
                "application/json": {
                    "schema": {
                        "type": "object",
                        "properties": {
                            "id": {"type": "integer"},
                            "username": {"type": "string"}
                        }
                    }
                }
            }
        },
        400: {"description": "Invalid input"}
    }
)
def create_user(req):
    user = User.create(
        username=req.body.get('username'),
        email=req.body.get('email'),
        password=req.body.get('password')
    )
    return Response().status_code(201).json({
        'id': user.id,
        'username': user.username
    })`}</code>
          </pre>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Authentication in Swagger</CardTitle>
          <CardDescription>
            Add authentication schemes to your API docs.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <pre className="bg-background border border-border rounded-lg p-4 overflow-x-auto">
            <code className="text-sm">{`SwaggerUI.enable(app,
    title="My API",
    security_schemes={
        "bearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }
)

@app.get("api/profile")
@SwaggerUI.doc(
    summary="Get user profile",
    security=[{"bearerAuth": []}],
    responses={
        200: {"description": "Success"},
        401: {"description": "Unauthorized"}
    }
)
def get_profile(req):
    return {
        'id': req.user.id,
        'username': req.user.username
    }`}</code>
          </pre>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Tags and Grouping</CardTitle>
          <CardDescription>
            Organize endpoints with tags.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <pre className="bg-background border border-border rounded-lg p-4 overflow-x-auto">
            <code className="text-sm">{`# User endpoints
@app.get("api/users")
@SwaggerUI.doc(summary="List users", tags=["Users"])
def list_users(req):
    return {"users": []}

@app.post("api/users")
@SwaggerUI.doc(summary="Create user", tags=["Users"])
def create_user(req):
    return {"created": True}

# Post endpoints
@app.get("api/posts")
@SwaggerUI.doc(summary="List posts", tags=["Posts"])
def list_posts(req):
    return {"posts": []}

@app.post("api/posts")
@SwaggerUI.doc(summary="Create post", tags=["Posts"])
def create_post(req):
    return {"created": True}`}</code>
          </pre>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Complete Example</CardTitle>
          <CardDescription>
            Full API with Swagger documentation.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <pre className="bg-background border border-border rounded-lg p-4 overflow-x-auto">
            <code className="text-sm">{`from shanks import App, swagger, Response, User

app = App()

# Enable Swagger
app.use(swagger(
    title="Blog API",
    version="1.0.0",
    description="Complete blog API with authentication"
))

# Auth endpoints
@app.post("api/auth/login")
def login(req):
    """Login with username and password"""
    user = authenticate(
        username=req.body.get('username'),
        password=req.body.get('password')
    )
    if not user:
        return Response().status_code(401).json({
            'error': 'Invalid credentials'
        })
    return {'token': create_token(user)}

@app.post("api/auth/register")
def register(req):
    """Register new user"""
    user = User.create(
        username=req.body.get('username'),
        email=req.body.get('email'),
        password=req.body.get('password')
    )
    return Response().status_code(201).json({
        'id': user.id,
        'username': user.username
    })

# Post endpoints
@app.get("api/posts")
def list_posts(req):
    """List all posts with pagination"""
    page = int(req.query.get('page', 1))
    limit = int(req.query.get('limit', 10))
    posts = Post.find_many()
    return {'posts': [...], 'page': page, 'limit': limit}

@app.get("api/posts/<int:post_id>")
def get_post(req, post_id):
    """Get single post by ID"""
    post = Post.find_unique(id=post_id)
    if not post:
        return Response().status_code(404).json({
            'error': 'Post not found'
        })
    return {'post': {...}}

@app.post("api/posts")
def create_post(req):
    """Create new post (requires auth)"""
    post = Post.create(
        title=req.body.get('title'),
        content=req.body.get('content'),
        author=req.user
    )
    return Response().status_code(201).json({'id': post.id})

urlpatterns = app.get_urls()

# Visit: http://localhost:8000/docs`}</code>
          </pre>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Swagger UI Features</CardTitle>
        </CardHeader>
        <CardContent>
          <ul className="space-y-3">
            <li className="flex items-start gap-3">
              <span className="text-xl">📚</span>
              <span className="text-muted-foreground">Interactive API documentation</span>
            </li>
            <li className="flex items-start gap-3">
              <span className="text-xl">🧪</span>
              <span className="text-muted-foreground">Test endpoints directly from browser</span>
            </li>
            <li className="flex items-start gap-3">
              <span className="text-xl">🔐</span>
              <span className="text-muted-foreground">Authentication support (Bearer, API Key, etc)</span>
            </li>
            <li className="flex items-start gap-3">
              <span className="text-xl">📋</span>
              <span className="text-muted-foreground">Request/response examples</span>
            </li>
            <li className="flex items-start gap-3">
              <span className="text-xl">🏷️</span>
              <span className="text-muted-foreground">Organize with tags and groups</span>
            </li>
            <li className="flex items-start gap-3">
              <span className="text-xl">📥</span>
              <span className="text-muted-foreground">Download OpenAPI spec (JSON/YAML)</span>
            </li>
          </ul>
        </CardContent>
      </Card>
    </div>
  );
}
