import { DocPage, CodeBlock, Callout } from '@/components/DocPage';

export default function InstallationPage() {
  return (
    <DocPage
      title="Installation"
      description="Install Shanks Django and get started in minutes."
    >
      <h2>Requirements</h2>
      <ul>
        <li>Python 3.8 or higher</li>
        <li>pip (Python package manager)</li>
        <li>Virtual environment (recommended)</li>
      </ul>

      <h2>Install via pip</h2>
      <CodeBlock code="pip install shanks-django" language="bash" />

      <Callout type="success" title="Installation Complete">
        You now have access to <code>shanks</code> and <code>sorm</code> CLI commands!
      </Callout>

      <h2>Verify Installation</h2>
      <CodeBlock 
        code={`shanks help
sorm --help

# Check version
python -c "import shanks; print(shanks.__version__)"`}
        language="bash"
      />

      <h2>Create Your First Project</h2>
      <CodeBlock code="shanks new myproject" language="bash" />

      <Callout type="info">
        Continue to <a href="/docs/getting-started">Getting Started</a> for a complete tutorial.
      </Callout>
    </DocPage>
  );
}
