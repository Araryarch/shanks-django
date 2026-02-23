from shanks import Ace, Request, Response

# Create Shanks app
app = Ace()

# Middleware example
def logger(req: Request):
    print(f"{req.method} {req.path}")

app.use(logger)

# Routes
@app.get('api/users')
def get_users(req: Request):
    return Response().json({
        'users': [
            {'id': 1, 'name': 'John'},
            {'id': 2, 'name': 'Jane'}
        ]
    })

@app.get('api/users/<int:user_id>')
def get_user(req: Request, user_id):
    return {
        'id': user_id,
        'name': 'John Doe'
    }

@app.post('api/users')
def create_user(req: Request):
    data = req.body
    return Response().status_code(201).json({
        'message': 'User created',
        'data': data
    })

# Export for Django urls.py
urlpatterns = app.get_urls()
