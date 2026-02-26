import { DocPage, CodeBlock, Callout } from '@/components/DocPage';
import Link from 'next/link';

export default function MiddlewarePage() {
  return (
    <DocPage title="Middleware" description="Intercept requests and responses with the familiar req, res, next pattern.">

      <h2>Middleware Pattern</h2>
      <p>
        Shanks middleware follows the Express.js pattern: a function that receives <code>req</code>, <code>res</code>,
        and <code>next</code>. Call <code>next()</code> to pass to the next handler.
      </p>

      <CodeBlock
        code={`def my_middleware(req, res, next):
    # Do something before the handler
    print(f"Request: {req.method} {req.path}")
    next()
    # Do something after the handler (optional)`}
      />

      <h2>Applying Middleware</h2>
      <CodeBlock
        code={`from shanks import App

app = App()

# Global middleware (applies to all routes)
app.use(my_middleware)

# Route-group middleware
protected = app.group('api/v1/admin', auth_middleware)

# Per-route middleware (pass as second arg)
@app.get('api/data', rate_limit_middleware)
def get_data(req):
    return {'data': []}`}
      />

      <h2>Sub-pages</h2>
      <div className="not-prose grid gap-3 sm:grid-cols-3 my-6">
        {[
          { href: '/docs/middleware/builtin', title: 'Built-in', desc: 'auto_cache, logging' },
          { href: '/docs/middleware/custom', title: 'Custom', desc: 'Write your own' },
          { href: '/docs/middleware/cors', title: 'CORS', desc: 'Cross-origin setup' },
        ].map(l => (
          <Link key={l.href} href={l.href} className="block rounded-xl border border-white/10 bg-white/3 hover:bg-white/6 p-4 transition-all hover:-translate-y-0.5">
            <p className="font-semibold text-white/90">{l.title}</p>
            <p className="text-sm text-white/40">{l.desc}</p>
          </Link>
        ))}
      </div>
    </DocPage>
  );
}
