import { DocPage, CodeBlock, Callout } from '@/components/DocPage';

export default function JWTPage() {
  return (
    <DocPage title="JWT Auth" description="JSON Web Token authentication — stateless, secure, production-ready.">

      <h2>How It Works</h2>
      <p>
        After a successful login, Shanks signs a JWT with your secret key. The client stores the token
        and sends it as a <code>Bearer</code> token in the <code>Authorization</code> header on subsequent
        requests.
      </p>

      <h2>Generated Login Route</h2>
      <CodeBlock
        filename="internal/routes/auth.py"
        code={`from shanks import App, Response
from shanks.auth import create_token, verify_token
from entity.user import User

app = App()

@app.post('api/auth/login')
def login(req):
    username = req.body.get('username')
    password = req.body.get('password')

    user = User.find_unique(username=username)
    if not user or not user.check_password(password):
        return Response().status_code(401).json({'error': 'Invalid credentials'})

    token = create_token({'user_id': user.id})
    return {'token': token, 'user': {'id': user.id, 'username': user.username}}`}
      />

      <h2>Token Refresh</h2>
      <CodeBlock
        code={`@app.post('api/auth/refresh')
def refresh(req):
    token = req.body.get('token')
    payload = verify_token(token)
    if not payload:
        return Response().status_code(401).json({'error': 'Invalid token'})

    new_token = create_token({'user_id': payload['user_id']})
    return {'token': new_token}`}
      />

      <h2>Token Configuration</h2>
      <CodeBlock
        language="bash"
        filename=".env"
        code={`JWT_SECRET_KEY=your-very-secret-key-here
JWT_EXPIRY_HOURS=24
JWT_REFRESH_EXPIRY_DAYS=30`}
      />

      <Callout type="info">
        Change <code>JWT_SECRET_KEY</code> before deploying. A compromised secret means all tokens are compromised.
      </Callout>
    </DocPage>
  );
}
