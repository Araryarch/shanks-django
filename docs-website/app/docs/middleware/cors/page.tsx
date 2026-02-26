import { DocPage, CodeBlock, Callout } from '@/components/DocPage';

export default function CorsMiddlewarePage() {
  return (
    <DocPage title="CORS" description="Enable cross-origin requests for your frontend in a few lines.">

      <h2>Basic CORS Setup</h2>
      <CodeBlock
        filename="internal/middleware/cors.py"
        code={`def cors_middleware(req, res, next):
    res.headers['Access-Control-Allow-Origin'] = '*'
    res.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, PATCH, DELETE, OPTIONS'
    res.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'

    if req.method == 'OPTIONS':
        return Response().status_code(204)

    next()`}
      />

      <h2>Restrict Origins</h2>
      <CodeBlock
        code={`ALLOWED_ORIGINS = [
    'https://myapp.com',
    'http://localhost:3000',
]

def cors_middleware(req, res, next):
    origin = req.headers.get('Origin', '')
    if origin in ALLOWED_ORIGINS:
        res.headers['Access-Control-Allow-Origin'] = origin
    next()`}
      />

      <h2>Apply Globally</h2>
      <CodeBlock
        code={`from shanks import App
from internal.middleware.cors import cors_middleware

app = App()
app.use(cors_middleware)`}
      />

      <Callout type="info">
        For production, always restrict <code>Access-Control-Allow-Origin</code> to your actual frontend domains.
      </Callout>
    </DocPage>
  );
}
