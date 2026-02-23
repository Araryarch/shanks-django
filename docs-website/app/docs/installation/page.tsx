import { H1, H2, Lead, P, SimpleCodeBlock, Alert, H3, List, ListItem, Section } from '@/components/Typography'

export default function InstallationPage() {
  return (
    <div>
      <H1>Installation</H1>
      <Lead>Get Shanks Django installed on your system.</Lead>

      <Section>
        <H2>Requirements</H2>
        <List>
          <ListItem>Python 3.8 or higher</ListItem>
          <ListItem>Django 3.2 or higher</ListItem>
        </List>
      </Section>

      <Section>
        <H2>Install from PyPI</H2>
        <SimpleCodeBlock>pip install shanks-django</SimpleCodeBlock>
      </Section>

      <Section>
        <H2>Install from Wheel</H2>
        <P>If you have the .whl file:</P>
        <SimpleCodeBlock>pip install shanks_django-0.1.0-py3-none-any.whl</SimpleCodeBlock>
      </Section>

      <Section>
        <H2>Install from Source</H2>
        <SimpleCodeBlock>
          git clone https://github.com/Ararya/shanks-django.git{'\n'}
          cd shanks-django{'\n'}
          pip install -e .
        </SimpleCodeBlock>
      </Section>

      <Section>
        <H2>Optional Dependencies</H2>
        <div className="space-y-4">
          <div>
            <p className="text-xs text-neutral-600 mb-2">PostgreSQL support:</p>
            <SimpleCodeBlock>pip install shanks-django[postgres]</SimpleCodeBlock>
          </div>
          <div>
            <p className="text-xs text-neutral-600 mb-2">MySQL support:</p>
            <SimpleCodeBlock>pip install shanks-django[mysql]</SimpleCodeBlock>
          </div>
          <div>
            <p className="text-xs text-neutral-600 mb-2">All databases:</p>
            <SimpleCodeBlock>pip install shanks-django[all]</SimpleCodeBlock>
          </div>
        </div>
      </Section>

      <Section>
        <H2>Verify Installation</H2>
        <SimpleCodeBlock>
          shanks --version{'\n'}
          # or{'\n'}
          python -c "import shanks; print(shanks.__version__)"
        </SimpleCodeBlock>
      </Section>

      <Alert type="success">
        <H3>Next Steps</H3>
        <P>
          Now that Shanks is installed, check out the{' '}
          <a href="/docs/getting-started" className="text-red-500 hover:text-red-400 transition">Getting Started</a>{' '}
          guide to create your first project.
        </P>
      </Alert>
    </div>
  )
}
