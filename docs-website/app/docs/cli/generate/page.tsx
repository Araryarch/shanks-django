import { DocPage, CodeBlock, Callout } from '@/components/DocPage';

export default function CLIGeneratePage() {
  return (
    <DocPage title="shanks generate" description="Convert your Shanks project into a standard Django structure for deployment.">

      <h2>Usage</h2>
      <CodeBlock language="bash" code={`shanks generate django`} />

      <h2>What It Does</h2>
      <p>This command creates a <code>django_output/</code> folder with a fully standard Django project:</p>
      <CodeBlock
        language="text"
        code={`django_output/
├── myproject/
│   ├── settings.py
│   ├── urls.py        # Auto-generated from Shanks routes
│   └── wsgi.py
├── entity/            # Your models
├── internal/          # Your app code
├── manage.py
└── README.md          # Deployment guide`}
      />

      <h2>Why Use This?</h2>
      <ul>
        <li><strong>Easy deployment</strong> — many platforms expect standard Django layout</li>
        <li><strong>Comparison</strong> — see Shanks vs raw Django structure side by side</li>
        <li><strong>Migration path</strong> — move to pure Django if needed</li>
        <li><strong>Tooling compatibility</strong> — some tools require standard Django structure</li>
      </ul>

      <h2>Deploy the Output</h2>
      <CodeBlock
        language="bash"
        code={`cd django_output/
pip install -r requirements.txt
python manage.py collectstatic
gunicorn myproject.wsgi:application`}
      />

      <Callout type="info">
        The generated <code>urls.py</code> is auto-converted from your Shanks routes — no manual work needed.
      </Callout>
    </DocPage>
  );
}
