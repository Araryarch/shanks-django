import { DocPage, CodeBlock } from '@/components/DocPage';

export default function RoutingMethodsPage() {
  return (
    <DocPage title="HTTP Methods" description="All standard HTTP methods are supported — GET, POST, PUT, PATCH, DELETE.">

      <h2>All Supported Methods</h2>
      <CodeBlock
        code={`from shanks import App

app = App()

@app.get('api/resource')
def read(req): ...

@app.post('api/resource')
def create(req): ...

@app.put('api/resource/<resource_id>')
def replace(req, resource_id): ...

@app.patch('api/resource/<resource_id>')
def partial_update(req, resource_id): ...

@app.delete('api/resource/<resource_id>')
def destroy(req, resource_id): ...`}
      />

      <h2>RESTful Convention</h2>
      <CodeBlock
        language="text"
        code={`GET    /api/posts           → list all posts
GET    /api/posts/<id>      → get one post
POST   /api/posts           → create a post
PUT    /api/posts/<id>      → replace a post
PATCH  /api/posts/<id>      → partially update
DELETE /api/posts/<id>      → delete a post`}
      />

      <h2>Same Path, Multiple Methods</h2>
      <CodeBlock
        code={`@app.get('api/profile')
def get_profile(req):
    return {'user': req.user}

@app.put('api/profile')
def update_profile(req):
    req.user.update_self(**req.body)
    return {'updated': True}

@app.delete('api/profile')
def delete_profile(req):
    req.user.delete_self()
    return {'deleted': True}`}
      />
    </DocPage>
  );
}
