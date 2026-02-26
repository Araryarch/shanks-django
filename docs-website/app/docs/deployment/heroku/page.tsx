import { DocPage, CodeBlock, Callout } from '@/components/DocPage';

export default function HerokuPage() {
  return (
    <DocPage title="Deploy to Heroku" description="Deploy your Shanks API to Heroku using git push.">

      <h2>Prerequisites</h2>
      <ul>
        <li>Heroku CLI installed</li>
        <li><code>shanks generate django</code> already run</li>
        <li>PostgreSQL addon for database</li>
      </ul>

      <h2>Setup</h2>
      <CodeBlock
        language="bash"
        code={`cd django_output/

# Login to Heroku
heroku login

# Create app
heroku create my-shanks-api

# Add PostgreSQL
heroku addons:create heroku-postgresql:mini`}
      />

      <h2>Configure Environment</h2>
      <CodeBlock
        language="bash"
        code={`heroku config:set DEBUG=False
heroku config:set SECRET_KEY=your-production-secret
heroku config:set ALLOWED_HOSTS=my-shanks-api.herokuapp.com`}
      />

      <h2>Add Procfile</h2>
      <CodeBlock
        filename="Procfile"
        language="text"
        code={`web: gunicorn myproject.wsgi:application`}
      />

      <h2>Deploy</h2>
      <CodeBlock
        language="bash"
        code={`git init
git add .
git commit -m "Initial deploy"
heroku git:remote -a my-shanks-api
git push heroku main

# Run migrations
heroku run python manage.py migrate`}
      />

      <Callout type="success">
        Your API will be live at <code>https://my-shanks-api.herokuapp.com</code>
      </Callout>
    </DocPage>
  );
}
