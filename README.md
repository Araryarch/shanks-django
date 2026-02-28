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

-  **Express.js-like syntax** - Familiar routing
-  **Prisma-like ORM** - Modern database queries
-  **Flexible CRUD generation** - Generate only what you need (-c, -r, -u, -d flags)
-  **Built-in JWT authentication** - Secure endpoints with --auth flag
-  **Auto-caching enabled** - GET requests cached by default (10x faster!)
-  **Smart cache invalidation** - Auto-clear on POST/PUT/DELETE
-  **Route grouping** - Organize routes like Gin (Go)
-  **Auto-type detection** - No need to specify `<int:id>`
-  **Swagger built-in** - Auto-generated API docs
-  **CLI generators** - Generate CRUD & Auth instantly
-  **SORM CLI** - Prisma-like database management

## 🚀 Quick Start

```bash
# Buat project baru
shanks new myproject
cd myproject

# Generate auth endpoints
shanks create auth --simple

# Generate CRUD endpoints
shanks create products              # Full CRUD
shanks create orders -c -r          # Only Create & Read
shanks create reviews --crud --auth # Full CRUD with JWT auth

# Run migrations
sorm make
sorm db migrate

# Or use push (make + migrate in one command)
sorm db push

# Start server
shanks run
```

Visit:
- API: http://127.0.0.1:8000/api/v1/health
- Auth: http://127.0.0.1:8000/api/v1/auth/register
- Swagger: http://127.0.0.1:8000/docs

That's it! Your API now has:
- ✅ JWT authentication (register, login, me)
- ✅ Flexible CRUD endpoints (only what you need)
- ✅ Auto-caching enabled (10x faster GET requests)
- ✅ Smart cache invalidation on writes
- ✅ Swagger documentation

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
# Generate full CRUD (default)
shanks create posts

# Generate full CRUD (explicit)
shanks create posts --crud

# Generate specific operations only
shanks create posts -c -r        # Only Create and Read
shanks create posts -c -r -u     # Create, Read, Update
shanks create posts -d           # Only Delete

# Generate with JWT authentication
shanks create posts --crud --auth    # Full CRUD, all protected
shanks create posts -c --auth        # Only Create with auth
shanks create posts -c -r --auth     # Create and Read with auth
```

**Flags:**
- `-c` = Create operation
- `-r` = Read operations (list + get by ID)
- `-u` = Update operation
- `-d` = Delete operation
- `--crud` = All operations (same as default)
- `--auth` = Require JWT authentication for all operations

Ini akan create:
- `db/entity/posts_entity.py` - Django model
- `internal/repository/posts_repository.py` - Data access layer
- `internal/service/posts_service.py` - Business logic
- `internal/controller/posts_controller.py` - Request handlers
- `internal/routes/posts_route.py` - API routes

Yang di-generate (tergantung flags):
- ✅ List dengan pagination (page, limit) - jika `-r`
- ✅ Get by ID - jika `-r`
- ✅ Create - jika `-c`
- ✅ Update - jika `-u`
- ✅ Delete - jika `-d`
- ✅ JWT auth middleware - jika `--auth`
- ✅ Error handling
- ✅ BaseDTO response format

Contoh hasil generate:

```python
# internal/routes/posts_route.py
from shanks import App
from internal.controller import posts_controller
from internal.middleware.auth_middleware import jwt_auth_middleware  # if --auth

router = App(prefix='/api/v1/posts')

# Apply auth middleware if --auth flag used
# router.use(jwt_auth_middleware)

@router.get('/')
def list_posts_route(req):
    return posts_controller.list_posts(req)

@router.get('/<id>')
def get_posts_route(req, id):
    return posts_controller.get_by_id(req, id)

@router.post('/')
def create_posts_route(req):
    return posts_controller.create(req)

@router.put('/<id>')
def update_posts_route(req, id):
    return posts_controller.update(req, id)

@router.delete('/<id>')
def delete_posts_route(req, id):
    return posts_controller.delete(req, id)
```

**Examples:**

```bash
# Blog API - full CRUD without auth
shanks create posts

# E-commerce - products with read-only public access
shanks create products -r

# Reviews - full CRUD with authentication required
shanks create reviews --crud --auth

# Orders - create and read only, with auth
shanks create orders -c -r --auth

# Admin actions - delete only with auth
shanks create reports -d --auth
```

### Generate Auth Endpoints

```bash
# Simple auth: register, login, logout, me
shanks create auth --simple

# Complete auth: + email verification, password reset
shanks create auth --complete
```

Yang di-generate untuk `--simple`:
- POST `/api/v1/auth/register` - Register user baru
- POST `/api/v1/auth/login` - Login user (returns JWT token)
- POST `/api/v1/auth/logout` - Logout user
- GET `/api/v1/auth/me` - Get current user info
- `internal/middleware/auth_middleware.py` - JWT middleware

Yang di-generate untuk `--complete`:
- Semua dari `--simple`
- POST `/api/v1/auth/verify` - Email verification
- POST `/api/v1/auth/resend` - Resend verification email
- POST `/api/v1/auth/forgot-password` - Request password reset
- POST `/api/v1/auth/reset-password` - Reset password with token

**Middleware yang di-generate:**
- `jwt_auth_middleware` - Require valid JWT token
- `optional_auth_middleware` - Optional JWT token (user available if provided)

**Usage:**

```python
# Protect routes with auth middleware
from shanks import App
from internal.middleware.auth_middleware import jwt_auth_middleware

