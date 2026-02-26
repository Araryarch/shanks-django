import { DocPage, CodeBlock, Callout } from '@/components/DocPage';

export default function SormDatabasePage() {
  return (
    <DocPage title="Database Setup" description="Configure your database connection in .env and let SORM handle the rest.">

      <h2>Default: SQLite</h2>
      <p>New projects use SQLite out of the box — no configuration needed.</p>
      <CodeBlock
        language="bash"
        filename=".env"
        code={`DATABASE_URL=sqlite:///db.sqlite3`}
      />

      <h2>PostgreSQL</h2>
      <CodeBlock
        language="bash"
        filename=".env"
        code={`DATABASE_URL=postgresql://user:password@localhost:5432/mydb`}
      />
      <CodeBlock
        language="bash"
        code={`# Install adapter
pip install psycopg2-binary`}
      />

      <h2>MySQL</h2>
      <CodeBlock
        language="bash"
        filename=".env"
        code={`DATABASE_URL=mysql://user:password@localhost:3306/mydb`}
      />
      <CodeBlock
        language="bash"
        code={`pip install mysqlclient`}
      />

      <h2>Apply Schema</h2>
      <CodeBlock
        language="bash"
        code={`# After configuring, push your schema
sorm db push`}
      />

      <Callout type="info">
        Shanks reads <code>DATABASE_URL</code> and configures Django's <code>DATABASES</code> setting automatically.
      </Callout>
    </DocPage>
  );
}
