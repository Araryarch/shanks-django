import { DocPage, CodeBlock } from '@/components/DocPage';

export default function OrmModelsPage() {
  return (
    <DocPage title="Models" description="Define Django models inside the entity/ directory. Shanks reads them automatically.">

      <h2>Creating a Model</h2>
      <CodeBlock
        filename="entity/post.py"
        code={`from django.db import models

class Post(models.Model):
    title       = models.CharField(max_length=255)
    content     = models.TextField()
    author      = models.ForeignKey('entity.User', on_delete=models.CASCADE)
    published   = models.BooleanField(default=False)
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'entity'
        ordering  = ['-created_at']

    def __str__(self):
        return self.title`}
      />

      <h2>Using CLI to Generate</h2>
      <CodeBlock
        language="bash"
        code={`# Generates entity/posts.py + routes + controller
shanks create posts --crud`}
      />

      <h2>After Defining a Model</h2>
      <CodeBlock
        language="bash"
        code={`# Create & run migration
sorm db push

# Or step by step:
sorm make        # create migration file
sorm db migrate  # apply it`}
      />
    </DocPage>
  );
}
