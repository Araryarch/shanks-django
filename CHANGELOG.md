# Changelog

All notable changes to Shanks Django will be documented in this file.

## [0.4.0] - 2026-02-28

### Added
- **Flexible CRUD Generation**: Individual operation flags for granular control
  - `-c` flag for Create operation only
  - `-r` flag for Read operations (list + get by ID)
  - `-u` flag for Update operation only
  - `-d` flag for Delete operation only
  - `--crud` flag for full CRUD (same as default)
  - Default behavior (no flags) generates full CRUD
  - Mix and match flags: `shanks create orders -c -r` (only Create & Read)

- **JWT Authentication Flag**: `--auth` flag for protected endpoints
  - `shanks create posts --crud --auth` - Full CRUD with JWT required
  - `shanks create comments -c --auth` - Only Create with JWT required
  - Works with any combination of operation flags
  - Auto-generates JWT middleware in `internal/middleware/auth_middleware.py`
  - Middleware applied at route level with `router.use(jwt_auth_middleware)`
  - Controller checks `hasattr(req, 'user_id')` for authentication

- **Dual Routing Styles**: Support both prefix and group methods
  - Style 1: `App(prefix='/api/v1/posts')` - Direct prefix (used by generator)
  - Style 2: `app.group('api/v1/posts')` - Gin-style grouping
  - Both styles work identically, choose based on preference
  - `app.include()` method to combine multiple routers

### Changed
- **Project Structure**: Updated to layered architecture
  - `db/entity/` - Django models
  - `internal/repository/` - Data access layer
  - `internal/service/` - Business logic layer
  - `internal/controller/` - Request handlers
  - `internal/routes/` - API routes
  - Better separation of concerns

- **CRUD Generation**: Now generates 5 files instead of 2
  - Entity (model) with proper Django fields
  - Repository for database operations
  - Service for business logic
  - Controller for request/response handling
  - Routes with proper HTTP methods

- **Response Format**: Standardized with BaseDTO
  - All responses use `{"status": 200, "message": "...", "data": {...}, "pagination": {...}}`
  - Consistent error handling across all endpoints
  - Proper HTTP status codes

### Improved
- **Authentication**: JWT middleware properly sets `req.user` and `req.user_id`
  - Middleware validates token and attaches user to request
  - Controllers can access authenticated user via `req.user`
  - Clean separation between protected and public endpoints

- **Documentation**: Comprehensive README updates
  - Examples for all flag combinations
  - Both routing styles documented
  - Real-world use cases (blog, e-commerce, reviews, orders)
  - Clear explanations of when to use each flag

### Examples

```bash
# Default - Full CRUD
shanks create products

# Individual operations
shanks create orders -c -r          # Only Create & Read
shanks create reports -d            # Only Delete

# With authentication
shanks create reviews --crud --auth # Full CRUD, all protected
shanks create comments -c --auth    # Only Create with auth
shanks create posts -c -r --auth    # Create & Read with auth
```

### Technical Details
- Modified `shanks/cli/crud.py` to parse operation flags
- Updated `shanks/cli/crud_templates.py` to conditionally generate operations
- Fixed auto-registration logic in routes `__init__.py` to avoid duplicates
- Controller authentication check uses `hasattr(req, 'user_id')` pattern
- Middleware sets both `req.user` and `req.user_id` for flexibility

## [0.3.1] - 2026-02-27

### Fixed
- **Build Compatibility**: Fixed `pyproject.toml` license format for Python 3.8 compatibility
  - Changed from `license = "MIT"` to `license = {text = "MIT"}`
  - Resolves setuptools validation error in older Python versions
  - Ensures CI/CD passes on all supported Python versions (3.8-3.12)

## [0.3.0] - 2026-02-27

