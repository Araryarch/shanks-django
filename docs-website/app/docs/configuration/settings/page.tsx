import { DocPage, CodeBlock, Callout } from '@/components/DocPage';

export default function ConfigSettingsPage() {
  return (
    <DocPage title="Django Settings" description="Shanks wraps Django settings — you can extend them directly.">

      <h2>Default settings.py</h2>
      <CodeBlock
        filename="myproject/settings.py"
        code={`from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = os.environ['SECRET_KEY']
DEBUG = os.environ.get('DEBUG', 'False') == 'True'
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost').split(',')

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'entity',     # Your models
    # ...
]`}
      />

      <h2>Adding Third-Party Apps</h2>
      <CodeBlock
        code={`# Just add to INSTALLED_APPS like any Django project
INSTALLED_APPS = [
    # ...
    'rest_framework',
    'corsheaders',
    'django_filters',
]`}
      />

      <Callout type="info">
        Shanks doesn't restrict what you put in <code>settings.py</code>. It's a standard Django project
        under the hood — all Django features and third-party packages work.
      </Callout>
    </DocPage>
  );
}
