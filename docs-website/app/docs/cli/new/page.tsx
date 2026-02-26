import { DocPage, CodeBlock, Callout } from '@/components/DocPage';
import Link from 'next/link';

export default function CLINewPage() {
  return (
    <DocPage title="shanks new" description="Scaffold a new Shanks project with a Go-like folder structure in seconds.">

      <h2>Usage</h2>
      <CodeBlock language="bash" code={`shanks new <project-name>`} />

      <h2>Example</h2>
      <CodeBlock
        language="bash"
        code={`shanks new myapi
cd myapi
sorm db push
shanks run`}
      />

      <h2>Generated Structure</h2>
      <CodeBlock
        language="text"
        code={`myapi/
├── internal/
│   ├── routes/        # API route definitions
│   │   └── __init__.py
│   ├── controller/    # HTTP request handlers
│   ├── service/       # Business logic
│   └── middleware/    # Custom middleware
├── entity/            # Database models
├── dto/               # Data Transfer Objects
├── config/            # App configuration
├── utils/             # Helper utilities
├── myapi/             # Django settings package
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── .env               # Environment variables
└── manage.py`}
      />

      <Callout type="success">
        The generated project includes a health endpoint at <code>/api/health</code> and a working
        <code>shanks run</code> out of the box.
      </Callout>
    </DocPage>
  );
}
