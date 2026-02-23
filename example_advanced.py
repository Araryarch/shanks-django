from shanks import Ace, Request, Response
from django.contrib.auth.decorators import login_required
from django.db import models

app = Ace()

# Akses Django ORM langsung
class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()

# Middleware dengan Django session
def auth_check(req: Request):
    if not req.user.is_authenticated:
        return Response().status_code(401).json({'error': 'Login required'})

# Route dengan Django authentication
@app.get('api/profile')
def get_profile(req: Request):
    # Akses user dari Django
    user = req.user
    
    # Akses session
    visits = req.session.get('visits', 0)
    req.session['visits'] = visits + 1
    
    return {
        'username': user.username,
        'email': user.email,
        'visits': visits + 1
    }

# Upload file dengan Django
@app.post('api/upload')
def upload_file(req: Request):
    file = req.files.get('file')
    if file:
        # Process file dengan Django
        return {'filename': file.name, 'size': file.size}
    return Response().status_code(400).json({'error': 'No file'})

# Render Django template
@app.get('dashboard')
def dashboard(req: Request):
    return Response().render(req.django, 'dashboard.html', {
        'user': req.user,
        'data': {'title': 'Dashboard'}
    })

# Set cookie
@app.post('api/login')
def login(req: Request):
    token = 'abc123'
    return Response().json({'success': True}).cookie('token', token, max_age=3600)

# Redirect
@app.get('old-url')
def old_url(req: Request):
    return Response().redirect('/new-url')

# Akses full Django request jika perlu
@app.get('api/advanced')
def advanced(req: Request):
    # Akses langsung Django request
    django_req = req.django
    
    # Semua fitur Django tersedia
    ip = django_req.META.get('REMOTE_ADDR')
    user_agent = django_req.META.get('HTTP_USER_AGENT')
    
    # Query Django ORM
    users = User.objects.all()
    
    return {
        'ip': ip,
        'user_agent': user_agent,
        'total_users': users.count()
    }

urlpatterns = app.get_urls()
