import { DocPage, CodeBlock } from '@/components/DocPage';

export default function DockerPage() {
  return (
    <DocPage title="Docker" description="Containerise your Shanks API for consistent, reproducible deployments.">

      <h2>Dockerfile</h2>
      <CodeBlock
        filename="Dockerfile"
        language="bash"
        code={`FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN python manage.py collectstatic --no-input

EXPOSE 8000

CMD ["gunicorn", "myproject.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "4"]`}
      />

      <h2>docker-compose.yml</h2>
      <CodeBlock
        filename="docker-compose.yml"
        language="bash"
        code={`version: '3.9'

services:
  db:
    image: postgres:15
    environment:
      POSTGRES_DB: mydb
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
    volumes:
      - postgres_data:/var/lib/postgresql/data

  web:
    build: .
    ports:
      - "8000:8000"
    environment:
      DATABASE_URL: postgresql://user:password@db:5432/mydb
      DEBUG: "False"
      SECRET_KEY: your-secret-key
    depends_on:
      - db
    command: >
      sh -c "python manage.py migrate && gunicorn myproject.wsgi:application --bind 0.0.0.0:8000"

volumes:
  postgres_data:`}
      />

      <h2>Run</h2>
      <CodeBlock
        language="bash"
        code={`# Build and start
docker-compose up --build

# Run migrations
docker-compose exec web python manage.py migrate`}
      />
    </DocPage>
  );
}