router = App(prefix='/api/v1/posts')
router.use(jwt_auth_middleware)  # All routes require auth

@router.post('/')
def create_post(req):
    user = req.user  # Authenticated user
    return {'user_id': user.id}
```

### Generate Django Structure

```bash
# Generate full Django project structure
shanks generate django
```

Command ini akan:
- ✅ Generate folder `django_output/` dengan struktur Django standard
- ✅ Convert Shanks routes ke Django `urls.py`
- ✅ Copy semua models, migrations, dan app code
- ✅ Siap untuk deployment dengan Gunicorn/uWSGI
- ✅ Berguna untuk comparison atau deployment ke platform yang butuh Django standard

Output structure:
```
django_output/
├── myproject/
│   ├── settings.py
│   ├── urls.py          # Generated from Shanks routes
│   └── wsgi.py
├── entity/              # Your models
├── internal/            # Your app code
├── manage.py
└── README.md            # Deployment guide
```

Kenapa perlu ini?
- 🚀 **Easy deployment** - Banyak platform hosting familiar dengan Django standard
- 📊 **Comparison** - Compare Shanks vs Django structure
- 🔄 **Migration** - Kalau mau migrate dari Shanks ke pure Django
- 📦 **Compatibility** - Beberapa tools butuh Django standard structure

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
# Auto-detect as int (karena nama berakhiran '_id')
@app.get('api/posts/<post_id>')
def get_post(req, post_id):
    return {'id': post_id}

# Auto-detect as string
@app.get('api/users/<username>')
def get_user(req, username):
    return {'username': username}

# Masih bisa explicit type kalau perlu
@app.get('api/posts/<slug:slug>')  # force as slug
def get_user(req, username):
    return {'username': username}
```

Auto-detection rules:
- Parameter ends with `_id` atau nama `id` → treated as `int`
- Lainnya → treated as `string`
- Bisa tetap specify type explicitly: `<int:id>`, `<slug:slug>`, `<uuid:uuid>`

### Route Prefixing & Grouping

Shanks supports two styles for organizing routes - pilih yang sesuai preferensi:

#### Style 1: Direct Prefix (Recommended for generated code)

```python
from shanks import App

# Create router with prefix
router = App(prefix='/api/v1/posts')

@router.get('/')
def list_posts(req):
    return {'posts': []}

@router.get('/<id>')
def get_post(req, id):
    return {'post': {}}

@router.post('/')
def create_post(req):
    return {'created': True}

# Results in:
# GET  /api/v1/posts
# GET  /api/v1/posts/<id>
# POST /api/v1/posts
```

#### Style 2: Group Method (Gin-style)

```python
from shanks import App

app = App()

# Create route group
auth = app.group('api/v1/auth')

@auth.post('login')
def login(req):
    return {'token': '...'}

@auth.post('register')
def register(req):
    return {'user': {...}}

@auth.get('me')
def me(req):
    return {'user': req.user}

# Include group to main app
app.include(auth)

# Results in:
# POST /api/v1/auth/login
# POST /api/v1/auth/register
# GET  /api/v1/auth/me
```

Both styles work identically - use whichever you prefer!

#### With Middleware

```python
from internal.middleware.auth_middleware import jwt_auth_middleware

# Style 1: Direct prefix
router = App(prefix='/api/v1/admin')
router.use(jwt_auth_middleware)

@router.get('/users')
def get_users(req):
    user = req.user  # Authenticated user from middleware
    return {'users': []}

# Style 2: Group with middleware
app = App()
admin = app.group('api/v1/admin', jwt_auth_middleware)

@admin.get('users')
def get_users(req):
    user = req.user
    return {'users': []}

app.include(admin)
```

#### Multiple Routers

```python
# Style 1: Direct prefix (used by shanks generate)
auth_router = App(prefix='/api/v1/auth')
user_router = App(prefix='/api/v1/users')
post_router = App(prefix='/api/v1/posts')

# Register in internal/routes/__init__.py
urlpatterns = [*auth_router, *user_router, *post_router]

# Style 2: Group method
app = App()

auth = app.group('api/v1/auth')
users = app.group('api/v1/users')
posts = app.group('api/v1/posts')

# Define routes...
@auth.post('login')
def login(req): ...

@users.get('')
def list_users(req): ...

@posts.get('')
def list_posts(req): ...

# Include all
app.include(auth, users, posts)
```

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

- **GitHub**: https://github.com/Araryarch/shanks-django
- **PyPI**: https://pypi.org/project/shanks-django/
- **Issues**: https://github.com/Araryarch/shanks-django/issues
- **VSCode Extension**: https://marketplace.visualstudio.com/items?itemName=Ararya.shanks-django

---

Made with ❤️ by [Ararya](https://github.com/Araryarch)
