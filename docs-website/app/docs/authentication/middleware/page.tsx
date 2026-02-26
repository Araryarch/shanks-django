import { DocPage, CodeBlock, Callout } from '@/components/DocPage';

export default function AuthMiddlewarePage() {
  return (
    <DocPage title="Auth Middleware" description="Protect your routes using reusable authentication middleware.">

      <h2>JWT Auth Middleware</h2>
      <CodeBlock
        filename="internal/middleware/auth.py"
        code={`from shanks import Response
from shanks.auth import verify_token
from entity.user import User

def jwt_required(req, res, next):
    auth_header = req.headers.get('Authorization', '')
    if not auth_header.startswith('Bearer '):
        return Response().status_code(401).json({'error': 'Missing token'})

    token = auth_header.replace('Bearer ', '')
    payload = verify_token(token)
    if not payload:
        return Response().status_code(401).json({'error': 'Invalid or expired token'})

    req.user = User.find_unique(id=payload['user_id'])
    next()`}
      />

      <h2>Apply to a Group</h2>
      <CodeBlock
        code={`from shanks import App
from internal.middleware.auth import jwt_required

app = App()

# All routes under /api/v1/users are protected
users = app.group('api/v1/users', jwt_required)

@users.get('')
def list_users(req):
    return {'user': req.user.username}

app.include(users)`}
      />

      <h2>Apply to a Single Route</h2>
      <CodeBlock
        code={`@app.get('api/me', jwt_required)
def get_me(req):
    return {'user': {'id': req.user.id, 'username': req.user.username}}`}
      />

      <Callout type="info">
        Place auth middleware before business logic middleware in the chain so unauthenticated
        requests are rejected early.
      </Callout>
    </DocPage>
  );
}
