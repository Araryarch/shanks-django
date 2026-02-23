import { H1, H2, Lead, P, CodeBlock, SimpleCodeBlock, Alert, H3, Section } from '@/components/Typography'

export default function ConfigurationPage() {
  return (
    <div>
      <H1>Configuration</H1>
      <Lead>Super simple settings with built-in helpers. No boilerplate needed.</Lead>

      <Section>
        <H2>Minimal Settings</H2>
        <P>Shanks provides helper functions to simplify Django settings:</P>
        <CodeBlock title="settings.py">
          <span className="text-red-500">from</span> <span className="text-white">shanks</span> <span className="text-red-500">import</span> <span className="text-neutral-500">(</span>{'\n'}
          {'    '}<span className="text-white">get_base_dir</span><span className="text-neutral-500">,</span>{'\n'}
          {'    '}<span className="text-white">get_secret_key</span><span className="text-neutral-500">,</span>{'\n'}
          {'    '}<span className="text-white">get_debug</span><span className="text-neutral-500">,</span>{'\n'}
          {'    '}<span className="text-white">get_allowed_hosts</span><span className="text-neutral-500">,</span>{'\n'}
          {'    '}<span className="text-white">get_database</span><span className="text-neutral-500">,</span>{'\n'}
          {'    '}<span className="text-white">get_installed_apps</span><span className="text-neutral-500">,</span>{'\n'}
          {'    '}<span className="text-white">get_middleware</span><span className="text-neutral-500">,</span>{'\n'}
          {'    '}<span className="text-white">get_templates</span><span className="text-neutral-500">,</span>{'\n'}
          {'    '}<span className="text-white">get_password_validators</span><span className="text-neutral-500">,</span>{'\n'}
          <span className="text-neutral-500">)</span>{'\n\n'}
          <span className="text-neutral-600"># Paths</span>{'\n'}
          <span className="text-neutral-600">BASE_DIR = get_base_dir(__file__)</span>{'\n\n'}
          <span className="text-neutral-600"># Security</span>{'\n'}
          <span className="text-neutral-600">SECRET_KEY = get_secret_key()</span>{'\n'}
          <span className="text-neutral-600">DEBUG = get_debug()</span>{'\n'}
          <span className="text-neutral-600">ALLOWED_HOSTS = get_allowed_hosts()</span>{'\n\n'}
          <span className="text-neutral-600"># Apps</span>{'\n'}
          <span className="text-neutral-600">INSTALLED_APPS = get_installed_apps([</span><span className="text-neutral-400">"app"</span><span className="text-neutral-600">])</span>{'\n\n'}
          <span className="text-neutral-600"># Middleware</span>{'\n'}
          <span className="text-neutral-600">MIDDLEWARE = get_middleware()</span>{'\n\n'}
          <span className="text-neutral-600"># Routing</span>{'\n'}
          <span className="text-neutral-600">ROOT_URLCONF = </span><span className="text-neutral-400">"app.routes"</span>{'\n\n'}
          <span className="text-neutral-600"># Database</span>{'\n'}
          <span className="text-neutral-600">DATABASES = get_database(BASE_DIR)</span>
        </CodeBlock>
      </Section>

      <Section>
        <H2>Environment Variables</H2>
        <P>All helpers auto-load from .env file. No manual dotenv import needed:</P>
        <SimpleCodeBlock>
          SECRET_KEY=your-secret-key-here{'\n'}
          DEBUG=True{'\n'}
          ALLOWED_HOSTS=localhost,127.0.0.1{'\n'}
          DATABASE_URL=postgresql://user:pass@localhost/db
        </SimpleCodeBlock>
      </Section>

      <Section>
        <H2>Config Helpers</H2>
        
        <div className="space-y-6">
          <div>
            <H3>get_base_dir(file_path)</H3>
            <P>Get base directory from __file__</P>
            <CodeBlock>
              <span className="text-neutral-600">BASE_DIR = get_base_dir(__file__)</span>
            </CodeBlock>
          </div>

          <div>
            <H3>get_secret_key(default)</H3>
            <P>Get SECRET_KEY from environment</P>
            <CodeBlock>
              <span className="text-neutral-600">SECRET_KEY = get_secret_key()</span>{'\n'}
              <span className="text-neutral-600"># or with custom default</span>{'\n'}
              <span className="text-neutral-600">SECRET_KEY = get_secret_key(</span><span className="text-neutral-400">"my-default-key"</span><span className="text-neutral-600">)</span>
            </CodeBlock>
          </div>

          <div>
            <H3>get_debug(default)</H3>
            <P>Get DEBUG boolean from environment</P>
            <CodeBlock>
              <span className="text-neutral-600">DEBUG = get_debug()</span>{'\n'}
              <span className="text-neutral-600"># Reads from DEBUG env var (True/False)</span>
            </CodeBlock>
          </div>

          <div>
            <H3>get_allowed_hosts(default)</H3>
            <P>Get ALLOWED_HOSTS list from environment</P>
            <CodeBlock>
              <span className="text-neutral-600">ALLOWED_HOSTS = get_allowed_hosts()</span>{'\n'}
              <span className="text-neutral-600"># Reads from ALLOWED_HOSTS env var (comma-separated)</span>{'\n'}
              <span className="text-neutral-600"># Example: ALLOWED_HOSTS=localhost,127.0.0.1,myapp.com</span>
            </CodeBlock>
          </div>

          <div>
            <H3>get_database(base_dir)</H3>
            <P>Get database configuration. Auto-detects from DATABASE_URL or defaults to SQLite</P>
            <CodeBlock>
              <span className="text-neutral-600">DATABASES = get_database(BASE_DIR)</span>{'\n'}
              <span className="text-neutral-600"># If DATABASE_URL is set, uses that</span>{'\n'}
              <span className="text-neutral-600"># Otherwise uses SQLite at BASE_DIR/db.sqlite3</span>
            </CodeBlock>
          </div>

          <div>
            <H3>get_installed_apps(extra_apps)</H3>
            <P>Get default Django apps plus your custom apps</P>
            <CodeBlock>
              <span className="text-neutral-600">INSTALLED_APPS = get_installed_apps([</span><span className="text-neutral-400">"app"</span><span className="text-neutral-500">,</span> <span className="text-neutral-400">"api"</span><span className="text-neutral-600">])</span>
            </CodeBlock>
          </div>

          <div>
            <H3>get_middleware()</H3>
            <P>Get default Django middleware (CSRF disabled for API)</P>
            <CodeBlock>
              <span className="text-neutral-600">MIDDLEWARE = get_middleware()</span>
            </CodeBlock>
          </div>

          <div>
            <H3>get_templates()</H3>
            <P>Get default Django templates configuration</P>
            <CodeBlock>
              <span className="text-neutral-600">TEMPLATES = get_templates()</span>
            </CodeBlock>
          </div>

          <div>
            <H3>get_password_validators(debug)</H3>
            <P>Get password validators (disabled in debug mode)</P>
            <CodeBlock>
              <span className="text-neutral-600">AUTH_PASSWORD_VALIDATORS = get_password_validators(DEBUG)</span>{'\n'}
              <span className="text-neutral-600"># Returns [] if DEBUG=True</span>{'\n'}
              <span className="text-neutral-600"># Returns full validators if DEBUG=False</span>
            </CodeBlock>
          </div>
        </div>
      </Section>

      <Section>
        <H2>Manual Environment Variables</H2>
        <P>You can also use env helpers directly:</P>
        <CodeBlock>
          <span className="text-red-500">from</span> <span className="text-white">shanks</span> <span className="text-red-500">import</span> <span className="text-white">env</span><span className="text-neutral-500">,</span> <span className="text-white">env_bool</span><span className="text-neutral-500">,</span> <span className="text-white">env_list</span><span className="text-neutral-500">,</span> <span className="text-white">env_int</span>{'\n\n'}
          <span className="text-neutral-600"># Get string</span>{'\n'}
          <span className="text-neutral-600">api_key = env(</span><span className="text-neutral-400">"API_KEY"</span><span className="text-neutral-500">,</span> <span className="text-neutral-400">"default-key"</span><span className="text-neutral-600">)</span>{'\n\n'}
          <span className="text-neutral-600"># Get boolean</span>{'\n'}
          <span className="text-neutral-600">debug = env_bool(</span><span className="text-neutral-400">"DEBUG"</span><span className="text-neutral-500">,</span> <span className="text-neutral-400">False</span><span className="text-neutral-600">)</span>{'\n\n'}
          <span className="text-neutral-600"># Get list</span>{'\n'}
          <span className="text-neutral-600">hosts = env_list(</span><span className="text-neutral-400">"ALLOWED_HOSTS"</span><span className="text-neutral-500">,</span> <span className="text-neutral-500">[</span><span className="text-neutral-400">"localhost"</span><span className="text-neutral-500">]</span><span className="text-neutral-600">)</span>{'\n\n'}
          <span className="text-neutral-600"># Get integer</span>{'\n'}
          <span className="text-neutral-600">port = env_int(</span><span className="text-neutral-400">"PORT"</span><span className="text-neutral-500">,</span> <span className="text-neutral-400">8000</span><span className="text-neutral-600">)</span>
        </CodeBlock>
      </Section>

      <Section>
        <H2>Complete Example</H2>
        <CodeBlock title="settings.py">
          <span className="text-red-500">from</span> <span className="text-white">shanks</span> <span className="text-red-500">import</span> <span className="text-neutral-500">(</span>{'\n'}
          {'    '}<span className="text-white">get_base_dir</span><span className="text-neutral-500">,</span> <span className="text-white">get_secret_key</span><span className="text-neutral-500">,</span> <span className="text-white">get_debug</span><span className="text-neutral-500">,</span>{'\n'}
          {'    '}<span className="text-white">get_allowed_hosts</span><span className="text-neutral-500">,</span> <span className="text-white">get_database</span><span className="text-neutral-500">,</span>{'\n'}
          {'    '}<span className="text-white">get_installed_apps</span><span className="text-neutral-500">,</span> <span className="text-white">get_middleware</span><span className="text-neutral-500">,</span>{'\n'}
          {'    '}<span className="text-white">get_templates</span><span className="text-neutral-500">,</span> <span className="text-white">get_password_validators</span><span className="text-neutral-500">,</span>{'\n'}
          <span className="text-neutral-500">)</span>{'\n\n'}
          <span className="text-neutral-600">BASE_DIR = get_base_dir(__file__)</span>{'\n'}
          <span className="text-neutral-600">SECRET_KEY = get_secret_key()</span>{'\n'}
          <span className="text-neutral-600">DEBUG = get_debug()</span>{'\n'}
          <span className="text-neutral-600">ALLOWED_HOSTS = get_allowed_hosts()</span>{'\n\n'}
          <span className="text-neutral-600">INSTALLED_APPS = get_installed_apps([</span><span className="text-neutral-400">"app"</span><span className="text-neutral-600">])</span>{'\n'}
          <span className="text-neutral-600">MIDDLEWARE = get_middleware()</span>{'\n'}
          <span className="text-neutral-600">ROOT_URLCONF = </span><span className="text-neutral-400">"app.routes"</span>{'\n'}
          <span className="text-neutral-600">TEMPLATES = get_templates()</span>{'\n'}
          <span className="text-neutral-600">WSGI_APPLICATION = </span><span className="text-neutral-400">"wsgi.application"</span>{'\n\n'}
          <span className="text-neutral-600">DATABASES = get_database(BASE_DIR)</span>{'\n'}
          <span className="text-neutral-600">AUTH_PASSWORD_VALIDATORS = get_password_validators(DEBUG)</span>{'\n\n'}
          <span className="text-neutral-600">LANGUAGE_CODE = </span><span className="text-neutral-400">"en-us"</span>{'\n'}
          <span className="text-neutral-600">TIME_ZONE = </span><span className="text-neutral-400">"UTC"</span>{'\n'}
          <span className="text-neutral-600">USE_I18N = </span><span className="text-neutral-400">True</span>{'\n'}
          <span className="text-neutral-600">USE_TZ = </span><span className="text-neutral-400">True</span>{'\n\n'}
          <span className="text-neutral-600">STATIC_URL = </span><span className="text-neutral-400">"static/"</span>{'\n'}
          <span className="text-neutral-600">STATIC_ROOT = BASE_DIR / </span><span className="text-neutral-400">"staticfiles"</span>{'\n'}
          <span className="text-neutral-600">DEFAULT_AUTO_FIELD = </span><span className="text-neutral-400">"django.db.models.BigAutoField"</span>
        </CodeBlock>
      </Section>

      <Alert type="success">
        <H3>Why Use Config Helpers?</H3>
        <P>
          No need to manually import os, Path, or dotenv. Everything is handled by Shanks.
          Your settings.py stays clean and focused on configuration, not boilerplate.
        </P>
      </Alert>
    </div>
  )
}
