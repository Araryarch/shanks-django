import { DocPage, CodeBlock, Callout } from '@/components/DocPage';

export default function RailwayPage() {
  return (
    <DocPage title="Deploy to Railway" description="Railway is the easiest platform for deploying Shanks APIs with a database.">

      <h2>Quick Deploy</h2>
      <ol>
        <li>Run <code>shanks generate django</code></li>
        <li>Push <code>django_output/</code> to a GitHub repo</li>
        <li>Go to <a href="https://railway.app">railway.app</a> → New Project → Deploy from GitHub</li>
        <li>Select your repo</li>
        <li>Add a PostgreSQL plugin</li>
        <li>Set environment variables</li>
      </ol>

      <h2>Required Environment Variables</h2>
      <CodeBlock
        language="bash"
        code={`DEBUG=False
SECRET_KEY=your-production-secret
DATABASE_URL=\${RAILWAY_DATABASE_URL}   # auto-set by Railway postgres plugin
ALLOWED_HOSTS=your-app.up.railway.app`}
      />

      <h2>Procfile / Start Command</h2>
      <CodeBlock
        language="bash"
        code={`# Railway uses Procfile or the start command setting:
gunicorn myproject.wsgi:application --bind 0.0.0.0:$PORT`}
      />

      <h2>Run Migrations</h2>
      <p>Use Railway's shell or set a release command:</p>
      <CodeBlock
        filename="Procfile"
        language="text"
        code={`release: python manage.py migrate
web: gunicorn myproject.wsgi:application --bind 0.0.0.0:$PORT`}
      />

      <Callout type="success">
        Railway automatically detects Python projects and installs from <code>requirements.txt</code>.
      </Callout>
    </DocPage>
  );
}
