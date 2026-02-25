![shanks](https://github.com/user-attachments/assets/70a7c689-f475-41b4-862b-6b9371d127e9)

# Shanks Django CLI

🚀 CLI tool untuk generate Django project dengan Express.js syntax dan Prisma-like ORM.

[![PyPI version](https://badge.fury.io/py/shanks-django.svg)](https://pypi.org/project/shanks-django/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 📦 Installation

```bash
pip install shanks-django
```

## ✨ Features

- 🎯 **Express.js-like syntax** - Familiar routing
- 🔥 **Prisma-like ORM** - Modern database queries
- ⚡ **Auto-caching enabled** - GET requests cached by default (10x faster!)
- 🔄 **Smart cache invalidation** - Auto-clear on POST/PUT/DELETE
- 🎨 **Route grouping** - Organize routes like Gin (Go)
- 🚀 **Auto-type detection** - No need to specify `<int:id>`
- 📚 **Swagger built-in** - Auto-generated API docs
- 🛠️ **CLI generators** - Generate CRUD & Auth instantly
- 🗄️ **SORM CLI** - Prisma-like database management

## 🚀 Quick Start

```bash
# Buat project baru
shanks new myproject
cd myproject

# Generate CRUD endpoints
shanks create posts --crud

# Generate auth endpoints  
shanks create auth --simple

# Run migrations
sorm make
sorm db migrate

# Or use push (make + migrate in one command)
sorm db push

# Start server
shanks run
```

Visit:
- API: http://127.0.0.1:8000/api/health
- Swagger: http://127.0.0.1:8000/docs

That's it! Your API now has:
- ✅ Auto-caching enabled (10x faster GET requests)
- ✅ Smart cache invalidation on writes
- ✅ Swagger documentation
- ✅ CRUD endpoints with pagination

## 🛠️ CLI Commands

### Development Server

```bash
# Start server (default: 127.0.0.1:8000)
shanks run

# Custom port
shanks run 3000

# Custom host dan port
shanks run 0.0.0.0:8000
```

Auto-reload seperti nodemon, langsung detect perubahan file.

### Project Management

```bash
# Buat project baru dengan struktur Go-like
shanks new myproject
```

Struktur yang di-generate:
```
myproject/
├── manage.py
├── myproject/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── app/
    ├── models/
    ├── routes/
    ├── middleware/
    └── dto/
```

### Generate CRUD Endpoints

```bash
# Generate full CRUD dengan model
shanks create posts --crud
```

Ini akan create:
- `app/models/posts.py` - Model dengan SORM
- `app/routes/posts.py` - Complete CRUD routes

Yang di-generate:
- ✅ List dengan pagination (page, limit)
- ✅ Get by ID (findById)
- ✅ Create
- ✅ Update
- ✅ Delete
- ✅ Auth checks
- ✅ Error handling

Contoh hasil generate:

```python
# app/routes/posts.py
from shanks import App, Response
from app.models import Post

app = App()

@app.get('api/posts')
def list_posts(req):
    page = int(req.query.get('page', 1))
    limit = int(req.query.get('limit', 10))
    posts = Post.find_many()
    return {'posts': [...], 'page': page, 'limit': limit}

@app.get('api/posts/<int:post_id>')
def get_post(req, post_id):
    post = Post.find_unique(id=post_id)
    if not post:
        return Response().status_code(404).json({'error': 'Not found'})
    return {'post': {...}}

@app.post('api/posts')
def create_post(req):
    post = Post.create(**req.body)
    return Response().status_code(201).json({'id': post.id})

@app.put('api/posts/<int:post_id>')
def update_post(req, post_id):
    post = Post.find_unique(id=post_id)
    post.update_self(**req.body)
    return {'updated': True}

@app.delete('api/posts/<int:post_id>')
def delete_post(req, post_id):
    post = Post.find_unique(id=post_id)
    post.delete_self()
    return {'deleted': True}
```

### Generate Auth Endpoints

```bash
# Simple auth: /login, /register, /me
shanks create auth --simple

# Complete auth: + email verification
shanks create auth --complete
```

Yang di-generate untuk `--simple`:
- POST `/api/auth/register` - Register user baru
- POST `/api/auth/login` - Login user
- GET `/api/auth/me` - Get current user

Yang di-generate untuk `--complete`:
- Semua dari `--simple`
- POST `/api/auth/verify` - Email verification
- POST `/api/auth/resend` - Resend verification email

### Database Management (SORM)

```bash
# Create migrations
sorm make

# Apply migrations
sorm db migrate

# Create + apply migrations (one command)
sorm db push

# Reset database (flush all data)
sorm db reset

# Open database shell
sorm db shell

# Open admin panel (like Prisma Studio)
sorm studio
```

Command `sorm` mirip dengan Prisma CLI:
- `sorm make` = `prisma migrate dev --create-only`
- `sorm db migrate` = `prisma migrate deploy`
- `sorm db push` = `prisma db push`
- `sorm studio` = `prisma studio` (tapi pake Django Admin)

### Auto-Type Detection di Routes

Sekarang gak perlu specify type di URL parameters! Shanks auto-detect:

```python
# Old way (masih bisa dipakai)
@app.get('api/posts/<int:post_id>')
def get_post(req, post_id):
    return {'id': post_id}

# New way (auto-detect)
@app.get('api/posts/<post_id>')  # auto-detect as int karena nama 'post_id'
def get_post(req, post_id):
    return {'id': post_id}

@app.get('api/users/<username>')  # auto-detect as string
def get_user(req, username):
    return {'username': username}
```

Auto-detection rules:
- Parameter ends with `_id` atau nama `id` → treated as `int`
- Lainnya → treated as `string`
- Bisa tetap specify type explicitly: `<int:id>`, `<slug:slug>`, `<uuid:uuid>`

### Route Grouping (Gin-style)

Organize routes dengan grouping seperti Gin di Go:

```python
from shanks import App

app = App()

# Create route group
auth = app.group('api/v1/auth')

@auth.post('login')
def login(req):
    return {'message': 'Login'}

@auth.post('register')
def register(req):
    return {'message': 'Register'}

@auth.get('me')
def me(req):
    return {'user': req.user}

# Include group to main app
app.include(auth)

urlpatterns = app.get_urls()
```

Hasil:
- POST `/api/v1/auth/login`
- POST `/api/v1/auth/register`
- GET `/api/v1/auth/me`

#### With Middleware

```python
# Auth middleware
def auth_middleware(req, res, next):
    if not req.headers.get('Authorization'):
        return Response().status_code(401).json({'error': 'Unauthorized'})
    next()

# Protected group with middleware
admin = app.group('api/v1/admin', auth_middleware)

@admin.get('users')
def get_users(req):
    return {'users': []}

@admin.get('settings')
def get_settings(req):
    return {'settings': {}}

app.include(admin)
```

#### Multiple Groups

```python
# Auth routes
auth = app.group('api/v1/auth')
@auth.post('login')
def login(req): ...

# User routes
users = app.group('api/v1/users')
@users.get('')
def list_users(req): ...
@users.get('<user_id>')
def get_user(req, user_id): ...

# Post routes
posts = app.group('api/v1/posts')
@posts.get('')
def list_posts(req): ...

# Include all
app.include(auth, users, posts)
```

Lihat [ROUTE_GROUPING_EXAMPLE.md](ROUTE_GROUPING_EXAMPLE.md) untuk contoh lengkap!

### Built-in Caching (Enabled by Default!)

Shanks automatically caches all GET requests - 10x faster responses with zero configuration!

```python
from shanks import App

# Cache is enabled by default!
app = App()

@app.get('api/posts')
def list_posts(req):
    # First request: fetches from DB, caches result
    # Next requests: served from cache (10x faster!)
    return {'posts': [...]}

@app.post('api/posts')
def create_post(req):
    # Automatically invalidates /api/posts cache
    return {'created': True}
```

#### Customize Cache

```python
# Change cache TTL (default 5 minutes)
app.cache_config(ttl=600)  # Cache for 10 minutes

# Cache specific methods
app.cache_config(ttl=300, methods=['GET', 'HEAD'])

# Disable cache for specific group
realtime = app.group('api/realtime')
realtime.disable_cache()  # No caching for realtime endpoints

# Different cache settings per group
api_v1 = app.group('api/v1')
api_v1.cache_config(ttl=60)  # 1 minute cache

api_v2 = app.group('api/v2')
api_v2.cache_config(ttl=600)  # 10 minutes cache
```

#### Manual Cache Control

```python
from shanks import invalidate_cache, get_cache

# Clear all cache
invalidate_cache()

# Clear specific pattern
invalidate_cache('/api/posts')

# Direct cache access
cache = get_cache()
cache.set('key', 'value', ttl=300)
value = cache.get('key')
cache.delete('key')
```

#### How It Works

1. **Auto-cache GET requests**: First request fetches from DB and caches
2. **Smart invalidation**: POST/PUT/DELETE automatically clear related cache
3. **Pattern matching**: `/api/posts/123` invalidates `/api/posts` cache
4. **TTL-based**: Cache expires after configured time (default 5 minutes)

Benefits:
- ⚡ 10x faster response times
- 🔄 Automatic - no code changes needed
- 🧠 Smart invalidation on writes
- 💾 Memory efficient with TTL
- 🎯 Pattern-based invalidation

### Code Quality

```bash
# Format code dengan Black
shanks format

# Lint dengan Flake8
shanks lint

# Format + Lint sekaligus
shanks check
```

### Help

```bash
# Lihat semua commands
shanks help
```

## 📖 Dokumentasi Lengkap

CLI ini adalah bagian dari Shanks Django framework yang menyediakan:
- Express.js-like syntax untuk routing
- Prisma-like ORM untuk database queries
- Built-in caching, CORS, Swagger
- Middleware support
- Multi-database support (PostgreSQL, MySQL, MongoDB, Redis)

Untuk dokumentasi lengkap tentang API, ORM, middleware, dan fitur lainnya:
- **GitHub**: https://github.com/Ararya/shanks-django
- **Documentation**: https://github.com/Ararya/shanks-django/wiki

## 🎁 VSCode Extension

Install extension untuk snippets dan IntelliSense:

1. Buka VSCode
2. Extensions (Ctrl+Shift+X)
3. Cari "Shanks Django"
4. Install

Atau langsung: https://marketplace.visualstudio.com/items?itemName=Ararya.shanks-django

Snippets yang tersedia:
- `shanks-app` - Create new Shanks app
- `shanks-get` - GET route
- `shanks-post` - POST route
- `shanks-crud` - Full CRUD template
- Dan banyak lagi...

## 🤝 Contributing

Contributions welcome! Check [Contributing Guide](CONTRIBUTING.md).

```bash
# Clone repository
git clone https://github.com/Ararya/shanks-django.git
cd shanks-django

# Install dependencies
pip install -e ".[dev]"

# Run tests
pytest
```

## 📝 License

MIT License - see [LICENSE](LICENSE) file.

## 🔗 Links

- **GitHub**: https://github.com/Ararya/shanks-django
- **PyPI**: https://pypi.org/project/shanks-django/
- **Issues**: https://github.com/Ararya/shanks-django/issues
- **VSCode Extension**: https://marketplace.visualstudio.com/items?itemName=Ararya.shanks-django

---

Made with ❤️ by [Ararya](https://github.com/Ararya)
