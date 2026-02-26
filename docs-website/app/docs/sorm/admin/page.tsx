import { DocPage, CodeBlock, Callout } from '@/components/DocPage';

export default function SormAdminPage() {
  return (
    <DocPage title="Admin Panel" description="sorm studio opens Django Admin — your visual database browser.">

      <h2>Open Admin</h2>
      <CodeBlock
        language="bash"
        code={`# Start your server first
shanks run

# In another terminal
sorm studio
# → opens http://localhost:8000/admin`}
      />

      <h2>Create Superuser</h2>
      <CodeBlock
        language="bash"
        code={`sorm db shell

# Inside the shell:
from django.contrib.auth import get_user_model
User = get_user_model()
User.objects.create_superuser('admin', 'admin@example.com', 'password')`}
      />

      <Callout type="info">
        Django Admin is fully available. Register your models in <code>entity/admin.py</code> to manage
        them from the UI.
      </Callout>

      <h2>Register Models for Admin</h2>
      <CodeBlock
        filename="entity/admin.py"
        code={`from django.contrib import admin
from entity.post import Post
from entity.user import User

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'published', 'created_at']
    list_filter  = ['published']
    search_fields = ['title', 'content']`}
      />
    </DocPage>
  );
}
