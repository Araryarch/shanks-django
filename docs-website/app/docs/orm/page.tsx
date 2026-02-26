import { DocPage, CodeBlock, Callout } from '@/components/DocPage';
import Link from 'next/link';

export default function OrmPage() {
  return (
    <DocPage title="ORM Queries" description="Prisma-like query syntax on top of Django ORM — readable, powerful, typed.">

      <h2>Core Methods</h2>
      <CodeBlock
        code={`from entity.post import Post

# Find many records
posts = Post.find_many()

# With filters
posts = Post.find_many(author_id=1, published=True)

# Find a single record (returns None if not found)
post = Post.find_unique(id=42)

# Create
post = Post.create(title='Hello', content='World', author_id=1)

# Update
post.update_self(title='Updated title')

# Delete
post.delete_self()`}
      />

      <h2>Pagination</h2>
      <CodeBlock
        code={`@app.get('api/posts')
def list_posts(req):
    page  = int(req.query.get('page', 1))
    limit = int(req.query.get('limit', 10))

    posts = Post.find_many()
    start = (page - 1) * limit
    paginated = posts[start:start + limit]

    return {'posts': paginated, 'page': page, 'total': len(posts)}`}
      />

      <Callout type="info">
        The ORM wraps Django's queryset API. All standard Django ORM features are still accessible
        via <code>Post.objects</code> when you need them.
      </Callout>

      <h2>Sub-pages</h2>
      <div className="not-prose grid gap-3 sm:grid-cols-3 my-6">
        {[
          { href: '/docs/orm/models', title: 'Models', desc: 'Define your data' },
          { href: '/docs/orm/queries', title: 'Queries', desc: 'find_many, find_unique' },
          { href: '/docs/orm/relationships', title: 'Relationships', desc: 'Foreign keys & joins' },
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
