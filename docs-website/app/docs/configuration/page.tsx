import { DocPage, CodeBlock, Callout } from '@/components/DocPage';
import Link from 'next/link';

export default function ConfigurationPage() {
  return (
    <DocPage title="Configuration" description="All Shanks configuration lives in .env — simple environment variables, zero magic.">

      <h2>The .env File</h2>
      <CodeBlock
        language="bash"
        filename=".env"
        code={`# Application
DEBUG=True
SECRET_KEY=your-django-secret-key

# Database
DATABASE_URL=sqlite:///db.sqlite3

# JWT
JWT_SECRET_KEY=your-jwt-secret
JWT_EXPIRY_HOURS=24

# CORS
ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ORIGINS=http://localhost:3000`}
      />

      <Callout type="info">
        Never commit <code>.env</code> to version control. Add it to <code>.gitignore</code>.
      </Callout>

      <h2>Sub-pages</h2>
      <div className="not-prose grid gap-3 sm:grid-cols-3 my-6">
        {[
          { href: '/docs/configuration/env', title: 'Environment', desc: 'All env variables' },
          { href: '/docs/configuration/database', title: 'Database', desc: 'DB connection' },
          { href: '/docs/configuration/settings', title: 'Settings', desc: 'Django settings' },
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
