import { H1, H2, Lead, P, CodeBlock, Alert, H3, Section } from '@/components/Typography'

export default function RoutingPage() {
  return (
    <div>
      <H1>Routing</H1>
      <Lead>Express.js-like routing with grouping support. No more Django urls.py complexity.</Lead>

      <Section>
        <H2>Basic Routes</H2>
        <CodeBlock title="routes.py">
          <span className="text-red-500">from</span> <span className="text-white">shanks</span> <span className="text-red-500">import</span> <span className="text-white">App</span>{'\n\n'}
          <span className="text-neutral-600">app = App()</span>{'\n\n'}
          <span className="text-red-500">@app.get</span><span className="text-neutral-500">(</span><span className="text-neutral-400">"api/posts"</span><span className="text-neutral-500">)</span>{'\n'}
          <span className="text-red-500">def</span> <span className="text-white">list_posts</span><span className="text-neutral-500">(</span><span className="text-neutral-600">req</span><span className="text-neutral-500">)</span><span className="text-neutral-500">:</span>{'\n'}
          {'    '}<span className="text-red-500">return</span> <span className="text-neutral-500">{'{'}</span><span className="text-neutral-400">"posts"</span><span className="text-neutral-500">:</span> <span className="text-neutral-500">[]{'}'}</span>{'\n\n'}
          <span className="text-red-500">@app.post</span><span className="text-neutral-500">(</span><span className="text-neutral-400">"api/posts"</span><span className="text-neutral-500">)</span>{'\n'}
          <span className="text-red-500">def</span> <span className="text-white">create_post</span><span className="text-neutral-500">(</span><span className="text-neutral-600">req</span><span className="text-neutral-500">)</span><span className="text-neutral-500">:</span>{'\n'}
          {'    '}<span className="text-red-500">return</span> <span className="text-neutral-500">{'{'}</span><span className="text-neutral-400">"post"</span><span className="text-neutral-500">:</span> <span className="text-neutral-500">{'{}'}</span><span className="text-neutral-500">{'}'}</span>{'\n\n'}
          <span className="text-red-500">@app.get</span><span className="text-neutral-500">(</span><span className="text-neutral-400">"api/posts/&lt;int:id&gt;"</span><span className="text-neutral-500">)</span>{'\n'}
          <span className="text-red-500">def</span> <span className="text-white">get_post</span><span className="text-neutral-500">(</span><span className="text-neutral-600">req</span><span className="text-neutral-500">,</span> <span className="text-neutral-600">id</span><span className="text-neutral-500">)</span><span className="text-neutral-500">:</span>{'\n'}
          {'    '}<span className="text-red-500">return</span> <span className="text-neutral-500">{'{'}</span><span className="text-neutral-400">"post"</span><span className="text-neutral-500">:</span> <span className="text-neutral-500">{'{'}</span><span className="text-neutral-400">"id"</span><span className="text-neutral-500">:</span> <span className="text-neutral-600">id</span><span className="text-neutral-500">{'}}'}</span>
        </CodeBlock>
      </Section>

      <Section>
        <H2>Route Grouping</H2>
        <P>Group routes with prefixes like Gin/Express:</P>
        <CodeBlock>
          <span className="text-red-500">from</span> <span className="text-white">shanks</span> <span className="text-red-500">import</span> <span className="text-white">App</span>{'\n\n'}
          <span className="text-neutral-600">app = App()</span>{'\n\n'}
          <span className="text-neutral-600"># Create route groups</span>{'\n'}
          <span className="text-neutral-600">api = app.group(</span><span className="text-neutral-400">"api"</span><span className="text-neutral-600">)</span>{'\n'}
          <span className="text-neutral-600">v1 = api.group(</span><span className="text-neutral-400">"v1"</span><span className="text-neutral-600">)</span>{'\n\n'}
          <span className="text-neutral-600"># All routes in v1 will have prefix "api/v1"</span>{'\n'}
          <span className="text-red-500">@v1.get</span><span className="text-neutral-500">(</span><span className="text-neutral-400">"users"</span><span className="text-neutral-500">)</span>{'\n'}
          <span className="text-red-500">def</span> <span className="text-white">list_users</span><span className="text-neutral-500">(</span><span className="text-neutral-600">req</span><span className="text-neutral-500">)</span><span className="text-neutral-500">:</span>{'\n'}
          {'    '}<span className="text-red-500">return</span> <span className="text-neutral-500">{'{'}</span><span className="text-neutral-400">"users"</span><span className="text-neutral-500">:</span> <span className="text-neutral-500">[]{'}'}</span>  <span className="text-neutral-600"># GET /api/v1/users</span>
        </CodeBlock>
      </Section>

      <Section>
        <H2>Multiple Routers</H2>
        <P>Organize routes in separate files:</P>
        
        <div className="space-y-4">
          <div>
            <p className="text-xs text-neutral-600 mb-2">auth.py</p>
            <CodeBlock>
              <span className="text-red-500">from</span> <span className="text-white">shanks</span> <span className="text-red-500">import</span> <span className="text-white">App</span>{'\n\n'}
              <span className="text-neutral-600">router = App()</span>{'\n\n'}
              <span className="text-red-500">@router.post</span><span className="text-neutral-500">(</span><span className="text-neutral-400">"api/auth/login"</span><span className="text-neutral-500">)</span>{'\n'}
              <span className="text-red-500">def</span> <span className="text-white">login</span><span className="text-neutral-500">(</span><span className="text-neutral-600">req</span><span className="text-neutral-500">)</span><span className="text-neutral-500">:</span>{'\n'}
              {'    '}<span className="text-red-500">return</span> <span className="text-neutral-500">{'{'}</span><span className="text-neutral-400">"token"</span><span className="text-neutral-500">:</span> <span className="text-neutral-400">"..."</span><span className="text-neutral-500">{'}'}</span>
            </CodeBlock>
          </div>

          <div>
            <p className="text-xs text-neutral-600 mb-2">__init__.py</p>
            <CodeBlock>
              <span className="text-red-500">from</span> <span className="text-white">shanks</span> <span className="text-red-500">import</span> <span className="text-white">App</span>{'\n'}
              <span className="text-red-500">from</span> <span className="text-white">.</span> <span className="text-red-500">import</span> <span className="text-white">auth</span><span className="text-neutral-500">,</span> <span className="text-white">posts</span>{'\n\n'}
              <span className="text-neutral-600">app = App()</span>{'\n\n'}
              <span className="text-neutral-600"># Include all routers</span>{'\n'}
              <span className="text-neutral-600">app.include(auth.router, posts.router)</span>{'\n\n'}
              <span className="text-neutral-600">urlpatterns = app.get_urls()</span>
            </CodeBlock>
          </div>
        </div>
      </Section>

      <Section>
        <H2>Request Object</H2>
        <CodeBlock>
          <span className="text-red-500">@app.post</span><span className="text-neutral-500">(</span><span className="text-neutral-400">"api/posts"</span><span className="text-neutral-500">)</span>{'\n'}
          <span className="text-red-500">def</span> <span className="text-white">create_post</span><span className="text-neutral-500">(</span><span className="text-neutral-600">req</span><span className="text-neutral-500">)</span><span className="text-neutral-500">:</span>{'\n'}
          {'    '}<span className="text-neutral-600"># Access request data</span>{'\n'}
          {'    '}<span className="text-neutral-600">title = req.body.get(</span><span className="text-neutral-400">"title"</span><span className="text-neutral-600">)</span>{'\n'}
          {'    '}<span className="text-neutral-600">page = req.query.get(</span><span className="text-neutral-400">"page"</span><span className="text-neutral-500">,</span> <span className="text-neutral-400">1</span><span className="text-neutral-600">)</span>{'\n'}
          {'    '}<span className="text-neutral-600">token = req.headers.get(</span><span className="text-neutral-400">"Authorization"</span><span className="text-neutral-600">)</span>{'\n'}
          {'    '}<span className="text-neutral-600">user = req.user</span>{'\n\n'}
          {'    '}<span className="text-red-500">return</span> <span className="text-neutral-500">{'{'}</span><span className="text-neutral-400">"post"</span><span className="text-neutral-500">:</span> <span className="text-neutral-500">{'{'}</span><span className="text-neutral-400">"title"</span><span className="text-neutral-500">:</span> <span className="text-neutral-600">title</span><span className="text-neutral-500">{'}}'}</span>
        </CodeBlock>
      </Section>

      <Section>
        <H2>Response Object</H2>
        <CodeBlock>
          <span className="text-red-500">from</span> <span className="text-white">shanks</span> <span className="text-red-500">import</span> <span className="text-white">Response</span>{'\n\n'}
          <span className="text-red-500">@app.post</span><span className="text-neutral-500">(</span><span className="text-neutral-400">"api/posts"</span><span className="text-neutral-500">)</span>{'\n'}
          <span className="text-red-500">def</span> <span className="text-white">create_post</span><span className="text-neutral-500">(</span><span className="text-neutral-600">req</span><span className="text-neutral-500">)</span><span className="text-neutral-500">:</span>{'\n'}
          {'    '}<span className="text-red-500">return</span> <span className="text-white">Response</span><span className="text-neutral-500">()</span><span className="text-neutral-600">.status_code(</span><span className="text-neutral-400">201</span><span className="text-neutral-600">).json(</span><span className="text-neutral-500">{'{'}</span><span className="text-neutral-400">"post"</span><span className="text-neutral-500">:</span> <span className="text-neutral-500">{'{}'}</span><span className="text-neutral-500">{'}'}</span><span className="text-neutral-600">)</span>
        </CodeBlock>
      </Section>

      <Alert type="info">
        <H3>Pro Tip</H3>
        <P>
          You can return plain dictionaries and Shanks will automatically convert them to JSON responses.
          Use Response() only when you need custom status codes or headers.
        </P>
      </Alert>
    </div>
  )
}
