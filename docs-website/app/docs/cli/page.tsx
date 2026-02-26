import { CodeBlock } from '@/components/CodeBlock';
import { Callout } from '@/components/Callout';
import Link from 'next/link';

export default function CLIPage() {
  return (
    <div className="prose prose-gray dark:prose-invert max-w-none">
      <h1>Shanks CLI Reference</h1>
      <p className="lead">
        Complete guide to all Shanks command-line interface commands.
      </p>

      <Callout type="info" title="Quick Reference">
        Run <code>shanks help</code> to see all available commands.
      </Callout>

      <h2>Installation</h2>
      <p>
        The Shanks CLI is automatically installed when you install the shanks-django package:
      </p>
      <CodeBlock code="pip install shanks-django" language="bash" />

      <h2>Available Commands</h2>

      <div className="not-prose my-8 grid gap-4">
        <Link
          href="/docs/cli/new"
          className="block rounded-lg border border-gray-200 p-4 transition-colors hover:border-blue-500 dark:border-gray-800"
        >
          <h3 className="mb-2 text-lg font-semibold text-gray-900 dark:text-white">
            shanks new
          </h3>
          <p className="text-sm text-gray-600 dark:text-gray-400">
            Create a new Shanks project with complete structure
          </p>
        </Link>

        <Link
          href="/docs/cli/create"
          className="block rounded-lg border border-gray-200 p-4 transition-colors hover:border-blue-500 dark:border-gray-800"
        >
          <h3 className="mb-2 text-lg font-semibold text-gray-900 dark:text-white">
            shanks create
          </h3>
          <p className="text-sm text-gray-600 dark:text-gray-400">
            Generate CRUD endpoints, authentication, and more
          </p>
        </Link>

        <Link
          href="/docs/cli/generate"
          className="block rounded-lg border border-gray-200 p-4 transition-colors hover:border-blue-500 dark:border-gray-800"
        >
          <h3 className="mb-2 text-lg font-semibold text-gray-900 dark:text-white">
            shanks generate
          </h3>
          <p className="text-sm text-gray-600 dark:text-gray-400">
            Generate standard Django structure for deployment
          </p>
        </Link>

        <Link
          href="/docs/cli/run"
          className="block rounded-lg border border-gray-200 p-4 transition-colors hover:border-blue-500 dark:border-gray-800"
        >
          <h3 className="mb-2 text-lg font-semibold text-gray-900 dark:text-white">
            shanks run
          </h3>
          <p className="text-sm text-gray-600 dark:text-gray-400">
            Start the development server
          </p>
        </Link>
      </div>

      <h2>Command Overview</h2>

      <h3>shanks new &lt;project-name&gt;</h3>
      <p>Creates a new Shanks project with the following structure:</p>
      <CodeBlock
        code={`shanks new myproject

# Creates:
myproject/
├── internal/
│   ├── controller/
│   ├── routes/
│   ├── service/
│   └── middleware/
├── entity/
├── dto/
├── config/
├── utils/
└── manage.py`}
        language="bash"
      />

      <h3>shanks create &lt;name&gt; --crud</h3>
      <p>Generates complete CRUD endpoints for a resource:</p>
      <CodeBlock
        code={`shanks create posts --crud

# Generates:
# - entity/posts.py (Model)
# - internal/controller/posts.py (Controller)
# - internal/routes/posts.py (Routes)`}
        language="bash"
      />

      <h3>shanks create auth [--simple]</h3>
      <p>Generates authentication endpoints:</p>
      <CodeBlock
        code={`# Simple JWT auth (no email verification)
shanks create auth --simple

# Complete auth (with email verification)
shanks create auth`}
        language="bash"
      />

      <h3>shanks generate django</h3>
      <p>Converts Shanks project to standard Django structure:</p>
      <CodeBlock
        code={`shanks generate django

# Creates django_output/ with:
# - Standard Django structure
# - Auto-generated urls.py
# - Production requirements.txt
# - Deployment README`}
        language="bash"
      />

      <h3>shanks run</h3>
      <p>Starts the development server:</p>
      <CodeBlock
        code="shanks run" language="bash" />

      <Callout type="success" title="Pro Tip">
        Use <code>shanks help</code> to see all available commands and options.
      </Callout>

      <h2>Next Steps</h2>
      <ul>
        <li>
          <Link href="/docs/cli/new">Learn more about creating projects</Link>
        </li>
        <li>
          <Link href="/docs/cli/create">Explore code generation</Link>
        </li>
        <li>
          <Link href="/docs/sorm">Database management with SORM</Link>
        </li>
      </ul>
    </div>
  );
}
