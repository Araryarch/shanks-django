# Shanks Documentation Website

Modern documentation website built with Next.js 16, TypeScript, and Tailwind CSS.

## Features

- 📚 Complete documentation for Shanks Django
- 🎨 Next.js docs-inspired design
- 🌙 Dark mode support
- 📱 Fully responsive
- 🔍 Easy navigation with sidebar
- 💻 Code blocks with copy functionality
- ⚡ Fast and optimized

## Getting Started

### Prerequisites

- Node.js 18+ 
- npm or yarn

### Installation

```bash
cd docs-website
npm install
```

### Development

```bash
npm run dev
```

Visit [http://localhost:3000](http://localhost:3000)

### Build

```bash
npm run build
npm start
```

## Structure

```
docs-website/
├── app/
│   ├── docs/              # Documentation pages
│   │   ├── getting-started/
│   │   ├── cli/
│   │   ├── sorm/
│   │   ├── deployment/
│   │   └── ...
│   ├── layout.tsx         # Root layout
│   └── page.tsx           # Homepage
├── components/
│   ├── Sidebar.tsx        # Navigation sidebar
│   ├── CodeBlock.tsx      # Code block with copy
│   ├── Callout.tsx        # Info/warning boxes
│   └── ui/                # UI components
├── lib/
│   └── utils.ts           # Utility functions
└── public/                # Static assets
```

## Documentation Pages

### Completed ✅
- Homepage (`/`)
- Docs homepage (`/docs`)
- Getting Started (`/docs/getting-started`)
- CLI Reference (`/docs/cli`)
- SORM (`/docs/sorm`)
- Deployment (`/docs/deployment`)

### To Be Added
- Installation details
- Routing guides
- Authentication guides
- Middleware documentation
- Caching guides
- ORM documentation
- Configuration guides
- Swagger/OpenAPI docs
- Platform-specific deployment guides
- Real-world examples

## Components

### Sidebar
Hierarchical navigation with:
- Active state highlighting
- Collapsible sections
- 13 main sections
- Mobile responsive

### CodeBlock
Code display with:
- Copy to clipboard
- Syntax highlighting support
- Filename display
- Dark mode support

### Callout
Info boxes with:
- 4 types: info, warning, error, success
- Icons
- Custom titles
- Dark mode support

## Styling

- Tailwind CSS 4
- Dark mode with `dark:` prefix
- Responsive design
- Accessible components

## Tech Stack

- **Framework**: Next.js 16
- **Language**: TypeScript
- **Styling**: Tailwind CSS 4
- **Icons**: Lucide React
- **UI Components**: Radix UI

## Contributing

1. Add new documentation pages in `app/docs/`
2. Update sidebar navigation in `components/Sidebar.tsx`
3. Use existing components (CodeBlock, Callout) for consistency
4. Follow the existing page structure

## License

MIT
