import { DocPage, CodeBlock, Callout } from '@/components/DocPage';

export default function SwaggerPage() {
  return (
    <DocPage title="Swagger / OpenAPI" description="Auto-generated interactive API docs available at /docs as soon as you run shanks run.">

      <h2>Auto-generated Docs</h2>
      <p>
        Shanks automatically generates a Swagger UI at <code>/docs</code> and an OpenAPI JSON schema
        at <code>/openapi.json</code>. No configuration required.
      </p>

      <h2>Access Swagger UI</h2>
      <CodeBlock
        language="bash"
        code={`shanks run

# Open in browser:
# http://127.0.0.1:8000/docs         → Swagger UI
# http://127.0.0.1:8000/openapi.json → Raw OpenAPI schema`}
      />

      <h2>Add Descriptions</h2>
      <p>Use docstrings to add descriptions visible in the Swagger UI:</p>
      <CodeBlock
        code={`@app.get('api/posts')
def list_posts(req):
    """
    List all posts with pagination.

    Query params:
    - page (int): page number, default 1
    - limit (int): results per page, default 10
    """
    return {'posts': []}`}
      />

      <Callout type="info">
        Shanks reads function docstrings and type hints to build the OpenAPI schema automatically.
      </Callout>

      <h2>Request / Response Types</h2>
      <CodeBlock
        code={`from shanks import App, Response
from typing import Optional

@app.post('api/posts')
def create_post(req):
    """
    Create a new post.

    Body: { title: str, content: str, published: bool }
    Returns: { id: int }
    """
    post = Post.create(**req.body)
    return Response().status_code(201).json({'id': post.id})`}
      />
    </DocPage>
  );
}
