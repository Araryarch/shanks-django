# Shanks Django - VSCode Extension

Snippets and syntax highlighting for Shanks Django framework.

## Features

- 🚀 Code snippets for common Shanks patterns
- 📝 IntelliSense support
- 🎨 Syntax highlighting
- ⚡ Quick scaffolding

## Snippets

### Basic App

- `shanks-app` - Create a new Shanks app
- `shanks-get` - Create a GET route
- `shanks-post` - Create a POST route
- `shanks-put` - Create a PUT route
- `shanks-delete` - Create a DELETE route

### Middleware

- `shanks-middleware` - Create middleware
- `shanks-auth` - Create auth middleware

### CORS & Swagger

- `shanks-cors` - Enable CORS
- `shanks-swagger` - Enable Swagger UI
- `shanks-doc` - Add Swagger documentation

### Response

- `shanks-response` - Return Response object
- `shanks-cookie` - Return Response with cookie
- `shanks-redirect` - Redirect response

### Database

- `shanks-mongodb` - Setup MongoDB connection
- `shanks-redis` - Setup Redis connection
- `shanks-postgres` - Setup PostgreSQL database

### Complete

- `shanks-full` - Create full API with CORS and Swagger

## Usage

1. Install the extension
2. Open a Python file
3. Type a snippet prefix (e.g., `shanks-app`)
4. Press `Tab` to expand

## Examples

### Create a new app

Type `shanks-app` and press Tab:

```python
from shanks import App

app = App()

@app.get('api/hello')
def hello(req):
    return {'message': 'Hello World!'}

urlpatterns = app.get_urls()
```

### Add a POST route

Type `shanks-post` and press Tab:

```python
@app.post('api/users')
def create_user(req):
    data = req.body
    return {'created': True}
```

### Enable CORS

Type `shanks-cors` and press Tab:

```python
from shanks import CORS

CORS.enable(app,
    origins=['http://localhost:3000'],
    credentials=True
)
```

## Requirements

- VSCode 1.80.0 or higher
- Python extension for VSCode

## Installation

### From GitHub Releases (Recommended)

1. Download the latest `.vsix` file from [Releases](https://github.com/Ararya/shanks-django/releases)
2. Open VSCode
3. Go to Extensions (Ctrl+Shift+X / Cmd+Shift+X)
4. Click "..." menu → Install from VSIX
5. Select the downloaded file

Or via command line:
```bash
code --install-extension shanks-django-0.1.0.vsix
```

### From VSCode Marketplace (Coming Soon)

1. Open VSCode
2. Go to Extensions (Ctrl+Shift+X)
3. Search for "Shanks Django"
4. Click Install

### From VSIX

1. Download the `.vsix` file
2. Open VSCode
3. Go to Extensions
4. Click "..." menu
5. Select "Install from VSIX..."
6. Choose the downloaded file

## Contributing

Contributions are welcome! Please visit [GitHub](https://github.com/Ararya/shanks-django).

## Development

### Build VSIX locally

```bash
cd vscode-extension
npm install -g @vscode/vsce
vsce package
```

This will generate `shanks-django-x.x.x.vsix` file.

### GitHub Actions

The extension is automatically built and released via GitHub Actions:

- **Automatic Release**: Push a tag starting with `v` (e.g., `v0.1.0`)
- **Manual Build**: Go to Actions → "Build VSCode Extension (Manual)" → Run workflow

The VSIX file will be available in:
- Release assets (for tagged releases)
- Workflow artifacts (for manual builds)

## License

MIT
