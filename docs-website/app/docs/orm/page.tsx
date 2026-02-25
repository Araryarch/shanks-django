import { H1, H2, Lead, P, CodeBlock, Alert, H3, Grid, GridItem, Section } from '@/components/Typography'

export default function ORMPage() {
  return (
    <div>
      <H1>ORM</H1>
      <Lead>Define models with JSON-like syntax. Super simple, no Django complexity.</Lead>

      <Section>
        <H2>JSON-like Schema (New!)</H2>
        <P>Define models like JSON. No need to import field types:</P>
        <CodeBlock title="models/post.py">
          <span className="text-red-500">from</span> <span className="text-white">shanks</span> <span className="text-red-500">import</span> <span className="text-white">model</span>{'\n\n'}
          <span className="text-neutral-600">Post = model(</span><span className="text-neutral-400">"Post"</span><span className="text-neutral-500">,</span> <span className="text-neutral-500">{'{'}</span>{'\n'}
          {'    '}<span className="text-neutral-400">"title"</span><span className="text-neutral-500">:</span> <span className="text-neutral-400">"string"</span><span className="text-neutral-500">,</span>{'\n'}
          {'    '}<span className="text-neutral-400">"content"</span><span className="text-neutral-500">:</span> <span className="text-neutral-400">"text"</span><span className="text-neutral-500">,</span>{'\n'}
          {'    '}<span className="text-neutral-400">"published"</span><span className="text-neutral-500">:</span> <span className="text-neutral-400">"boolean"</span><span className="text-neutral-500">,</span>{'\n'}
          {'    '}<span className="text-neutral-400">"views"</span><span className="text-neutral-500">:</span> <span className="text-neutral-400">"integer"</span><span className="text-neutral-500">,</span>{'\n'}
          {'    '}<span className="text-neutral-400">"author"</span><span className="text-neutral-500">:</span> <span className="text-neutral-500">{'{'}</span><span className="text-neutral-400">"type"</span><span className="text-neutral-500">:</span> <span className="text-neutral-400">"relation"</span><span className="text-neutral-500">,</span> <span className="text-neutral-400">"model"</span><span className="text-neutral-500">:</span> <span className="text-neutral-400">"auth.User"</span><span className="text-neutral-500">{'}'}</span><span className="text-neutral-500">,</span>{'\n'}
          {'    '}<span className="text-neutral-400">"created_at"</span><span className="text-neutral-500">:</span> <span className="text-neutral-400">"datetime"</span>{'\n'}
          <span className="text-neutral-500">{'}'}</span><span className="text-neutral-600">)</span>
        </CodeBlock>
        <P>That's it! No CharField, TextField, or any Django imports needed.</P>
      </Section>

      <Section>
        <H2>Available Field Types</H2>
        <Grid>
          <GridItem title="string" description="Short text (max 255 chars)" />
          <GridItem title="text" description="Long text" />
          <GridItem title="integer" description="Whole numbers" />
          <GridItem title="float" description="Decimal numbers" />
          <GridItem title="boolean" description="True/False" />
          <GridItem title="date" description="Date only" />
          <GridItem title="datetime" description="Date and time" />
          <GridItem title="email" description="Email address" />
          <GridItem title="url" description="URL/Link" />
          <GridItem title="slug" description="URL-friendly text" />
          <GridItem title="json" description="JSON data" />
          <GridItem title="relation" description="Foreign key" />
        </Grid>
      </Section>

      <Section>
        <H2>Relations</H2>
        <CodeBlock>
          <span className="text-neutral-600">Comment = model(</span><span className="text-neutral-400">"Comment"</span><span className="text-neutral-500">,</span> <span className="text-neutral-500">{'{'}</span>{'\n'}
          {'    '}<span className="text-neutral-400">"content"</span><span className="text-neutral-500">:</span> <span className="text-neutral-400">"text"</span><span className="text-neutral-500">,</span>{'\n'}
          {'    '}<span className="text-neutral-400">"post"</span><span className="text-neutral-500">:</span> <span className="text-neutral-500">{'{'}</span>{'\n'}
          {'        '}<span className="text-neutral-400">"type"</span><span className="text-neutral-500">:</span> <span className="text-neutral-400">"relation"</span><span className="text-neutral-500">,</span>{'\n'}
          {'        '}<span className="text-neutral-400">"model"</span><span className="text-neutral-500">:</span> <span className="text-neutral-400">"Post"</span><span className="text-neutral-500">,</span>{'\n'}
          {'        '}<span className="text-neutral-400">"on_delete"</span><span className="text-neutral-500">:</span> <span className="text-neutral-400">"CASCADE"</span>{'\n'}
          {'    '}<span className="text-neutral-500">{'}'}</span><span className="text-neutral-500">,</span>{'\n'}
          {'    '}<span className="text-neutral-400">"tags"</span><span className="text-neutral-500">:</span> <span className="text-neutral-500">{'{'}</span><span className="text-neutral-400">"type"</span><span className="text-neutral-500">:</span> <span className="text-neutral-400">"many"</span><span className="text-neutral-500">,</span> <span className="text-neutral-400">"model"</span><span className="text-neutral-500">:</span> <span className="text-neutral-400">"Tag"</span><span className="text-neutral-500">{'}'}</span>{'\n'}
          <span className="text-neutral-500">{'}'}</span><span className="text-neutral-600">)</span>
        </CodeBlock>
      </Section>

      <Section>
        <H2>Find Operations</H2>
        <CodeBlock>
          <span className="text-neutral-600"># Find all</span>{'\n'}
          <span className="text-neutral-600">posts = Post.find_many()</span>{'\n\n'}
          <span className="text-neutral-600"># Find with filter</span>{'\n'}
          <span className="text-neutral-600">published = Post.find_many(published=</span><span className="text-neutral-400">True</span><span className="text-neutral-600">)</span>{'\n\n'}
          <span className="text-neutral-600"># Find unique</span>{'\n'}
          <span className="text-neutral-600">post = Post.find_unique(id=</span><span className="text-neutral-400">1</span><span className="text-neutral-600">)</span>{'\n\n'}
          <span className="text-neutral-600"># Find first</span>{'\n'}
          <span className="text-neutral-600">post = Post.find_first(published=</span><span className="text-neutral-400">True</span><span className="text-neutral-600">)</span>{'\n\n'}
          <span className="text-neutral-600"># Count</span>{'\n'}
          <span className="text-neutral-600">total = Post.count()</span>{'\n'}
          <span className="text-neutral-600">published_count = Post.count(published=</span><span className="text-neutral-400">True</span><span className="text-neutral-600">)</span>
        </CodeBlock>
      </Section>

      <Section>
        <H2>Create & Update</H2>
        <CodeBlock>
          <span className="text-neutral-600"># Create</span>{'\n'}
          <span className="text-neutral-600">post = Post.create(</span>{'\n'}
          {'    '}<span className="text-neutral-600">title=</span><span className="text-neutral-400">"Hello World"</span><span className="text-neutral-500">,</span>{'\n'}
          {'    '}<span className="text-neutral-600">content=</span><span className="text-neutral-400">"My first post"</span><span className="text-neutral-500">,</span>{'\n'}
          {'    '}<span className="text-neutral-600">published=</span><span className="text-neutral-400">True</span>{'\n'}
          <span className="text-neutral-600">)</span>{'\n\n'}
          <span className="text-neutral-600"># Update</span>{'\n'}
          <span className="text-neutral-600">post.update_self(title=</span><span className="text-neutral-400">"Updated Title"</span><span className="text-neutral-600">)</span>{'\n\n'}
          <span className="text-neutral-600"># Delete</span>{'\n'}
          <span className="text-neutral-600">post.delete_self()</span>
        </CodeBlock>
      </Section>

      <Section>
        <H2>Complete Example</H2>
        <CodeBlock>
          <span className="text-red-500">from</span> <span className="text-white">shanks</span> <span className="text-red-500">import</span> <span className="text-white">App</span><span className="text-neutral-500">,</span> <span className="text-white">model</span>{'\n\n'}
          <span className="text-neutral-600"># Define model with JSON</span>{'\n'}
          <span className="text-neutral-600">Post = model(</span><span className="text-neutral-400">"Post"</span><span className="text-neutral-500">,</span> <span className="text-neutral-500">{'{'}</span>{'\n'}
          {'    '}<span className="text-neutral-400">"title"</span><span className="text-neutral-500">:</span> <span className="text-neutral-400">"string"</span><span className="text-neutral-500">,</span>{'\n'}
          {'    '}<span className="text-neutral-400">"content"</span><span className="text-neutral-500">:</span> <span className="text-neutral-400">"text"</span><span className="text-neutral-500">,</span>{'\n'}
          {'    '}<span className="text-neutral-400">"views"</span><span className="text-neutral-500">:</span> <span className="text-neutral-400">"integer"</span>{'\n'}
          <span className="text-neutral-500">{'}'}</span><span className="text-neutral-600">)</span>{'\n\n'}
          <span className="text-neutral-600">app = App()</span>{'\n\n'}
          <span className="text-red-500">@app.get</span><span className="text-neutral-500">(</span><span className="text-neutral-400">"api/posts"</span><span className="text-neutral-500">)</span>{'\n'}
          <span className="text-red-500">def</span> <span className="text-white">list_posts</span><span className="text-neutral-500">(</span><span className="text-neutral-600">req</span><span className="text-neutral-500">)</span><span className="text-neutral-500">:</span>{'\n'}
          {'    '}<span className="text-neutral-600">posts = Post.find_many()</span>{'\n'}
          {'    '}<span className="text-red-500">return</span> <span className="text-neutral-500">{'{'}</span><span className="text-neutral-400">"posts"</span><span className="text-neutral-500">:</span> <span className="text-neutral-500">[</span><span className="text-neutral-500">{'{'}</span><span className="text-neutral-400">"id"</span><span className="text-neutral-500">:</span> <span className="text-neutral-600">p.id</span><span className="text-neutral-500">,</span> <span className="text-neutral-400">"title"</span><span className="text-neutral-500">:</span> <span className="text-neutral-600">p.title</span><span className="text-neutral-500">{'}'}</span> <span className="text-red-500">for</span> <span className="text-neutral-600">p</span> <span className="text-red-500">in</span> <span className="text-neutral-600">posts</span><span className="text-neutral-500">]</span><span className="text-neutral-500">{'}'}</span>{'\n\n'}
          <span className="text-red-500">@app.post</span><span className="text-neutral-500">(</span><span className="text-neutral-400">"api/posts"</span><span className="text-neutral-500">)</span>{'\n'}
          <span className="text-red-500">def</span> <span className="text-white">create_post</span><span className="text-neutral-500">(</span><span className="text-neutral-600">req</span><span className="text-neutral-500">)</span><span className="text-neutral-500">:</span>{'\n'}
          {'    '}<span className="text-neutral-600">post = Post.create(**req.body)</span>{'\n'}
          {'    '}<span className="text-red-500">return</span> <span className="text-neutral-500">{'{'}</span><span className="text-neutral-400">"id"</span><span className="text-neutral-500">:</span> <span className="text-neutral-600">post.id</span><span className="text-neutral-500">{'}'}</span>
        </CodeBlock>
      </Section>

      <Alert type="success">
        <H3>Why JSON-like?</H3>
        <P>
          No need to remember Django field types. Just use simple strings like "string", "text", "integer".
          It's intuitive and easy to read.
        </P>
        <P>
          You can still use the old Django way if you prefer. Both syntaxes work together.
        </P>
      </Alert>

      <Section>
        <H2>SORM CLI Commands</H2>
        <P>
          Manage your database with Prisma-like commands. SORM (Shanks ORM) provides a simple CLI for migrations.
        </P>
        
        <div className="space-y-6 mt-6">
          <div>
            <H3>Create Migrations</H3>
            <CodeBlock>
              <span className="text-neutral-600">sorm make</span>
            </CodeBlock>
            <P className="text-sm text-muted-foreground mt-2">
              Like <code className="text-xs bg-muted px-1 py-0.5 rounded">prisma migrate dev --create-only</code>
            </P>
          </div>

          <div>
            <H3>Apply Migrations</H3>
            <CodeBlock>
              <span className="text-neutral-600">sorm db migrate</span>
            </CodeBlock>
            <P className="text-sm text-muted-foreground mt-2">
              Like <code className="text-xs bg-muted px-1 py-0.5 rounded">prisma migrate deploy</code>
            </P>
          </div>

          <div>
            <H3>Push to Database (Recommended)</H3>
            <CodeBlock>
              <span className="text-neutral-600">sorm db push</span>
            </CodeBlock>
            <P className="text-sm text-muted-foreground mt-2">
              Like <code className="text-xs bg-muted px-1 py-0.5 rounded">prisma db push</code> - Creates and applies migrations in one command
            </P>
          </div>

          <div>
            <H3>Reset Database</H3>
            <CodeBlock>
              <span className="text-neutral-600">sorm db reset</span>
            </CodeBlock>
            <P className="text-sm text-muted-foreground mt-2">
              Flush all data from database (requires confirmation)
            </P>
          </div>

          <div>
            <H3>Database Shell</H3>
            <CodeBlock>
              <span className="text-neutral-600">sorm db shell</span>
            </CodeBlock>
            <P className="text-sm text-muted-foreground mt-2">
              Open interactive database shell
            </P>
          </div>

          <div>
            <H3>Studio (Admin Panel)</H3>
            <CodeBlock>
              <span className="text-neutral-600">sorm studio</span>
            </CodeBlock>
            <P className="text-sm text-muted-foreground mt-2">
              Like <code className="text-xs bg-muted px-1 py-0.5 rounded">prisma studio</code> - Opens Django Admin at /admin
            </P>
          </div>
        </div>
      </Section>

      <Section>
        <H2>Typical Workflow</H2>
        <CodeBlock>
          <span className="text-neutral-600"># 1. Define your models</span>{'\n'}
          <span className="text-neutral-600"># entity/post.py</span>{'\n\n'}
          <span className="text-neutral-600"># 2. Push to database</span>{'\n'}
          <span className="text-neutral-600">sorm db push</span>{'\n\n'}
          <span className="text-neutral-600"># 3. Open admin panel</span>{'\n'}
          <span className="text-neutral-600">sorm studio</span>{'\n\n'}
          <span className="text-neutral-600"># 4. Start coding!</span>{'\n'}
          <span className="text-neutral-600">shanks run</span>
        </CodeBlock>
      </Section>
    </div>
  )
}
