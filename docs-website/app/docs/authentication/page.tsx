import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';

export default function AuthenticationPage() {
  return (
    <div className="space-y-12">
      <div className="space-y-4">
        <h1 className="text-4xl font-bold tracking-tight">Authentication</h1>
        <p className="text-xl text-muted-foreground">
          Build secure authentication with JWT, sessions, or Django's built-in auth system.
        </p>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Quick Start with CLI</CardTitle>
          <CardDescription>
            Generate complete auth system with one command.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <div>
              <h3 className="text-lg font-semibold mb-2">Simple Auth</h3>
              <pre className="bg-background border border-border rounded-lg p-3 overflow-x-auto">
                <code className="text-sm">{`shanks create auth --simple`}</code>
              </pre>
              <p className="text-sm text-muted-foreground mt-2">
                Generates: POST /api/auth/login, POST /api/auth/register, GET /api/auth/me
              </p>
            </div>

            <div>
              <h3 className="text-lg font-semibold mb-2">Complete Auth</h3>
              <pre className="bg-background border border-border rounded-lg p-3 overflow-x-auto">
                <code className="text-sm">{`shanks create auth --complete`}</code>
              </pre>
              <p className="text-sm text-muted-foreground mt-2">
                Includes email verification, password reset, and more.
              </p>
            </div>
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>JWT Authentication</CardTitle>
          <CardDescription>
            Token-based authentication for stateless APIs.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <pre className="bg-background border border-border rounded-lg p-4 overflow-x-auto">
            <code className="text-sm">{`from shanks import App, Response, User, authenticate
import jwt
from datetime import datetime, timedelta

app = App()
SECRET_KEY = 'your-secret-key'

def create_token(user_id, username):
    payload = {
        'user_id': user_id,
        'username': username,
        'exp': datetime.utcnow() + timedelta(days=7)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm='HS256')

def verify_token(token):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
    except:
        return None

# Register
@app.post('api/auth/register')
def register(req):
    username = req.body.get('username')
    email = req.body.get('email')
    password = req.body.get('password')
    
    if User.find_unique(username=username):
        return Response().status_code(400).json({
            'error': 'Username already exists'
        })
    
    user = User.create(
        username=username,
        email=email,
        password=password
    )
    
    token = create_token(user.id, user.username)
    return Response().status_code(201).json({
        'token': token,
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email
        }
    })

# Login
@app.post('api/auth/login')
def login(req):
    username = req.body.get('username')
    password = req.body.get('password')
    
    user = authenticate(username=username, password=password)
    if not user:
        return Response().status_code(401).json({
            'error': 'Invalid credentials'
        })
    
    token = create_token(user.id, user.username)
    return {
        'token': token,
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email
        }
    }`}</code>
          </pre>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Auth Middleware</CardTitle>
          <CardDescription>
            Protect routes with authentication middleware.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <pre className="bg-background border border-border rounded-lg p-4 overflow-x-auto">
            <code className="text-sm">{`def auth_required(req, res, next):
    auth_header = req.headers.get('Authorization')
    
    if not auth_header or not auth_header.startswith('Bearer '):
        return Response().status_code(401).json({
            'error': 'Unauthorized'
        })
    
    token = auth_header.split(' ')[1]
    payload = verify_token(token)
    
    if not payload:
        return Response().status_code(401).json({
            'error': 'Invalid token'
        })
    
    # Attach user to request
    req.user = User.find_unique(id=payload['user_id'])
    if not req.user:
        return Response().status_code(401).json({
            'error': 'User not found'
        })
    
    next()

# Apply to all routes
app.use(auth_required)

# Or apply to specific routes
@app.get('api/profile')
def get_profile(req):
    return {
        'id': req.user.id,
        'username': req.user.username,
        'email': req.user.email
    }`}</code>
          </pre>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Session-Based Auth</CardTitle>
          <CardDescription>
            Use Django's built-in session authentication.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <pre className="bg-background border border-border rounded-lg p-4 overflow-x-auto">
            <code className="text-sm">{`from shanks import App, Response, authenticate
from django.contrib.auth import login as django_login, logout as django_logout

app = App()

@app.post('api/auth/login')
def login(req):
    username = req.body.get('username')
    password = req.body.get('password')
    
    user = authenticate(username=username, password=password)
    if not user:
        return Response().status_code(401).json({
            'error': 'Invalid credentials'
        })
    
    # Create session
    django_login(req.django, user)
    
    return {
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email
        }
    }

@app.post('api/auth/logout')
def logout(req):
    django_logout(req.django)
    return {'message': 'Logged out'}

@app.get('api/auth/me')
def get_me(req):
    if not req.user.is_authenticated:
        return Response().status_code(401).json({
            'error': 'Not authenticated'
        })
    
    return {
        'id': req.user.id,
        'username': req.user.username,
        'email': req.user.email
    }`}</code>
          </pre>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>User Model</CardTitle>
          <CardDescription>
            Work with Django's User model using Prisma-like syntax.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <pre className="bg-background border border-border rounded-lg p-4 overflow-x-auto">
            <code className="text-sm">{`from shanks import User, authenticate

# Find users
users = User.find_many()
user = User.find_unique(username='john')
user = User.find_first(email='john@example.com')

# Create user
user = User.create(
    username='john',
    email='john@example.com',
    password='secret123',  # Auto-hashed
    first_name='John',
    last_name='Doe'
)

# Authenticate
user = authenticate(username='john', password='secret123')
if user:
    print('Login successful')

# Update user
user.update_self(
    first_name='Johnny',
    email='johnny@example.com'
)

# Update password
user.update_self(password='newpassword')  # Auto-hashed

# Count users
total = User.count()
active = User.count(is_active=True)`}</code>
          </pre>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Password Reset</CardTitle>
          <CardDescription>
            Implement password reset with email verification.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <pre className="bg-background border border-border rounded-lg p-4 overflow-x-auto">
            <code className="text-sm">{`from shanks import App, Response, User
import secrets
from datetime import datetime, timedelta

app = App()

# Request password reset
@app.post('api/auth/forgot-password')
def forgot_password(req):
    email = req.body.get('email')
    user = User.find_first(email=email)
    
    if not user:
        # Don't reveal if email exists
        return {'message': 'If email exists, reset link sent'}
    
    # Generate reset token
    token = secrets.token_urlsafe(32)
    expires = datetime.utcnow() + timedelta(hours=1)
    
    # Save token (you'd store this in DB)
    # user.reset_token = token
    # user.reset_expires = expires
    # user.save()
    
    # Send email (implement your email service)
    # send_email(user.email, f'Reset link: /reset/{token}')
    
    return {'message': 'If email exists, reset link sent'}

# Reset password
@app.post('api/auth/reset-password')
def reset_password(req):
    token = req.body.get('token')
    new_password = req.body.get('password')
    
    # Verify token (check DB)
    # user = User.find_first(reset_token=token)
    # if not user or user.reset_expires < datetime.utcnow():
    #     return Response().status_code(400).json({
    #         'error': 'Invalid or expired token'
    #     })
    
    # Update password
    # user.update_self(password=new_password)
    # user.reset_token = None
    # user.reset_expires = None
    # user.save()
    
    return {'message': 'Password reset successful'}`}</code>
          </pre>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Role-Based Access Control</CardTitle>
          <CardDescription>
            Implement permissions and roles.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <pre className="bg-background border border-border rounded-lg p-4 overflow-x-auto">
            <code className="text-sm">{`def require_role(role):
    def middleware(req, res, next):
        if not req.user.is_authenticated:
            return Response().status_code(401).json({
                'error': 'Unauthorized'
            })
        
        # Check role (implement your role system)
        if not has_role(req.user, role):
            return Response().status_code(403).json({
                'error': 'Forbidden'
            })
        
        next()
    return middleware

# Admin only route
@app.delete('api/users/<int:user_id>')
def delete_user(req, user_id):
    # Apply middleware inline
    response = require_role('admin')(req, None, lambda: None)
    if response:
        return response
    
    user = User.find_unique(id=user_id)
    user.delete_self()
    return {'deleted': True}`}</code>
          </pre>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Complete Auth Example</CardTitle>
          <CardDescription>
            Full authentication system with JWT.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <pre className="bg-background border border-border rounded-lg p-4 overflow-x-auto">
            <code className="text-sm">{`from shanks import App, Response, User, authenticate
import jwt
from datetime import datetime, timedelta

app = App()
SECRET_KEY = 'your-secret-key'

def create_token(user):
    return jwt.encode({
        'user_id': user.id,
        'username': user.username,
        'exp': datetime.utcnow() + timedelta(days=7)
    }, SECRET_KEY, algorithm='HS256')

def auth_middleware(req, res, next):
    auth_header = req.headers.get('Authorization')
    if auth_header and auth_header.startswith('Bearer '):
        token = auth_header.split(' ')[1]
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            req.user = User.find_unique(id=payload['user_id'])
        except:
            pass
    next()

app.use(auth_middleware)

@app.post('api/auth/register')
def register(req):
    user = User.create(
        username=req.body.get('username'),
        email=req.body.get('email'),
        password=req.body.get('password')
    )
    return Response().status_code(201).json({
        'token': create_token(user),
        'user': {'id': user.id, 'username': user.username}
    })

@app.post('api/auth/login')
def login(req):
    user = authenticate(
        username=req.body.get('username'),
        password=req.body.get('password')
    )
    if not user:
        return Response().status_code(401).json({
            'error': 'Invalid credentials'
        })
    return {
        'token': create_token(user),
        'user': {'id': user.id, 'username': user.username}
    }

@app.get('api/auth/me')
def get_me(req):
    if not req.user or not req.user.is_authenticated:
        return Response().status_code(401).json({
            'error': 'Not authenticated'
        })
    return {
        'id': req.user.id,
        'username': req.user.username,
        'email': req.user.email
    }

urlpatterns = app.get_urls()`}</code>
          </pre>
        </CardContent>
      </Card>
    </div>
  );
}
