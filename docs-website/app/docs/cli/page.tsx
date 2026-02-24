import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';

export default function CLIPage() {
  return (
    <div className="space-y-12">
      <div className="space-y-4">
        <h1 className="text-4xl font-bold tracking-tight">CLI Commands</h1>
        <p className="text-xl text-muted-foreground">
          Powerful command-line tools to speed up development. Generate CRUD, Auth, and more with one command.
        </p>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Create New Project</CardTitle>
          <CardDescription>
            Generate a new Shanks project with Go-like architecture.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <pre className="bg-background border border-border rounded-lg p-4 overflow-x-auto">
            <code className="text-sm">{`shanks new myproject
cd myproject
shanks run`}</code>
          </pre>
          <p className="text-sm text-muted-foreground mt-4">
            Creates project structure: internal/, entity/, dto/, config/, utils/
          </p>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Generate CRUD Endpoints</CardTitle>
          <CardDescription>
            Create complete CRUD with model, controller, and routes automatically.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <pre className="bg-background border border-border rounded-lg p-4 overflow-x-auto">
            <code className="text-sm">{`shanks create posts --crud`}</code>
          </pre>
          <div className="mt-4 space-y-3">
            <p className="text-sm text-muted-foreground">This generates:</p>
            <ul className="space-y-2 text-sm text-muted-foreground">
              <li className="flex items-start gap-2">
                <span className="text-primary">•</span>
                <span><code className="text-xs bg-muted px-1.5 py-0.5 rounded">entity/posts.py</code> - Model definition</span>
              </li>
              <li className="flex items-start gap-2">
                <span className="text-primary">•</span>
                <span><code className="text-xs bg-muted px-1.5 py-0.5 rounded">internal/controller/posts.py</code> - Business logic</span>
              </li>
              <li className="flex items-start gap-2">
                <span className="text-primary">•</span>
                <span><code className="text-xs bg-muted px-1.5 py-0.5 rounded">internal/routes/posts.py</code> - API endpoints</span>
              </li>
            </ul>
            <p className="text-sm text-muted-foreground mt-4">Includes:</p>
            <ul className="space-y-2 text-sm text-muted-foreground">
              <li className="flex items-start gap-2">
                <span className="text-primary">✓</span>
                <span>List with pagination (page, limit)</span>
              </li>
              <li className="flex items-start gap-2">
                <span className="text-primary">✓</span>
                <span>Get by ID</span>
              </li>
              <li className="flex items-start gap-2">
                <span className="text-primary">✓</span>
                <span>Create, Update, Delete</span>
              </li>
              <li className="flex items-start gap-2">
                <span className="text-primary">✓</span>
                <span>Auth checks</span>
              </li>
              <li className="flex items-start gap-2">
                <span className="text-primary">✓</span>
                <span>Error handling</span>
              </li>
            </ul>
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Generate Auth Endpoints</CardTitle>
          <CardDescription>
            Create authentication system with login, register, and more.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-6">
            <div>
              <h3 className="text-lg font-semibold mb-2">Simple Auth</h3>
              <pre className="bg-background border border-border rounded-lg p-3 overflow-x-auto">
                <code className="text-sm">{`shanks create auth --simple`}</code>
              </pre>
              <p className="text-sm text-muted-foreground mt-2">
                Generates: /login, /register, /me
              </p>
            </div>

            <div>
              <h3 className="text-lg font-semibold mb-2">Complete Auth</h3>
              <pre className="bg-background border border-border rounded-lg p-3 overflow-x-auto">
                <code className="text-sm">{`shanks create auth --complete`}</code>
              </pre>
              <p className="text-sm text-muted-foreground mt-2">
                Generates: /login, /register, /verify, /forgot-password, /reset-password, /me
              </p>
            </div>
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Development Server</CardTitle>
          <CardDescription>
            Run development server with auto-reload (like nodemon).
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <div>
              <pre className="bg-background border border-border rounded-lg p-3 overflow-x-auto">
                <code className="text-sm">{`shanks run                    # Default: 127.0.0.1:8000
shanks run 3000               # Custom port
shanks run 0.0.0.0:8000       # All interfaces`}</code>
              </pre>
            </div>
            <p className="text-sm text-muted-foreground">
              Automatically reloads when you save files. No need to restart manually!
            </p>
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Code Quality</CardTitle>
          <CardDescription>
            Format and lint your code with built-in tools.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <div>
              <h3 className="text-lg font-semibold mb-2">Format with Black</h3>
              <pre className="bg-background border border-border rounded-lg p-3 overflow-x-auto">
                <code className="text-sm">{`shanks format`}</code>
              </pre>
            </div>

            <div>
              <h3 className="text-lg font-semibold mb-2">Lint with Flake8</h3>
              <pre className="bg-background border border-border rounded-lg p-3 overflow-x-auto">
                <code className="text-sm">{`shanks lint`}</code>
              </pre>
            </div>

            <div>
              <h3 className="text-lg font-semibold mb-2">Format + Lint</h3>
              <pre className="bg-background border border-border rounded-lg p-3 overflow-x-auto">
                <code className="text-sm">{`shanks check`}</code>
              </pre>
            </div>
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Database Commands</CardTitle>
          <CardDescription>
            Manage database migrations and operations.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <pre className="bg-background border border-border rounded-lg p-4 overflow-x-auto">
            <code className="text-sm">{`# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Shell
python manage.py shell`}</code>
          </pre>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Complete Workflow</CardTitle>
          <CardDescription>
            From zero to production-ready API in minutes.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <pre className="bg-background border border-border rounded-lg p-4 overflow-x-auto">
            <code className="text-sm">{`# 1. Create project
shanks new blog
cd blog

# 2. Generate CRUD endpoints
shanks create posts --crud
shanks create comments --crud

# 3. Generate auth
shanks create auth --simple

# 4. Run migrations
python manage.py makemigrations
python manage.py migrate

# 5. Create admin user
python manage.py createsuperuser

# 6. Start server
shanks run

# 7. Visit API
# http://127.0.0.1:8000/api/posts
# http://127.0.0.1:8000/docs (Swagger)`}</code>
          </pre>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>All Commands</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-3">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
              <div className="space-y-1">
                <code className="text-sm bg-muted px-2 py-1 rounded">shanks new &lt;name&gt;</code>
                <p className="text-xs text-muted-foreground">Create new project</p>
              </div>
              <div className="space-y-1">
                <code className="text-sm bg-muted px-2 py-1 rounded">shanks create &lt;name&gt; --crud</code>
                <p className="text-xs text-muted-foreground">Generate CRUD</p>
              </div>
              <div className="space-y-1">
                <code className="text-sm bg-muted px-2 py-1 rounded">shanks create auth --simple</code>
                <p className="text-xs text-muted-foreground">Generate simple auth</p>
              </div>
              <div className="space-y-1">
                <code className="text-sm bg-muted px-2 py-1 rounded">shanks create auth --complete</code>
                <p className="text-xs text-muted-foreground">Generate complete auth</p>
              </div>
              <div className="space-y-1">
                <code className="text-sm bg-muted px-2 py-1 rounded">shanks run [port]</code>
                <p className="text-xs text-muted-foreground">Start dev server</p>
              </div>
              <div className="space-y-1">
                <code className="text-sm bg-muted px-2 py-1 rounded">shanks format</code>
                <p className="text-xs text-muted-foreground">Format with Black</p>
              </div>
              <div className="space-y-1">
                <code className="text-sm bg-muted px-2 py-1 rounded">shanks lint</code>
                <p className="text-xs text-muted-foreground">Lint with Flake8</p>
              </div>
              <div className="space-y-1">
                <code className="text-sm bg-muted px-2 py-1 rounded">shanks check</code>
                <p className="text-xs text-muted-foreground">Format + Lint</p>
              </div>
              <div className="space-y-1">
                <code className="text-sm bg-muted px-2 py-1 rounded">shanks help</code>
                <p className="text-xs text-muted-foreground">Show all commands</p>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
