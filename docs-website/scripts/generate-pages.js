const fs = require('fs');
const path = require('path');

const pages = [
  // CLI pages
  { path: 'cli/new', title: 'shanks new', desc: 'Create a new Shanks project' },
  { path: 'cli/create', title: 'shanks create', desc: 'Generate CRUD endpoints and authentication' },
  { path: 'cli/generate', title: 'shanks generate', desc: 'Generate Django structure for deployment' },
  { path: 'cli/run', title: 'shanks run', desc: 'Start the development server' },
  
  // SORM pages
  { path: 'sorm/database', title: 'Database Setup', desc: 'Configure and setup your database' },
  { path: 'sorm/migrations', title: 'Migrations', desc: 'Manage database migrations' },
  { path: 'sorm/admin', title: 'Admin Panel', desc: 'Django admin panel configuration' },
  
  // Routing pages
  { path: 'routing', title: 'Routing', desc: 'Express.js-like routing for Django' },
  { path: 'routing/basic', title: 'Basic Routes', desc: 'Define basic routes with decorators' },
  { path: 'routing/groups', title: 'Route Groups', desc: 'Group routes with common prefixes' },
  { path: 'routing/dynamic', title: 'Dynamic Routes', desc: 'Handle dynamic URL parameters' },
  { path: 'routing/methods', title: 'HTTP Methods', desc: 'Handle GET, POST, PUT, DELETE requests' },
  
  // Auth pages
  { path: 'authentication', title: 'Authentication', desc: 'User authentication and authorization' },
  { path: 'authentication/jwt', title: 'JWT Authentication', desc: 'JSON Web Token authentication' },
  { path: 'authentication/session', title: 'Session Authentication', desc: 'Django session-based auth' },
  { path: 'authentication/middleware', title: 'Auth Middleware', desc: 'Protect routes with middleware' },
  
  // Middleware pages
  { path: 'middleware', title: 'Middleware', desc: 'Express.js-style middleware' },
  { path: 'middleware/builtin', title: 'Built-in Middleware', desc: 'Auto-cache and smart invalidation' },
  { path: 'middleware/custom', title: 'Custom Middleware', desc: 'Create your own middleware' },
  { path: 'middleware/cors', title: 'CORS', desc: 'Cross-Origin Resource Sharing setup' },
  
  // Caching pages
  { path: 'caching', title: 'Caching', desc: 'Built-in caching for 10x performance' },
  { path: 'caching/auto', title: 'Auto Cache', desc: 'Automatic caching for GET requests' },
  { path: 'caching/manual', title: 'Manual Cache', desc: 'Manual cache control' },
  { path: 'caching/invalidation', title: 'Cache Invalidation', desc: 'Smart cache invalidation' },
  
  // ORM pages
  { path: 'orm', title: 'ORM', desc: 'Prisma-like ORM for Django' },
  { path: 'orm/models', title: 'Models', desc: 'Define database models' },
  { path: 'orm/queries', title: 'Queries', desc: 'Query your database' },
  { path: 'orm/relationships', title: 'Relationships', desc: 'Model relationships' },
  
  // Config pages
  { path: 'configuration', title: 'Configuration', desc: 'Configure your Shanks application' },
  { path: 'configuration/env', title: 'Environment Variables', desc: 'Manage environment variables' },
  { path: 'configuration/database', title: 'Database Configuration', desc: 'Configure database connections' },
  { path: 'configuration/settings', title: 'Settings', desc: 'Django settings configuration' },
  
  // Swagger
  { path: 'swagger', title: 'Swagger/OpenAPI', desc: 'Auto-generated API documentation' },
  
  // Deployment pages
  { path: 'deployment/generate', title: 'Generate Django', desc: 'Convert to standard Django structure' },
  { path: 'deployment/heroku', title: 'Deploy to Heroku', desc: 'Deploy your app to Heroku' },
  { path: 'deployment/railway', title: 'Deploy to Railway', desc: 'Deploy your app to Railway' },
  { path: 'deployment/docker', title: 'Docker Deployment', desc: 'Containerize your application' },
  
  // Examples
  { path: 'examples', title: 'Examples', desc: 'Real-world examples and tutorials' },
  { path: 'examples/blog', title: 'Blog API', desc: 'Build a complete blog API' },
  { path: 'examples/ecommerce', title: 'E-commerce API', desc: 'Build an e-commerce backend' },
  { path: 'examples/chat', title: 'Real-time Chat', desc: 'Build a real-time chat application' },
];

const template = (title, desc) => `import { DocPage, CodeBlock, Callout } from '@/components/DocPage';

export default function Page() {
  return (
    <DocPage
      title="${title}"
      description="${desc}"
    >
      <Callout type="info">
        This page is under construction. Check back soon for complete documentation.
      </Callout>

      <h2>Coming Soon</h2>
      <p>
        Detailed documentation for ${title} is being written. In the meantime, check out:
      </p>
      <ul>
        <li><a href="/docs/getting-started">Getting Started Guide</a></li>
        <li><a href="/docs/cli">CLI Reference</a></li>
        <li><a href="https://github.com/Araryarch/shanks-django">GitHub Repository</a></li>
      </ul>
    </DocPage>
  );
}
`;

pages.forEach(page => {
  const filePath = path.join(__dirname, '..', 'app', 'docs', page.path, 'page.tsx');
  const dir = path.dirname(filePath);
  
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
  }
  
  fs.writeFileSync(filePath, template(page.title, page.desc));
  console.log(`Created: ${page.path}/page.tsx`);
});

console.log(`\nGenerated ${pages.length} pages!`);
