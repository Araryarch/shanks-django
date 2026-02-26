import { DocPage, CodeBlock, Callout } from '@/components/DocPage';

export default function RoutingGroupsPage() {
  return (
    <DocPage title="Route Groups" description="Organise routes with shared prefixes and middleware using Gin-style grouping.">

      <h2>Creating a Group</h2>
      <CodeBlock
        code={`from shanks import App

app = App()

auth = app.group('api/v1/auth')

@auth.post('login')
def login(req):
    return {'token': '...'}

@auth.post('register')
def register(req):
    return {'user': {}}

@auth.get('me')
def me(req):
    return {'user': req.user}

# Register the group
app.include(auth)
urlpatterns = app.get_urls()`}
        filename="internal/routes/__init__.py"
      />

      <Callout type="info">
        The group prefix and route path are joined automatically.{' '}
        <code>app.group('api/v1/auth')</code> + <code>@auth.post('login')</code> →{' '}
        <code>POST /api/v1/auth/login</code>
      </Callout>

      <h2>Groups with Middleware</h2>
      <CodeBlock
        code={`def auth_middleware(req, res, next):
    if not req.headers.get('Authorization'):
        return Response().status_code(401).json({'error': 'Unauthorized'})
    next()

# All routes in this group are protected
admin = app.group('api/v1/admin', auth_middleware)

@admin.get('users')
def get_users(req):
    return {'users': []}

@admin.delete('users/<user_id>')
def delete_user(req, user_id):
    return {'deleted': True}

app.include(admin)`}
      />

      <h2>Multiple Groups</h2>
      <CodeBlock
        code={`auth  = app.group('api/v1/auth')
users = app.group('api/v1/users')
posts = app.group('api/v1/posts')

# ... define routes ...

app.include(auth, users, posts)
urlpatterns = app.get_urls()`}
      />
    </DocPage>
  );
}
