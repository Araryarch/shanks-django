# Change Log

## [0.1.3] - 2024-02-24

### Added
- 🎨 **Syntax highlighting** for Shanks and SORM keywords
- 🌈 **Shanks Dark theme** - Custom color theme with red accents
- Highlight for decorators: `@app.get()`, `@app.post()`, etc.
- Highlight for SORM: `table()`, `Model`, field types, query methods
- Highlight for Shanks classes: `App`, `Response`, `CORS`, `SwaggerUI`
- Language configuration for better Python editing
- `sorm-table` - Super simple JSON-like table syntax
- Updated `sorm-model` to use `table()` function

### Changed
- SORM now uses `table()` for JSON-like model definition
- Syntax: `"string:100:unique"` instead of `CharField(max_length=100, unique=True)`
- Much simpler and cleaner model definitions

## [0.1.2] - 2024-02-24

### Added
- SORM (Shanks ORM) snippets for cleaner imports
- `sorm-model` - Create model with SORM imports
- `sorm-user` - Use SORM User model
- Updated all model snippets to use SORM instead of shanks imports

### Changed
- `shanks-model` now uses SORM imports
- `shanks-user-create` now uses SORM imports
- `shanks-authenticate` now uses SORM imports

## [0.1.1] - 2024-02-24

### Added
- JSON-like model syntax snippet (`shanks-json-model`)
- Simplified settings.py template (`shanks-settings`)
- Route grouping snippet (`shanks-group`)
- Include routers snippet (`shanks-include`)
- Environment variables helpers (`shanks-env`)
- Minimal WSGI configuration (`shanks-wsgi`)

### Changed
- Updated snippets to reflect no urls.py requirement
- Simplified configuration approach

## [0.1.0] - 2024-02-23

### Added
- Initial release
- Code snippets for Shanks Django
- Support for routes (GET, POST, PUT, DELETE)
- Middleware snippets
- CORS configuration snippets
- Swagger/OpenAPI documentation snippets
- Database connection snippets (MongoDB, Redis, PostgreSQL)
- Response helpers
- Full API template
