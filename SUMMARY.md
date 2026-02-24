# Shanks Django - Complete Summary

## 🎯 What is Shanks?

Shanks is a modern Django framework that brings Express.js-like routing and Prisma-like ORM to Django, with built-in caching for 10x performance boost.

## ✨ Key Features

### 1. Built-in Caching (NEW!)
- Auto-cache GET requests (5 min TTL)
- Smart cache invalidation on writes
- 10x faster responses (~50ms → ~5ms)
- Zero configuration needed

### 2. Express.js-like Routing
- No urls.py needed
- Clean decorator syntax: `@app.get()`, `@app.post()`
- Route grouping with `app.group()`
- Middleware support: `def middleware(req, res, next)`

### 3. Prisma-like ORM
- `find_many()` - Find multiple records
- `find_unique()` - Find single record
- `create()` - Create record
- `update_self()` - Update instance
- `delete_self()` - Delete instance
- `count()` - Count records

### 4. CLI Generator
- `shanks new <project>` - Create project with Go-like architecture
- `shanks create <endpoint> --crud` - Generate full CRUD
- `shanks create auth --simple|--complete` - Generate auth
- `shanks run` - Development server with auto-reload

### 5. Go-like Architecture
```
project/
├── internal/       # Internal code
│   ├── controller/ # HTTP handlers
│   ├── repository/ # Data access
│   ├── service/    # Business logic
│   ├── middleware/ # Middleware
│   └── routes/     # Routes
├── entity/         # Models
├── dto/            # DTOs
├── config/         # Config
└── utils/          # Utils
```

### 6. Auto-generated Swagger
- Interactive API docs at `/docs`
- Zero configuration: `app.use(swagger())`
- Applies to all endpoints

### 7. Configuration Helpers
- Simplified settings.py (48 lines vs 77)
- Simplified wsgi.py (6 lines)
- Environment variable support

## 🚀 Quick Start

```bash
# Install
pip install shanks-django

# Create project
shanks new myproject
cd myproject

# Generate CRUD
shanks create posts --crud

# Generate Auth
shanks create auth --simple

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Start server
shanks run
```

Visit:
- API: http://127.0.0.1:8000/api/health
- Swagger: http://127.0.0.1:8000/docs

## 💡 Code Example

```python
# internal/routes/__init__.py
from shanks import App, auto_cache, smart_cache_invalidation, swagger

app = App()

# Built-in caching - 10x faster!
app.use(auto_cache)
app.use(smart_cache_invalidation)

# Auto Swagger docs
app.use(swagger(title="My API"))

@app.get('api/posts')
def list_posts(req):
    # Automatically cached!
    return {'posts': Post.find_many()}

@app.post('api/posts')
def create_post(req):
    # Automatically invalidates cache!
    post = Post.create(**req.body)
    return {'id': post.id}

urlpatterns = app.get_urls()
```

## 📊 Performance

| Metric | Without Cache | With Cache | Speedup |
|--------|--------------|------------|---------|
| Response Time | ~50ms | ~5ms | 10x |
| Database Queries | Every request | First request only | - |
| Memory Usage | Low | Low (TTL-based) | - |

## 🎨 Generated CRUD Includes

- ✅ List with pagination (page, limit)
- ✅ Get by ID (findById)
- ✅ Create with auth check
- ✅ Update with auth check
- ✅ Delete with auth check
- ✅ Error handling
- ✅ Prisma-like methods

## 🔐 Generated Auth Includes

**Simple** (`--simple`):
- POST /api/auth/register
- POST /api/auth/login
- GET /api/auth/me

**Complete** (`--complete`):
- POST /api/auth/register
- POST /api/auth/login
- POST /api/auth/verify
- GET /api/auth/me

## 🛠️ CLI Commands

```bash
# Development
shanks run                    # Start server
shanks run 3000               # Custom port
shanks run 0.0.0.0:8000      # All interfaces

# Project
shanks new myproject          # Create project

# Generate
shanks create posts --crud    # CRUD endpoints
shanks create auth --simple   # Auth endpoints

# Code Quality
shanks format                 # Black formatting
shanks lint                   # Flake8 linting
shanks check                  # Format + Lint

# Help
shanks help                   # Show commands
```

## 📚 Documentation

- **README.md** - Main documentation
- **FEATURES_COMPLETE.md** - Complete feature list
- **RELEASE_NOTES.md** - Version history
- **CACHE_DEMO.md** - Caching examples (in projects)
- **docs-website/** - Next.js documentation site

## 🎯 Use Cases

Perfect for:
- REST APIs
- Microservices
- Backend for mobile apps
- Backend for web apps
- Rapid prototyping
- Production applications

## 🌟 Why Choose Shanks?

1. **Familiar Syntax** - Express.js routing, Prisma-like ORM
2. **Built-in Performance** - 10x faster with auto-caching
3. **Zero Config** - Works out of the box
4. **Clean Architecture** - Go-like project structure
5. **Fast Development** - CLI generators, auto-reload
6. **Production Ready** - Built on Django, battle-tested
7. **Full Stack** - Swagger, CORS, Auth included

## 📦 Installation Options

```bash
# Basic
pip install shanks-django

# With PostgreSQL
pip install shanks-django[postgres]

# With MySQL
pip install shanks-django[mysql]

# With MongoDB
pip install shanks-django[mongodb]

# With Redis
pip install shanks-django[redis]

# All databases
pip install shanks-django[all]
```

## 🔧 Configuration

Everything is configurable with sensible defaults:
- Cache TTL (default: 5 minutes)
- Database (default: SQLite)
- Debug mode (default: True in dev)
- Allowed hosts (default: *)
- Middleware stack (default: Django + Shanks)

## 🎁 Extras

- **VSCode Extension** - Syntax highlighting, snippets, theme
- **GitHub Actions** - Auto-build and release
- **Example Project** - Complete working example
- **Documentation Website** - Next.js site with dark theme

## 📄 License

MIT License - Free for commercial use

## 🙏 Credits

Built with ❤️ by Ararya

## 🔗 Links

- PyPI: https://pypi.org/project/shanks-django/
- GitHub: https://github.com/Ararya/shanks-django
- Documentation: See docs-website/

## 🚀 Get Started Now!

```bash
pip install shanks-django
shanks new myproject
cd myproject
shanks run
```

That's it! You're ready to build fast, modern Django APIs! 🎉
