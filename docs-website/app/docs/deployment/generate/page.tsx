import { DocPage, CodeBlock, Callout } from '@/components/DocPage';

export default function DeploymentGeneratePage() {
  return (
    <DocPage title="Generate Django" description="Convert Shanks to standard Django for deployment on any platform.">

      <h2>Run the Generator</h2>
      <CodeBlock language="bash" code={`shanks generate django`} />

      <h2>Output</h2>
      <CodeBlock
        language="text"
        code={`django_output/
├── myproject/
│   ├── settings.py
│   ├── urls.py        ← auto-generated from Shanks routes
│   └── wsgi.py
├── entity/
├── internal/
├── manage.py
├── requirements.txt
└── README.md          ← deployment instructions`}
      />

      <h2>Run Locally to Verify</h2>
      <CodeBlock
        language="bash"
        code={`cd django_output/
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver`}
      />

      <h2>Deploy with Gunicorn</h2>
      <CodeBlock
        language="bash"
        code={`gunicorn myproject.wsgi:application --bind 0.0.0.0:8000 --workers 4`}
      />

      <Callout type="info">
        The generated project is a standard Django project. Any guide for deploying Django applies.
      </Callout>
    </DocPage>
  );
}
