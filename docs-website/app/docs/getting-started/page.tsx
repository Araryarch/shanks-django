import { H1, H2, Lead, P, InlineCode, CodeBlock, SimpleCodeBlock, Alert, H3, Section } from '@/components/Typography'

export default function GettingStartedPage() {
  return (
    <div>
      <H1>Getting Started</H1>
      <Lead>Get up and running with Shanks Django in minutes.</Lead>
      
      <Section>
        <H2>Installation</H2>
        <SimpleCodeBlock>pip install shanks-django</SimpleCodeBlock>
      </Section>

      <Section>
        <H2>Create New Project</H2>
        <SimpleCodeBlock>
          shanks new myproject{'\n'}
          cd myproject{'\n'}
          shanks run
        </SimpleCodeBlock>
        <P>
          This creates a new Django project with Shanks pre-configured. Visit{' '}
          <InlineCode>http://127.0.0.1:8000</InlineCode>{' '}
          to see your app.
        </P>
      </Section>

      <Section>
        <H2>Generate CRUD Endpoints (Quick!)</H2>
        <P>
          Shanks can generate complete CRUD endpoints with models automatically:
        </P>
        <SimpleCodeBlock>
          shanks create posts --crud
        </SimpleCodeBlock>
        <P>
          This creates <InlineCode>app/models/posts.py</InlineCode> and{' '}
          <InlineCode>app/routes/posts.py</InlineCode> with:
        </P>
        <ul className="list-disc list-inside space-y-1 text-neutral-300 ml-4 mt-2">
          <li>List with pagination</li>
          <li>Get by ID</li>
          <li>Create, Update, Delete</li>
          <li>Auth checks</li>
        </ul>
      </Section>

      <Section>
        <H2>Generate Auth Endpoints</H2>
        <P>Simple auth (login, register, me):</P>
        <SimpleCodeBlock>shanks create auth --simple</SimpleCodeBlock>
        <P>Complete auth (with email verification):</P>
        <SimpleCodeBlock>shanks create auth --complete</SimpleCodeBlock>
      </Section>

      <Section>
        <H2>Your First Route</H2>
        <P>
          Create a file <InlineCode>app/routes/__init__.py</InlineCode>:
        </P>
        <CodeBlock title="app/routes/__init__.py">
          <span className="text-red-500">from</span> <span className="text-white">shanks</span> <span className="text-red-500">import</span> <span className="text-white">App</span>{'\n\n'}
          <span className="text-neutral-600">app = App()</span>{'\n\n'}
          <span className="text-red-500">@app.get</span><span className="text-neutral-500">(</span><span className="text-neutral-400">"api/hello"</span><span className="text-neutral-500">)</span>{'\n'}
          <span className="text-red-500">def</span> <span className="text-white">hello</span><span className="text-neutral-500">(</span><span className="text-neutral-600">req</span><span className="text-neutral-500">)</span><span className="text-neutral-500">:</span>{'\n'}
          {'    '}<span className="text-red-500">return</span> <span className="text-neutral-500">{'{'}</span><span className="text-neutral-400">"message"</span><span className="text-neutral-500">:</span> <span className="text-neutral-400">"Hello from Shanks!"</span><span className="text-neutral-500">{'}'}</span>{'\n\n'}
          <span className="text-neutral-600">urlpatterns = app.get_urls()</span>
        </CodeBlock>
      </Section>

      <Section>
        <H2>Configure Settings</H2>
        <P>
          In <InlineCode>settings.py</InlineCode>:
        </P>
        <SimpleCodeBlock>ROOT_URLCONF = "app.routes"</SimpleCodeBlock>
        <P>That's it! No urls.py needed.</P>
      </Section>

      <Section>
        <H2>Run Migrations</H2>
        <SimpleCodeBlock>
          sorm db push{'\n'}
          # or separately:{'\n'}
          sorm make{'\n'}
          sorm db migrate
        </SimpleCodeBlock>
        <P>
          Use <InlineCode>sorm db push</InlineCode> to create and apply migrations in one command,
          similar to Prisma's <InlineCode>db push</InlineCode>.
        </P>
      </Section>

      <Section>
        <H2>Start Development Server</H2>
        <SimpleCodeBlock>
          shanks run{'\n'}
          # or{'\n'}
          python manage.py runserver
        </SimpleCodeBlock>
      </Section>

      <Alert type="success">
        <H3>Next Steps</H3>
        <P>
          Your Shanks Django app is now running. Check out the{' '}
          <a href="/docs/routing" className="text-red-500 hover:text-red-400 transition">Routing guide</a>{' '}
          to learn more about creating routes.
        </P>
      </Alert>
    </div>
  )
}