### Added
- **Template Rendering Support**: Django-style template rendering
  - New `render()` function for rendering HTML templates with context
  - New `render_string()` function for rendering templates to string
  - New `render_html()` function for rendering raw HTML with context
  - Auto-generated `templates/` folder in new projects
  - Beautiful landing page template (`index.html`) included by default
  - Full Django template engine integration

### Changed
- **Project Structure**: Renamed `routes/` to `views/` for Django best practice
  - `internal/routes/` → `internal/views/`
  - `*_route.py` → `*_view.py`
  - Better alignment with Django conventions
  - All CLI commands updated to use new structure

### Improved
- **Django Conversion**: Enhanced `shanks generate django` command
  - Properly converts `render()` imports to Django's `from django.shortcuts import render`
  - Handles template rendering in converted projects
  - Fixed URL pattern generation (no leading slash for root path)
  - Templates directory included in converted projects
  - Production-ready settings with template configuration

### Fixed
- **Template Configuration**: Fixed `get_templates()` to include project templates directory
  - Templates now properly discovered in `BASE_DIR/templates/`
  - Works seamlessly with both Shanks and converted Django projects

## [0.2.6] - 2026-02-26

### Added
- **Generate Django Command**: `shanks generate django`
  - Converts Shanks project to standard Django structure for deployment
  - Auto-generates `urls.py` from Shanks routes
  - Copies all apps, models, migrations, and database
  - Creates `requirements.txt` with production dependencies
  - Generates deployment README with Gunicorn, uWSGI, Docker examples
  - Ready for deployment to Heroku, Railway, PythonAnywhere, etc.

### Tested
- All generated Django projects pass `python manage.py check`
- Server runs successfully with generated structure
- All endpoints work correctly
- Deployment-ready structure validated

## [0.2.5] - 2026-02-26

### Added
- **JWT Authentication**: `shanks create auth --simple` command
  - Generates JWT-based authentication without email verification
  - No SMTP configuration required
  - Includes register, login, logout, me, and refresh token endpoints
  - Uses PyJWT for token generation and validation
  - Token expiration: 7 days
  - Stateless authentication with Bearer token

### Fixed
- **HTTP Method Routing**: Fixed critical issue where all HTTP methods (GET, POST, PUT, DELETE) were handled by GET handler
  - Root cause: Django `path()` creates one view per path, but Shanks was creating separate views for each method
  - Solution: Group routes by path and create combined views that check `request.method`
  - Impact: All CRUD operations now work correctly

- **Cache Invalidation**: Fixed smart cache invalidation not working
  - Issue: Cache keys were hashed, pattern matching couldn't find them
  - Solution: Added path-to-keys mapping in SimpleCache class
  - Cache now properly invalidates on POST/PUT/PATCH/DELETE operations
  - Auto-cache and smart invalidation work seamlessly together

### Improved
- **CLI**: Added `shanks create auth [--simple]` command
  - `--simple`: JWT auth without email verification (no SMTP)
  - Without flag: Complete auth with email verification (requires SMTP)
  - Auto-generates controller and routes files
  - Includes usage instructions and examples

- **Documentation**: 
  - Added `AUTH_TEST_RESULTS.md` with complete JWT auth documentation
  - Added `CRUD_TEST_RESULTS.md` with CRUD testing results
  - Updated help messages with auth command

### Technical Details
- Modified `shanks/app.py` to group routes by path and handle multiple HTTP methods
- Enhanced `shanks/cache.py` with path tracking for proper invalidation
- Added JWT token helpers in auth controller
- All tests passing on Windows with PowerShell

## [0.2.3] - 2026-02-25

### Fixed
- **Critical Bug**: Fixed `AttributeError: 'Request' object has no attribute 'GET'` when accessing `/docs` (Swagger UI)
  - Issue: `cache_key()` function was trying to access `request.GET` on Shanks Request wrapper instead of Django request
  - Solution: Added check to handle both Shanks Request wrapper (`request.django`) and direct Django request
  - Impact: Swagger documentation now works correctly with auto-caching enabled

