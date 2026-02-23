"""Example: CORS configuration with Shanks Django"""

from shanks import App, CORS, enable_cors, Response

# ============================================
# Method 1: Simple - Enable CORS for all origins
# ============================================
app1 = App()

# Enable CORS for all origins (*)
CORS.enable(app1)

# Or using shortcut
# enable_cors(app1)


@app1.get("api/data")
def get_data(req):
    return {"message": "CORS enabled for all origins"}


# ============================================
# Method 2: Specific origins
# ============================================
app2 = App()

# Allow specific origins
CORS.enable(
    app2,
    origins=["http://localhost:3000", "https://myapp.com"],
)


@app2.get("api/users")
def get_users(req):
    return {"users": []}


# ============================================
# Method 3: With credentials (cookies, auth)
# ============================================
app3 = App()

# Enable CORS with credentials
CORS.enable(
    app3,
    origins=["http://localhost:3000"],
    credentials=True,  # Allow cookies and auth headers
)


@app3.post("api/login")
def login(req):
    # Can now receive and send cookies
    return Response().cookie("token", "abc123").json({"success": True})


# ============================================
# Method 4: Full configuration
# ============================================
app4 = App()

CORS.enable(
    app4,
    origins=["http://localhost:3000", "http://localhost:5173"],
    methods=["GET", "POST", "PUT", "DELETE"],
    headers=["Content-Type", "Authorization", "X-Custom-Header"],
    credentials=True,
    max_age=86400,  # Cache preflight for 24 hours
)


@app4.get("api/protected")
def protected(req):
    return {"data": "Protected with CORS"}


# ============================================
# Method 5: Using middleware directly
# ============================================
app5 = App()

# Add CORS as middleware
app5.use(
    CORS.middleware(
        origins=["http://localhost:3000"],
        credentials=True,
    )
)


@app5.get("api/data")
def get_data5(req):
    return {"message": "CORS via middleware"}


# ============================================
# Method 6: Dynamic CORS (check origin in runtime)
# ============================================
app6 = App()

# List of allowed origins
ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:5173",
    "https://myapp.com",
    "https://staging.myapp.com",
]

CORS.enable(app6, origins=ALLOWED_ORIGINS, credentials=True)


@app6.get("api/data")
def get_data6(req):
    return {"message": "Dynamic CORS check"}


# ============================================
# Complete Example: React + Shanks
# ============================================
app = App()

# Enable CORS for React dev server
CORS.enable(
    app,
    origins=["http://localhost:3000", "http://localhost:5173"],  # React/Vite
    methods=["GET", "POST", "PUT", "DELETE", "PATCH"],
    headers=["Content-Type", "Authorization"],
    credentials=True,
)


# Auth middleware
def auth_middleware(req):
    token = req.headers.get("Authorization")
    if not token and req.path.startswith("api/protected"):
        return Response().status_code(401).json({"error": "Unauthorized"})


app.use(auth_middleware)


# Public routes
@app.get("api/health")
def health(req):
    return {"status": "ok"}


@app.post("api/login")
def login(req):
    username = req.body.get("username")
    password = req.body.get("password")

    # Validate credentials
    if username == "admin" and password == "password":
        return (
            Response()
            .cookie("session", "abc123", max_age=3600)
            .json({"success": True, "user": username})
        )

    return Response().status_code(401).json({"error": "Invalid credentials"})


# Protected routes
@app.get("api/protected/data")
def protected_data(req):
    return {"data": "This is protected data", "user": "admin"}


@app.post("api/protected/upload")
def upload(req):
    file = req.files.get("file")
    if file:
        return {"filename": file.name, "size": file.size}
    return Response().status_code(400).json({"error": "No file"})


# Export URL patterns
urlpatterns = app.get_urls()

"""
Frontend (React) example:

// With credentials (cookies)
fetch('http://localhost:8000/api/login', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  credentials: 'include', // Important for cookies
  body: JSON.stringify({
    username: 'admin',
    password: 'password'
  })
})

// With Authorization header
fetch('http://localhost:8000/api/protected/data', {
  headers: {
    'Authorization': 'Bearer token123',
    'Content-Type': 'application/json'
  },
  credentials: 'include'
})
"""
