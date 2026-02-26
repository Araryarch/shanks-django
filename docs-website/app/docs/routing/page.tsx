import { DocPage, CodeBlock, Callout } from '@/components/DocPage';
import Link from 'next/link';

export default function RoutingPage() {
  return (
    <DocPage
      title="Routing"
      description="Express.js-like routing for Django. Simple, clean, and powerful."
    >
      <h2>Overview</h2>
      <p>
        Shanks provides an Express.js-inspired routing system that makes defining API endpoints
        simple and intuitive. No more complex Django urls.py files - just clean decorators.
      </p>

      <Callout type="info" title="Key Features">
        <ul>
          <li>Express.js-like decorator syntax</li>
          <li>Route grouping with prefixes</li>
          <li>Dynamic URL parameters with type detection</li>
          <li>Multiple HTTP methods on same path</li>
          <li>Automatic URL pattern generation</li>
        </ul>
      </Callout>

      <h2>Quick Example</h2>
      <CodeBlock
        code={`from shanks import App

app = App()

@app.get("api/posts")
def list_posts(req):
    return {"posts": []}

@app.get("api/posts/<id>")
def get_post(req, id):
    return {"id": id}

@app.post("api/posts")
def create_post(req):
    data = req.body
    return {"message": "Created"}

# Export for Django
urlpatterns = app.get_urls()`}
        filename="internal/routes/__init__.py"
      />

      <h2>Core Concepts</h2>

      <h3>1. App Instance</h3>
      <p>
        The <code>App</code> class is the main router. Create an instance and use decorators
        to define routes:
      </p>
      <CodeBlock
        code={`from shanks import App

app = App()  # Create router instance`}
      />

      <h3>2. Route Decorators</h3>
      <p>
        Use decorators to define routes for different HTTP methods:
      </p>
      <CodeBlock
        code={`@app.get("path")      # GET requests
@app.post("path")     # POST requests
@app.put("path")      # PUT requests
@app.delete("path")   # DELETE requests
@app.patch("path")    # PATCH requests`}
      />

      <h3>3. Request Object</h3>
      <p>
        All route handlers receive a <code>Request</code> object with useful properties:
      </p>
      <CodeBlock
        code={`def handler(req):
    req.method      # HTTP method (GET, POST, etc.)
    req.path        # Request path
    req.body        # Parsed JSON body (POST/PUT)
    req.query       # Query parameters
    req.headers     # Request headers
    req.user        # Authenticated user
    req.session     # Session data
    req.cookies     # Cookies
    req.files       # Uploaded files`}
      />

      <h3>4. Response Types</h3>
      <p>
        Return different types of responses:
      </p>
      <CodeBlock
        code={`# JSON response (automatic)
@app.get("api/data")
def get_data(req):
    return {"key": "value"}

# Custom response
from shanks import Response

@app.get("api/custom")
def custom(req):
    return Response()\\
        .status_code(201)\\
        .json({"message": "Created"})

# Error response
@app.get("api/error")
def error(req):
    return Response()\\
        .status_code(404)\\
        .json({"error": "Not found"})`}
      />

      <h2>Routing Topics</h2>

      <div className="not-prose grid gap-4 sm:grid-cols-2 my-8">
        <Link
          href="/docs/routing/basic"
          className="block rounded-lg border p-4 transition-colors"
          style={{
            borderColor: 'var(--ctp-surface0)',
            backgroundColor: 'var(--ctp-mantle)'
          }}
        >
          <h3 className="mb-2 font-semibold" style={{ color: 'var(--ctp-text)' }}>
            Basic Routes
          </h3>
          <p className="text-sm" style={{ color: 'var(--ctp-subtext0)' }}>
            Learn how to define basic routes with GET, POST, PUT, DELETE
          </p>
        </Link>

        <Link
          href="/docs/routing/groups"
          className="block rounded-lg border p-4 transition-colors"
          style={{
            borderColor: 'var(--ctp-surface0)',
            backgroundColor: 'var(--ctp-mantle)'
          }}
        >
          <h3 className="mb-2 font-semibold" style={{ color: 'var(--ctp-text)' }}>
            Route Groups
          </h3>
          <p className="text-sm" style={{ color: 'var(--ctp-subtext0)' }}>
            Group routes with common prefixes and middleware
          </p>
        </Link>

        <Link
          href="/docs/routing/dynamic"
          className="block rounded-lg border p-4 transition-colors"
          style={{
            borderColor: 'var(--ctp-surface0)',
            backgroundColor: 'var(--ctp-mantle)'
          }}
        >
          <h3 className="mb-2 font-semibold" style={{ color: 'var(--ctp-text)' }}>
            Dynamic Routes
          </h3>
          <p className="text-sm" style={{ color: 'var(--ctp-subtext0)' }}>
            Handle dynamic URL parameters with automatic type detection
          </p>
        </Link>

        <Link
          href="/docs/routing/methods"
          className="block rounded-lg border p-4 transition-colors"
          style={{
            borderColor: 'var(--ctp-surface0)',
            backgroundColor: 'var(--ctp-mantle)'
          }}
        >
          <h3 className="mb-2 font-semibold" style={{ color: 'var(--ctp-text)' }}>
            HTTP Methods
          </h3>
          <p className="text-sm" style={{ color: 'var(--ctp-subtext0)' }}>
            Handle multiple HTTP methods on the same path
          </p>
        </Link>
      </div>

      <h2>Best Practices</h2>
      <ul>
        <li>Use RESTful naming conventions (e.g., <code>/api/posts</code>, <code>/api/posts/&lt;id&gt;</code>)</li>
        <li>Group related routes together</li>
        <li>Use route groups for common prefixes</li>
        <li>Keep route handlers thin - move logic to services</li>
        <li>Use meaningful parameter names</li>
        <li>Return consistent response formats</li>
      </ul>

      <h2>Next Steps</h2>
      <ul>
        <li><Link href="/docs/routing/basic">Learn about basic routes</Link></li>
        <li><Link href="/docs/routing/groups">Explore route groups</Link></li>
        <li><Link href="/docs/middleware">Add middleware to routes</Link></li>
      </ul>
    </DocPage>
  );
}
