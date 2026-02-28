# finalapp

Shanks Django project

## Quick Start

```bash
cd finalapp
cp .env.example .env
sorm db push              # Setup database
shanks run                # Start server
```

## Available Commands

```bash
shanks run                # Start development server
shanks create <name> --crud  # Generate CRUD endpoint
sorm db push              # Apply database changes
sorm db pull              # Pull database schema
```

## Project Structure

```
finalapp/
├── internal/
│   ├── routes/           # API routes
│   ├── views/            # Template views (optional)
│   ├── controller/       # Request handlers
│   ├── service/          # Business logic
│   ├── repository/       # Data access
│   └── middleware/       # Custom middleware
├── db/
│   ├── entity/           # Django models
│   ├── migrations/       # Database migrations
│   └── seeds/            # Database seeders
├── dto/                  # Data transfer objects
├── templates/            # HTML templates
└── finalapp/       # Django config
```

## Template Rendering

Shanks supports Django-style template rendering:

```python
from shanks import render

@router.get('/')
def home(req):
    return render(req, 'index.html', {'title': 'Welcome'})
```
