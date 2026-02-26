# Shanks Documentation Website Structure

## Overview
Complete documentation website built with Next.js 16, TypeScript, and Tailwind CSS.

## Structure

```
docs-website/
├── app/
│   ├── docs/
│   │   ├── getting-started/     # Getting started guide
│   │   ├── installation/        # Installation instructions
│   │   ├── cli/                 # CLI reference
│   │   │   ├── new/            # shanks new command
│   │   │   ├── create/         # shanks create command
│   │   │   ├── generate/       # shanks generate command
│   │   │   └── run/            # shanks run command
│   │   ├── sorm/                # SORM documentation
│   │   │   ├── database/       # Database setup
│   │   │   ├── migrations/     # Migrations guide
│   │   │   └── admin/          # Admin panel
│   │   ├── routing/             # Routing documentation
│   │   │   ├── basic/          # Basic routes
│   │   │   ├── groups/         # Route groups
│   │   │   ├── dynamic/        # Dynamic routes
│   │   │   └── methods/        # HTTP methods
│   │   ├── authentication/      # Auth documentation
│   │   │   ├── jwt/            # JWT authentication
│   │   │   ├── session/        # Session auth
│   │   │   └── middleware/     # Auth middleware
│   │   ├── middleware/          # Middleware docs
│   │   │   ├── builtin/        # Built-in middleware
│   │   │   ├── custom/         # Custom middleware
│   │   │   └── cors/           # CORS setup
│   │   ├── caching/             # Caching documentation
│   │   │   ├── auto/           # Auto cache
│   │   │   ├── manual/         # Manual cache
│   │   │   └── invalidation/   # Cache invalidation
│   │   ├── orm/                 # ORM documentation
│   │   │   ├── models/         # Model definition
│   │   │   ├── queries/        # Querying data
│   │   │   └── relationships/  # Model relationships
│   │   ├── configuration/       # Configuration docs
│   │   │   ├── env/            # Environment variables
│   │   │   ├── database/       # Database config
│   │   │   └── settings/       # Settings
│   │   ├── swagger/             # Swagger/OpenAPI docs
│   │   ├── deployment/          # Deployment guides
│   │   │   ├── generate/       # Generate Django
│   │   │   ├── heroku/         # Heroku deployment
│   │   │   ├── railway/        # Railway deployment
│   │   │   └── docker/         # Docker deployment
│   │   ├── examples/            # Examples
│   │   │   ├── blog/           # Blog API example
│   │   │   ├── ecommerce/      # E-commerce example
│   │   │   └── chat/           # Real-time chat
│   │   ├── layout.tsx          # Docs layout with sidebar
│   │   └── page.tsx            # Docs homepage
│   ├── layout.tsx              # Root layout
│   ├── page.tsx                # Homepage
│   └── globals.css             # Global styles
├── components/
│   ├── Sidebar.tsx             # Navigation sidebar
│   ├── CodeBlock.tsx           # Code block with copy
│   ├── Callout.tsx             # Info/warning/error boxes
│   ├── Typography.tsx          # Typography components
│   └── ui/                     # UI components
│       ├── button.tsx
│       ├── card.tsx
│       └── separator.tsx
└── public/                     # Static assets

## Features

### Components

#### Sidebar
- Hierarchical navigation
- Active state highlighting
- Collapsible sections
- Mobile responsive

#### CodeBlock
- Syntax highlighting
- Copy to clipboard
- Language support
- Filename display

#### Callout
- Info, warning, error, success types
- Icons
- Custom titles
- Dark mode support

### Pages Created

✅ Homepage (`/docs`)
✅ Getting Started (`/docs/getting-started`)
✅ CLI Reference (`/docs/cli`)
✅ SORM Documentation (`/docs/sorm`)
✅ Deployment Guide (`/docs/deployment`)

### Pages To Create

- [ ] Installation details
- [ ] Routing guides (basic, groups, dynamic, methods)
- [ ] Authentication guides (JWT, session, middleware)
- [ ] Middleware documentation
- [ ] Caching guides
- [ ] ORM documentation
- [ ] Configuration guides
- [ ] Swagger/OpenAPI docs
- [ ] Deployment platform guides
- [ ] Examples (blog, ecommerce, chat)

## Development

```bash
cd docs-website
npm install
npm run dev
```

Visit: http://localhost:3000/docs

## Build

```bash
npm run build
npm start
```

## Styling

- Tailwind CSS 4
- Dark mode support
- Responsive design
- Next.js docs-inspired design

## Next Steps

1. Complete all documentation pages
2. Add search functionality
3. Add code syntax highlighting (Prism.js or Shiki)
4. Add table of contents for long pages
5. Add "Edit on GitHub" links
6. Add version selector
7. Add API reference
8. Add interactive examples
9. Add video tutorials
10. Add community section

## Notes

- All pages use TypeScript
- Components are client-side (`'use client'`)
- Prose styling for markdown-like content
- Lucide React for icons
- Responsive and accessible
