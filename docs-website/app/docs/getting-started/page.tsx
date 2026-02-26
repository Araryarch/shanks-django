import { CodeBlock } from '@/components/CodeBlock';
import { Callout } from '@/components/Callout';
import Link from 'next/link';

export default function GettingStartedPage() {
  return (
    <div className="prose prose-gray dark:prose-invert max-w-none">
      <h1>Getting Started</h1>
      <p className="lead">
        Learn how to create your first Shanks application in minutes.
      </p>

      <h2>Prerequisites</h2>
      <ul>
        <li>Python 3.8 or higher</li>
        <li>pip (Python package manager)</li>
        <li>Basic knowledge of Python and Django</li>
      </ul>

      <h2>Installation</h2>
      <p>Install Shanks using pip:</p>
      <CodeBlock code="pip install shanks-django" language="bash" />

      <Callout type="success" title="Installation Complete">
        You now have access to <code>shanks</code> and <code>sorm</code> commands!
      </Callout>

      <h2>Create Your First Project</h2>
      <p>Create a new Shanks project:</p>
      <CodeBlock code="shanks new myproject" language="bash" />

      <p>This creates a project with the following structure:</p>
      <CodeBlock
        code={`myproject/
├── internal/
│   ├── controller/      # HTTP handlers
│   ├── routes/          # Route definitions
│   ├── service/         # Business logic
│   └── middleware/      # Middleware
├── entity/              # Database models
├── dto/                 # Data Transfer Objects
├── config/              # Configuration
├── utils/               # Utilities
├── myproject/           # Django settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── manage.py`}
        language="text"
      />

      <h2>Setup Database</h2>
      <p>Navigate to your project and setup the database:</p>
      <CodeBlock
        code={`cd myproject
sorm db push`}
        language="bash"
      />

      <h2>Start the Server</h2>
      <p>Start the development server:</p>
      <CodeBlock code="shanks run" language="bash" />

      <p>Visit <code>http://127.0.0.1:8000/api/health</code> to see your API running!</p>

      <Callout type="info">
        The default health endpoint returns: <code>{`{"status": "ok", "service": "myproject"}`}</code>
      </Callout>

      <h2>Create Your First Endpoint</h2>
      <p>Let's create a simple blog API with CRUD operations:</p>

      <h3>1. Generate CRUD Endpoints</h3>
      <CodeBlock code="shanks create posts --crud" language="bash" />

      <p>This generates three files:</p>
      <ul>
        <li><code>entity/posts.py</code> - Database model</li>
        <li><code>internal/controller/posts.py</code> - Business logic</li>
        <li><code>internal/routes/posts.py</code> - API routes</li>
      </ul>

      <h3>2. Register Routes</h3>
      <p>Add the routes to <code>internal/routes/__init__.py</code>:</p>
      <CodeBlock
        code={`from shanks import App
from . import posts

app = App()

@app.get("api/health")
def health(req):
    return {"status": "ok", "service": "myproject"}

# Add this line
app.include(posts.router)

urlpatterns = app.get_urls()`}
        filename="internal/routes/__init__.py"
      />

      <h3>3. Update Database</h3>
      <CodeBlock code="sorm db push" language="bash" />

      <h3>4. Test Your API</h3>
      <p>Your API now has these endpoints:</p>
      <CodeBlock
        code={`GET    /api/posts          # List all posts
GET    /api/posts/<id>     # Get single post
POST   /api/posts          # Create post
PUT    /api/posts/<id>     # Update post
DELETE /api/posts/<id>     # Delete post`}
        language="text"
      />

      <p>Test with curl or PowerShell:</p>
      <CodeBlock
        code={`# Create a post
curl -X POST http://127.0.0.1:8000/api/posts \\
  -H "Content-Type: application/json" \\
  -d '{"title":"My First Post","description":"Hello Shanks!"}'

# Get all posts
curl http://127.0.0.1:8000/api/posts`}
        language="bash"
      />

      <h2>Add Authentication</h2>
      <p>Generate JWT authentication:</p>
      <CodeBlock code="shanks create auth --simple" language="bash" />

      <p>Register auth routes:</p>
      <CodeBlock
        code={`from shanks import App
from . import posts, auth

app = App()

@app.get("api/health")
def health(req):
    return {"status": "ok", "service": "myproject"}

app.include(posts.router)
app.include(auth.router)  # Add this

urlpatterns = app.get_urls()`}
        filename="internal/routes/__init__.py"
      />

      <p>Now you have authentication endpoints:</p>
      <CodeBlock
        code={`POST /api/auth/register    # Register user
POST /api/auth/login       # Login (get JWT token)
GET  /api/auth/me          # Get current user
POST /api/auth/refresh     # Refresh token
POST /api/auth/logout      # Logout`}
        language="text"
      />

      <h2>Project Structure Explained</h2>

      <h3>internal/</h3>
      <p>Contains your application code:</p>
      <ul>
        <li><strong>controller/</strong> - HTTP request handlers and business logic</li>
        <li><strong>routes/</strong> - API route definitions</li>
        <li><strong>service/</strong> - Reusable business logic</li>
        <li><strong>middleware/</strong> - Custom middleware</li>
      </ul>

      <h3>entity/</h3>
      <p>Database models (Django ORM):</p>
      <CodeBlock
        code={`from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        app_label = "entity"`}
        filename="entity/posts.py"
      />

      <h3>dto/</h3>
      <p>Data Transfer Objects for validation and serialization.</p>

      <h3>config/</h3>
      <p>Application configuration and environment variables.</p>

      <h2>Next Steps</h2>
      <div className="not-prose grid gap-4 sm:grid-cols-2">
        <Link
          href="/docs/routing"
          className="block rounded-lg border border-gray-200 p-4 transition-colors hover:border-blue-500 dark:border-gray-800"
        >
          <h3 className="mb-2 font-semibold text-gray-900 dark:text-white">
            Routing
          </h3>
          <p className="text-sm text-gray-600 dark:text-gray-400">
            Learn about routes, groups, and dynamic parameters
          </p>
        </Link>

        <Link
          href="/docs/authentication"
          className="block rounded-lg border border-gray-200 p-4 transition-colors hover:border-blue-500 dark:border-gray-800"
        >
          <h3 className="mb-2 font-semibold text-gray-900 dark:text-white">
            Authentication
          </h3>
          <p className="text-sm text-gray-600 dark:text-gray-400">
            Implement JWT and session authentication
          </p>
        </Link>

        <Link
          href="/docs/middleware"
          className="block rounded-lg border border-gray-200 p-4 transition-colors hover:border-blue-500 dark:border-gray-800"
        >
          <h3 className="mb-2 font-semibold text-gray-900 dark:text-white">
            Middleware
          </h3>
          <p className="text-sm text-gray-600 dark:text-gray-400">
            Add custom middleware and CORS support
          </p>
        </Link>

        <Link
          href="/docs/deployment"
          className="block rounded-lg border border-gray-200 p-4 transition-colors hover:border-blue-500 dark:border-gray-800"
        >
          <h3 className="mb-2 font-semibold text-gray-900 dark:text-white">
            Deployment
          </h3>
          <p className="text-sm text-gray-600 dark:text-gray-400">
            Deploy to Heroku, Railway, Docker, and more
          </p>
        </Link>
      </div>
    </div>
  );
}