### Technical Details
- Modified `shanks/cache.py` `cache_key()` function to detect request type
- Now properly accesses `request.django.GET` for Shanks Request wrappers
- Maintains backward compatibility with direct Django requests

## [0.2.2] - 2026-02-25

### Added
- **New Command**: `shanks generate django` - Generate full Django project structure
  - Creates `django_output/` directory with standard Django layout
  - Auto-generates `urls.py` from Shanks routes
  - Copies all models, migrations, and application code
  - Includes deployment README with Gunicorn/uWSGI/Docker examples
  - Useful for deployment to platforms requiring Django standard structure

### Documentation
- Added `GENERATE_DJANGO_EXAMPLE.md` with comprehensive usage guide
- Updated README with `shanks generate django` documentation
- Added deployment examples for Heroku, Railway, Docker

## [0.2.1] - 2026-02-25

### Added
- **Auto-urlpatterns**: No need to write `urlpatterns = app.get_urls()` anymore!
  - Uses Python's module-level `__getattr__` magic
  - Automatically exports `urlpatterns` when `App()` is instantiated
  - Cleaner code, less boilerplate

### Changed
- Updated all documentation to remove `urlpatterns = app.get_urls()`
- Updated CLI generators to use auto-urlpatterns
- Updated VSCode extension snippets
- Updated landing page template

### Documentation
- All examples now show auto-urlpatterns (with ✨ emoji)
- Updated README, docs website, and VSCode extension

## [0.2.0] - 2026-02-25

### Added
- **Auto-caching by default**: GET requests now cached automatically (10x faster!)
  - `App()` now has `enable_cache=True` by default
  - Auto-adds `auto_cache` and `smart_cache_invalidation` middlewares
  - Can be disabled with `app.disable_cache()`
  - Can be customized with `app.cache_config(ttl=600)`
- **Route grouping**: Gin-style route organization
  - `app.group('api/posts')` for cleaner route definitions
  - Groups inherit parent middlewares and cache settings
  - Supports nested grouping
- **Auto-type detection**: No need for `<int:id>` in URL parameters
  - Parameters ending with `_id` or named `id` auto-detected as integers
  - Other parameters auto-detected as strings
  - Still supports explicit types: `<slug:slug>`, `<uuid:uuid>`, etc.
- **SORM CLI**: Prisma-like database management
  - `sorm make` - Create migrations
  - `sorm db migrate` - Apply migrations
  - `sorm db push` - Create + apply in one command
  - `sorm db reset` - Reset database
  - `sorm db shell` - Database shell
  - `sorm studio` - Open admin panel
- **Separate SORM command**: Use `sorm` instead of `shanks sorm`

### Changed
- Updated CLI generators to use route grouping pattern
- Updated all examples to remove `<int:>` prefix
- Suppressed Django branding in terminal output
- Cleaner UX with "Shanks" branding

### Documentation
- Added `CACHING_GUIDE.md`
- Added `ROUTE_GROUPING_EXAMPLE.md`
- Added `GENERATED_CODE_EXAMPLE.md`
- Updated README with all new features

### Fixed
- Black formatting issues
- Test failures with auto-cache enabled

## [0.1.2] - 2026-02-24

### Initial Release
- Express.js-like routing syntax
- Prisma-like ORM (SORM)
- Swagger integration
- CLI generators for CRUD and Auth
- Go-like project architecture
- Request/Response wrappers
- Middleware support
- CORS support

---

## Version Format

We use [Semantic Versioning](https://semver.org/):
- MAJOR version for incompatible API changes
- MINOR version for new functionality (backward compatible)
- PATCH version for bug fixes (backward compatible)

## Categories

- **Added**: New features
- **Changed**: Changes in existing functionality
- **Deprecated**: Soon-to-be removed features
- **Removed**: Removed features
- **Fixed**: Bug fixes
- **Security**: Security fixes
