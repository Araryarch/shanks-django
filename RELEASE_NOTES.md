# Shanks Django - Release Notes

## Version 0.1.5 - Built-in Caching Release

### 🎉 Major Features

#### 1. Built-in Caching System
- **Auto-cache GET requests** - Enabled by default, 5-minute TTL
- **Smart cache invalidation** - Automatically clears cache on POST/PUT/DELETE
- **10x performance boost** - Response times drop from ~50ms to ~5ms
- **Zero configuration** - Works out of the box
- **Custom TTL support** - `@cache(ttl=600)` decorator for per-endpoint control
- **Manual cache control** - `invalidate_cache()`, `get_cache()` for advanced use cases
- **Pattern-based invalidation** - Clear cache by URL pattern

#### 2. Go-like Project Architecture
- **Clean structure** - internal/, entity/, dto/, config/, utils/
- **Separation of concerns** - controller, repository, service layers
- **Auto-generated** - `shanks new` creates complete structure

#### 3. CLI Generator Enhancements
- **CRUD generation** - `shanks create posts --crud` creates model, controller, routes
- **Auth generation** - `shanks create auth --simple|--complete`
- **Pagination built-in** - All generated CRUD includes pagination
- **findById support** - Get single record by ID
- **Auth checks** - Generated endpoints include authentication

#### 4. Express.js-style Middleware
- **req, res, next pattern** - Familiar for Node.js developers
- **Middleware chain** - Multiple middleware support
- **Built-in middleware** - auto_cache, smart_cache_invalidation, swagger

### 📚 Documentation Updates

- **README.md** - Comprehensive guide with caching examples
- **FEATURES_COMPLETE.md** - Complete feature list
- **CACHE_DEMO.md** - Generated in new projects with caching examples
- **docs-website** - New caching documentation page

### 🏗️ Project Structure

New projects now include:
```
myproject/
├── internal/
│   ├── controller/    # HTTP handlers
│   ├── repository/    # Data access
│   ├── service/       # Business logic
│   ├── middleware/    # Middleware
│   └── routes/        # Routes (with caching enabled)
├── entity/            # Models
├── dto/               # DTOs
├── config/            # Config
└── utils/             # Utils
```

### 🚀 Performance

- **Without cache**: ~50ms response time
- **With cache**: ~5ms response time
- **Speedup**: 10x faster for cached requests
- **Memory efficient**: TTL-based expiration
- **Smart invalidation**: Auto-clear on writes

### 🎯 Breaking Changes

None! Fully backward compatible.

### 📦 New Dependencies

None! Uses only Python standard library for caching.

### 🔧 Configuration

All features work with sensible defaults:
- Cache TTL: 5 minutes (configurable)
- Auto-cache: Enabled in new projects
- Smart invalidation: Enabled in new projects

### 🐛 Bug Fixes

- Fixed circular import issues with SORM
- Fixed Django model registration
- Improved CLI error messages
- Fixed manage.py warnings

### 📝 Migration Guide

For existing projects, add caching:

```python
# internal/routes/__init__.py
from shanks import auto_cache, smart_cache_invalidation

app.use(auto_cache)
app.use(smart_cache_invalidation)
```

### 🎨 Code Quality

- All code formatted with Black
- Flake8 linting passed
- Type hints added where applicable
- Comprehensive docstrings

### 🌟 Highlights

1. **Zero-config caching** - Just works out of the box
2. **10x performance** - Instant speed boost
3. **Smart invalidation** - No manual cache management
4. **Clean architecture** - Go-like project structure
5. **CLI generators** - CRUD & Auth in seconds

### 📖 Documentation

- Main docs: README.md
- Caching guide: CACHE_DEMO.md (in generated projects)
- Complete features: FEATURES_COMPLETE.md
- Website: docs-website/ (Next.js)

### 🔮 Future Plans

- Redis cache backend option
- Rate limiting middleware
- WebSocket support
- GraphQL integration
- Admin panel generator

### 🙏 Credits

Built with ❤️ by Ararya

### 📄 License

MIT License - See LICENSE file

---

## Installation

```bash
pip install shanks-django
```

## Quick Start

```bash
shanks new myproject
cd myproject
shanks create posts --crud
python manage.py makemigrations
python manage.py migrate
shanks run
```

Visit http://127.0.0.1:8000/docs for Swagger UI!
