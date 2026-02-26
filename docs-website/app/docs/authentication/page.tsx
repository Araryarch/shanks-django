import { DocPage, CodeBlock, Callout } from '@/components/DocPage';
import Link from 'next/link';

export default function AuthPage() {
  return (
    <DocPage title="Authentication" description="JWT and session-based authentication generated in seconds with shanks create auth.">

      <h2>Quick Setup</h2>
      <CodeBlock
        language="bash"
        code={`# Simple auth (login, register, /me)
shanks create auth --simple

# Complete auth (+ email verification)
shanks create auth --complete`}
      />

      <h2>Generated Endpoints</h2>
      <CodeBlock
        language="text"
        code={`POST /api/auth/register   → Register new user
POST /api/auth/login      → Login, receive JWT token
GET  /api/auth/me         → Get current user (protected)
POST /api/auth/refresh    → Refresh JWT token
POST /api/auth/logout     → Blacklist token`}
      />

      <h2>Using the Token</h2>
      <CodeBlock
        language="bash"
        code={`# 1. Register
curl -X POST http://localhost:8000/api/auth/register \\
  -H "Content-Type: application/json" \\
  -d '{"username":"alice","password":"secret123","email":"alice@example.com"}'

# 2. Login → returns token
curl -X POST http://localhost:8000/api/auth/login \\
  -d '{"username":"alice","password":"secret123"}'

# 3. Use token
curl http://localhost:8000/api/auth/me \\
  -H "Authorization: Bearer <token>"`}
      />

      <Callout type="info">
        The JWT secret is automatically set in your <code>.env</code> file. Change it before deploying to production.
      </Callout>

      <h2>Sub-pages</h2>
      <div className="not-prose grid gap-3 sm:grid-cols-3 my-6">
        {[
          { href: '/docs/authentication/jwt', title: 'JWT Auth', desc: 'Token-based auth' },
          { href: '/docs/authentication/session', title: 'Session Auth', desc: 'Cookie sessions' },
          { href: '/docs/authentication/middleware', title: 'Auth Middleware', desc: 'Protect routes' },
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
