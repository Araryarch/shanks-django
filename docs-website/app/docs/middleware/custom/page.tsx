import { DocPage, CodeBlock, Callout } from '@/components/DocPage';

export default function CustomMiddlewarePage() {
  return (
    <DocPage title="Custom Middleware" description="Write middleware that intercepts any request with req, res, next.">

      <h2>Anatomy of Middleware</h2>
      <CodeBlock
        filename="internal/middleware/auth.py"
        code={`from shanks import Response

def auth_middleware(req, res, next):
    token = req.headers.get('Authorization', '').replace('Bearer ', '')

    if not token:
        return Response().status_code(401).json({'error': 'Missing token'})

    user = verify_jwt(token)
    if not user:
        return Response().status_code(401).json({'error': 'Invalid token'})

    req.user = user  # Attach user to request
    next()           # Hand off to route handler`}
      />

      <Callout type="info">
        Return a <code>Response()</code> to short-circuit the handler. Call <code>next()</code> to proceed.
      </Callout>

      <h2>Rate Limiter Example</h2>
      <CodeBlock
        code={`from django.core.cache import cache

def rate_limit(max_requests=100, window=60):
    def middleware(req, res, next):
        ip = req.headers.get('X-Real-IP', '127.0.0.1')
        key = f'rate:{ip}'
        count = cache.get(key, 0)
        if count >= max_requests:
            return Response().status_code(429).json({'error': 'Too many requests'})
        cache.set(key, count + 1, timeout=window)
        next()
    return middleware

app.use(rate_limit(max_requests=60, window=60))`}
      />

      <h2>Request Timing Middleware</h2>
      <CodeBlock
        code={`import time

def timing_middleware(req, res, next):
    start = time.time()
    next()
    elapsed = round((time.time() - start) * 1000, 2)
    print(f"{req.method} {req.path} — {elapsed}ms")`}
      />
    </DocPage>
  );
}
