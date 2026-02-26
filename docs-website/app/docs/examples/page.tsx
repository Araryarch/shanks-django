import { DocPage, CodeBlock } from '@/components/DocPage';
import Link from 'next/link';

export default function ExamplesPage() {
  return (
    <DocPage title="Examples" description="Full working example projects built with Shanks Django.">

      <p>
        These examples show how to build real-world APIs with Shanks. Each covers a complete
        use-case from models to routes to auth.
      </p>

      <div className="not-prose grid gap-4 sm:grid-cols-3 my-8">
        {[
          { href: '/docs/examples/blog', title: 'Blog API', desc: 'CRUD posts, comments, JWT auth, pagination' },
          { href: '/docs/examples/ecommerce', title: 'E-commerce API', desc: 'Products, orders, carts, payments' },
          { href: '/docs/examples/chat', title: 'Real-time Chat', desc: 'WebSockets with channels, rooms, users' },
        ].map(l => (
          <Link key={l.href} href={l.href} className="block rounded-xl border border-white/10 bg-white/3 hover:bg-white/6 p-5 transition-all hover:-translate-y-0.5">
            <p className="font-bold text-white/90 mb-1">{l.title}</p>
            <p className="text-sm text-white/40">{l.desc}</p>
          </Link>
        ))}
      </div>

      <h2>Quick Start Any Example</h2>
      <CodeBlock
        language="bash"
        code={`# Generate a blog API in one command
shanks new blog-api
cd blog-api
shanks create posts --crud
shanks create auth --simple
sorm db push
shanks run`}
      />
    </DocPage>
  );
}
