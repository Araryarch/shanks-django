import { DocPage, CodeBlock } from '@/components/DocPage';

export default function ConfigDatabasePage() {
  return (
    <DocPage title="Database Configuration" description="Configure your database connection via DATABASE_URL.">

      <h2>Supported Databases</h2>

      <h3>SQLite (default)</h3>
      <CodeBlock language="bash" code={`DATABASE_URL=sqlite:///db.sqlite3`} />

      <h3>PostgreSQL</h3>
      <CodeBlock
        language="bash"
        code={`DATABASE_URL=postgresql://user:password@localhost:5432/mydb

# Install driver:
pip install psycopg2-binary`}
      />

      <h3>MySQL</h3>
      <CodeBlock
        language="bash"
        code={`DATABASE_URL=mysql://user:password@localhost:3306/mydb

# Install driver:
pip install mysqlclient`}
      />

      <h2>Connection Pooling (PostgreSQL)</h2>
      <CodeBlock
        language="bash"
        code={`DATABASE_URL=postgresql://user:pass@localhost:5432/mydb?conn_max_age=60`}
      />

      <h2>Apply Schema</h2>
      <CodeBlock
        language="bash"
        code={`sorm db push   # create migrations + apply`}
      />
    </DocPage>
  );
}
