import { DocPage, CodeBlock, Callout } from '@/components/DocPage';

export default function CLIRunPage() {
  return (
    <DocPage title="shanks run" description="Start the development server with auto-reload — like nodemon for Python.">

      <h2>Basic Usage</h2>
      <CodeBlock language="bash" code={`shanks run`} />
      <p>Starts the server at <code>http://127.0.0.1:8000</code> by default.</p>

      <h2>Custom Port & Host</h2>
      <CodeBlock
        language="bash"
        code={`# Custom port
shanks run 3000

# Custom host and port
shanks run 0.0.0.0:8000

# Expose on network (useful for mobile testing)
shanks run 0.0.0.0:8000`}
      />

      <Callout type="success" title="Auto-Reload">
        Shanks watches your files and restarts automatically on change — similar to nodemon.
        No need to restart manually after editing routes or models.
      </Callout>

      <h2>Health Check</h2>
      <p>After starting, visit:</p>
      <CodeBlock
        language="text"
        code={`http://127.0.0.1:8000/api/health   → {"status": "ok", "service": "myproject"}
http://127.0.0.1:8000/docs         → Swagger UI`}
      />

      <h2>Production</h2>
      <p>Do not use <code>shanks run</code> in production. Use <code>shanks generate django</code> and deploy with gunicorn:</p>
      <CodeBlock language="bash" code={`gunicorn myproject.wsgi:application --bind 0.0.0.0:8000 --workers 4`} />
    </DocPage>
  );
}
