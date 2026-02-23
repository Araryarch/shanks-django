# Bruno API Collection

API testing collection for Blog API using Bruno.

## Setup

1. Install Bruno: https://www.usebruno.com/
2. Open Bruno
3. Open Collection → Select this folder (`bruno/`)

## Usage

1. **Register** - Create a new user
2. **Login** - Get JWT token
3. Copy token from response
4. Use token in other requests (Authorization header)

## Environment Variables

Create environment in Bruno:
- `baseUrl`: http://localhost:8000
- `token`: (paste your JWT token here)

## Collections

- **Auth** - Register, Login, Get Me
- **Users** - List, Get, Update, Delete
- **Posts** - List, Create, Get, Update, Delete, Like
- **Comments** - List, Create, Update, Delete
- **Categories** - List, Create, Get, Update, Delete
- **Tags** - List, Create, Get, Delete
