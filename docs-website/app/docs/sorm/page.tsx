import { DocPage, CodeBlock, Callout } from '@/components/DocPage';
import Link from 'next/link';

export default function SormPage() {
  return (
    <DocPage title="SORM / Database" description="Prisma-style CLI for Django migrations. Create, push, and manage your database schema.">

      <h2>SORM CLI Commands</h2>
      <CodeBlock
        language="bash"
        code={`sorm make            # Create migration files
sorm db migrate      # Apply pending migrations
sorm db push         # make + migrate in one step
sorm db reset        # Flush all data (careful!)
sorm db shell        # Open Django database shell
sorm studio          # Open Django Admin panel`}
      />

      <Callout type="info" title="Prisma Equivalent">
        <code>sorm make</code> = <code>prisma migrate dev --create-only</code>
        <br />
        <code>sorm db push</code> = <code>prisma db push</code>
        <br />
        <code>sorm studio</code> = <code>prisma studio</code> (uses Django Admin)
      </Callout>

      <h2>Typical Workflow</h2>
      <CodeBlock
        language="bash"
        code={`# 1. Define or update your model in entity/
# 2. Create the migration
sorm make

# 3. Apply it
sorm db migrate

# Or combine both:
sorm db push`}
      />

      <h2>Sub-pages</h2>
      <div className="not-prose grid gap-3 sm:grid-cols-3 my-6">
        {[
          { href: '/docs/sorm/database', title: 'Database Setup', desc: 'Connect your DB' },
          { href: '/docs/sorm/migrations', title: 'Migrations', desc: 'sorm make & migrate' },
          { href: '/docs/sorm/admin', title: 'Admin Panel', desc: 'sorm studio' },
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
