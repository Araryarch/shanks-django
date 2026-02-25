import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';

export default function MiddlewarePage() {
  return (
    <div className="space-y-12">
      <div className="space-y-4">
        <h1 className="text-4xl font-bold tracking-tight">Middleware</h1>
        <p className="text-xl text-muted-foreground">
          Express.js-style middleware with req, res, next pattern. Chain multiple middleware for clean request processing.
        </p>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Basic Middleware</CardTitle>
          <CardDescription>
            Middleware signature: def middleware(req, res, next)
          </CardDescription>
        </CardHeader>
        <CardContent>
          <pre className="bg-background border border-border rounded-lg p-4 overflow-x-auto">
            <code className="text-sm">{`from shanks import App, Response

app = App()

# Simple logging middleware
def logger(req, res, next):
    print(f"{req.method} {req.path}")
    next()  # Continue to next middleware

app.use(logger)

@app.get("api/hello")
def hello(req):
    return {"message": "Hello!"}`}</code>
          </pre>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Authentication Middleware</CardTitle>
          <CardDescription>
            Stop the chain by returning a Response, or call next() to continue.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <pre className="bg-background border border-border rounded-lg p-4 overflow-x-auto">
            <code className="text-sm">{`def auth_middleware(req, res, next):
    token = req.headers.get('Authorization')
    
    if not token:
        # Stop chain, return error
        return Response().status_code(401).json({
            'error': 'Unauthorized'
        })
    
    # Verify token and attach user
    user = verify_token(token)
    if not user:
        return Response().status_code(401).json({
            'error': 'Invalid token'
        })
    
    req.user = user
    next()  # Continue to route

app.use(auth_middleware)

@app.get("api/protected")
def protected(req):
    return {"user": req.user.username}`}</code>
          </pre>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Modify Response</CardTitle>
          <CardDescription>
            Add headers, cookies, or modify the response object.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <pre className="bg-background border border-border rounded-lg p-4 overflow-x-auto">
            <code className="text-sm">{`def add_headers(req, res, next):
    res.header('X-API-Version', '1.0.0')
    res.header('X-Request-ID', generate_id())
    next()

def add_cors(req, res, next):
    res.header('Access-Control-Allow-Origin', '*')
    res.header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE')
    next()

app.use(add_headers)
app.use(add_cors)`}</code>
          </pre>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Multiple Middleware</CardTitle>
          <CardDescription>
            Chain multiple middleware in order. Each calls next() to continue.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <pre className="bg-background border border-border rounded-lg p-4 overflow-x-auto">
            <code className="text-sm">{`from shanks import App, auto_cache, swagger

app = App()

# Middleware chain
app.use(logger)              # 1. Log request
app.use(auth_middleware)     # 2. Check auth
app.use(rate_limiter)        # 3. Rate limiting
app.use(auto_cache)          # 4. Auto-caching
app.use(swagger())           # 5. Swagger docs

@app.get("api/data")
def get_data(req):
    # All middleware executed before this
    return {"data": "value"}`}</code>
          </pre>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Error Handling Middleware</CardTitle>
          <CardDescription>
            Catch errors and return appropriate responses.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <pre className="bg-background border border-border rounded-lg p-4 overflow-x-auto">
            <code className="text-sm">{`def error_handler(req, res, next):
    try:
        next()
    except ValueError as e:
        return Response().status_code(400).json({
            'error': 'Bad Request',
            'message': str(e)
        })
    except PermissionError:
        return Response().status_code(403).json({
            'error': 'Forbidden'
        })
    except Exception as e:
        return Response().status_code(500).json({
            'error': 'Internal Server Error',
            'message': str(e)
        })

app.use(error_handler)`}</code>
          </pre>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Request Timing Middleware</CardTitle>
          <CardDescription>
            Measure request processing time.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <pre className="bg-background border border-border rounded-lg p-4 overflow-x-auto">
            <code className="text-sm">{`import time

def timing_middleware(req, res, next):
    start = time.time()
    next()
    duration = time.time() - start
    res.header('X-Response-Time', f'{duration:.3f}s')

app.use(timing_middleware)`}</code>
          </pre>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Built-in Middleware</CardTitle>
          <CardDescription>
            Shanks provides ready-to-use middleware for common tasks.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <div>
              <h3 className="text-lg font-semibold mb-2">auto_cache</h3>
              <p className="text-sm text-muted-foreground mb-2">Automatically cache GET requests</p>
              <pre className="bg-background border border-border rounded-lg p-3 overflow-x-auto">
                <code className="text-sm">{`from shanks import auto_cache
app.use(auto_cache)`}</code>
              </pre>
            </div>

            <div>
              <h3 className="text-lg font-semibold mb-2">smart_cache_invalidation</h3>
              <p className="text-sm text-muted-foreground mb-2">Auto-invalidate cache on POST/PUT/DELETE</p>
              <pre className="bg-background border border-border rounded-lg p-3 overflow-x-auto">
                <code className="text-sm">{`from shanks import smart_cache_invalidation
app.use(smart_cache_invalidation)`}</code>
              </pre>
            </div>

            <div>
              <h3 className="text-lg font-semibold mb-2">swagger()</h3>
              <p className="text-sm text-muted-foreground mb-2">Auto-generate API documentation</p>
              <pre className="bg-background border border-border rounded-lg p-3 overflow-x-auto">
                <code className="text-sm">{`from shanks import swagger
app.use(swagger(title="My API"))`}</code>
              </pre>
            </div>
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Complete Example</CardTitle>
        </CardHeader>
        <CardContent>
          <pre className="bg-background border border-border rounded-lg p-4 overflow-x-auto">
            <code className="text-sm">{`from shanks import App, Response, auto_cache, swagger
import time

app = App()

# Logger
def logger(req, res, next):
    print(f"[{time.strftime('%H:%M:%S')}] {req.method} {req.path}")
    next()

# Auth
def auth(req, res, next):
    token = req.headers.get('Authorization')
    if not token:
        return Response().status_code(401).json({'error': 'Unauthorized'})
    req.user = verify_token(token)
    next()

# Timing
def timing(req, res, next):
    start = time.time()
    next()
    duration = time.time() - start
    res.header('X-Response-Time', f'{duration:.3f}s')

# Apply middleware
app.use(logger)
app.use(auth)
app.use(timing)
app.use(auto_cache)
app.use(swagger(title="Protected API"))

@app.get("api/data")
def get_data(req):
    return {"user": req.user.username, "data": "value"}

# urlpatterns auto-generated! ✨`}</code>
          </pre>
        </CardContent>
      </Card>
    </div>
  );
}
