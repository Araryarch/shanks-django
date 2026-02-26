import { DocPage, CodeBlock, Callout } from '@/components/DocPage';

export default function OrmQueriesPage() {
  return (
    <DocPage title="Queries" description="Prisma-like query methods on every Shanks model.">

      <h2>find_many()</h2>
      <CodeBlock
        code={`# All records
posts = Post.find_many()

# With filters (keyword args become WHERE clauses)
posts = Post.find_many(published=True)
posts = Post.find_many(author_id=1, published=True)`}
      />

      <h2>find_unique()</h2>
      <CodeBlock
        code={`# Returns the object or None
post = Post.find_unique(id=42)
if not post:
    return Response().status_code(404).json({'error': 'Not found'})

# Find by any unique field
user = User.find_unique(email='alice@example.com')`}
      />

      <h2>create()</h2>
      <CodeBlock
        code={`post = Post.create(
    title='My Post',
    content='Hello world',
    author_id=req.user.id,
    published=False,
)
return Response().status_code(201).json({'id': post.id})`}
      />

      <h2>update_self() / delete_self()</h2>
      <CodeBlock
        code={`post = Post.find_unique(id=42)

# Partial update (only provided fields are changed)
post.update_self(title='New title', published=True)

# Delete
post.delete_self()`}
      />

      <Callout type="info">
        All methods wrap Django's queryset API. For complex queries use{' '}
        <code>Post.objects.filter(...).annotate(...)</code> directly.
      </Callout>
    </DocPage>
  );
}
