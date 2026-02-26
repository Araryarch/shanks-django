import { DocPage, CodeBlock, Callout } from '@/components/DocPage';

export default function SormMigrationsPage() {
  return (
    <DocPage title="Migrations" description="Create and apply database migrations with Prisma-like SORM commands.">

      <h2>Workflow</h2>
      <CodeBlock
        language="bash"
        code={`# Step 1: Generate migration file
sorm make

# Step 2: Review the generated file in entity/migrations/

# Step 3: Apply migrations
sorm db migrate

# Shortcut: make + migrate in one command
sorm db push`}
      />

      <h2>Reset Database</h2>
      <CodeBlock
        language="bash"
        code={`# ⚠️ Deletes ALL data and re-applies from scratch
sorm db reset`}
      />

      <Callout type="info">
        <code>sorm db reset</code> is only for development. Never run it in production.
      </Callout>

      <h2>Open Database Shell</h2>
      <CodeBlock
        language="bash"
        code={`sorm db shell

# Interactive Django shell with models pre-loaded
> from entity.post import Post
> Post.find_many()`}
      />

      <h2>Migration Files</h2>
      <p>SORM generates standard Django migration files in <code>entity/migrations/</code>. You can inspect and edit
      them like any Django project.</p>
    </DocPage>
  );
}
