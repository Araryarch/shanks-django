import { DocPage, CodeBlock, Callout } from '@/components/DocPage';

export default function BuiltinMiddlewarePage() {
  return (
    <DocPage title="Built-in Middleware" description="Shanks ships with middleware for caching, logging, and more.">

      <h2>auto_cache</h2>
      <p>Caches all GET responses. Enabled automatically when you call <code>App()</code>.</p>
      <CodeBlock
        code={`from shanks import App, auto_cache

app = App()
app.use(auto_cache)  # Already active by default, but explicit is fine`}
      />

      <h2>request_logger</h2>
      <p>Logs every incoming request to stdout — useful for development.</p>
      <CodeBlock
        code={`from shanks import App
from shanks.middleware import request_logger

app = App()
app.use(request_logger)

# Output example:
# [GET] /api/posts - 200 OK (12ms)`}
      />

      <Callout type="info">
        Built-in middleware can be combined freely. Order matters — middleware runs top-to-bottom.
      </Callout>

      <h2>Combining Middleware</h2>
      <CodeBlock
        code={`from shanks.middleware import request_logger, auto_cache

app.use(request_logger)   # Log first
app.use(auto_cache)       # Then cache`}
      />
    </DocPage>
  );
}
