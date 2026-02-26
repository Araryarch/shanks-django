import { DocPage, CodeBlock, Callout } from '@/components/DocPage';
import Link from 'next/link';

export default function DeploymentPage() {
  return (
    <DocPage title="Deployment" description="Deploy your Shanks API to production using Docker, Heroku, Railway, or any Django-compatible host.">

      <h2>Step 1 — Generate Django Structure</h2>
      <p>Convert your Shanks project to a standard Django layout before deploying:</p>
      <CodeBlock language="bash" code={`shanks generate django`} />
      <p>This creates a <code>django_output/</code> folder with a production-ready Django project.</p>

      <h2>Step 2 — Environment Variables</h2>
      <CodeBlock
        language="bash"
        code={`DEBUG=False
SECRET_KEY=your-production-secret-key
DATABASE_URL=postgresql://user:pass@host:5432/db
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com`}
      />

      <Callout type="info">
        Always set <code>DEBUG=False</code> and use a strong <code>SECRET_KEY</code> in production.
      </Callout>

      <h2>Deployment Platforms</h2>
      <div className="not-prose grid gap-3 sm:grid-cols-2 my-6">
        {[
          { href: '/docs/deployment/heroku', title: 'Heroku', desc: 'One-click git push deploy' },
          { href: '/docs/deployment/railway', title: 'Railway', desc: 'Modern cloud platform' },
          { href: '/docs/deployment/docker', title: 'Docker', desc: 'Container-based deploy' },
          { href: '/docs/deployment/generate', title: 'Generate Django', desc: 'Convert for any host' },
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
