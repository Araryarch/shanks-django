import { DocPage, CodeBlock, Callout } from '@/components/DocPage';

export default function SessionAuthPage() {
  return (
    <DocPage title="Session Auth" description="Cookie-based session authentication using Django's session framework.">

      <h2>Session Login</h2>
      <CodeBlock
        filename="internal/routes/auth.py"
        code={`from shanks import App, Response
from django.contrib.auth import authenticate, login, logout

app = App()

@app.post('api/auth/session/login')
def session_login(req):
    username = req.body.get('username')
    password = req.body.get('password')

    user = authenticate(username=username, password=password)
    if not user:
        return Response().status_code(401).json({'error': 'Invalid credentials'})

    login(req, user)   # Creates session cookie
    return {'user': {'id': user.id, 'username': user.username}}


@app.post('api/auth/session/logout')
def session_logout(req):
    logout(req)
    return {'message': 'Logged out'}`}
      />

      <h2>Accessing Session Data</h2>
      <CodeBlock
        code={`@app.get('api/profile')
def get_profile(req):
    if not req.user.is_authenticated:
        return Response().status_code(401).json({'error': 'Not logged in'})
    return {'user': {'id': req.user.id, 'username': req.user.username}}`}
      />

      <Callout type="info">
        Session auth requires Django's <code>SESSION_ENGINE</code> to be configured.
        The default (database-backed) sessions work out of the box.
      </Callout>
    </DocPage>
  );
}
