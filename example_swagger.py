"""Example: Swagger/OpenAPI documentation with Shanks Django"""
from shanks import App, SwaggerUI, Response

app = App()

# Enable Swagger UI at /docs
SwaggerUI.enable(
    app,
    title="My API",
    version="1.0.0",
    description="API documentation for My App",
    docs_url="docs",  # Access at http://localhost:8000/docs
)


# Simple route with documentation
@app.get("api/health")
@SwaggerUI.doc(
    summary="Health check",
    description="Check if the API is running",
    tags=["System"],
    responses={200: {"description": "API is healthy"}},
)
def health(req):
    return {"status": "ok", "version": "1.0.0"}


# GET with path parameter
@app.get("api/users/<int:user_id>")
@SwaggerUI.doc(
    summary="Get user by ID",
    description="Returns a single user by their ID",
    tags=["Users"],
    parameters=[
        {
            "name": "user_id",
            "in": "path",
            "required": True,
            "schema": {"type": "integer"},
            "description": "User ID",
        }
    ],
    responses={
        200: {
            "description": "Success",
            "content": {
                "application/json": {
                    "schema": {
                        "type": "object",
                        "properties": {
                            "id": {"type": "integer"},
                            "name": {"type": "string"},
                            "email": {"type": "string"},
                        },
                    }
                }
            },
        },
        404: {"description": "User not found"},
    },
)
def get_user(req, user_id):
    return {"id": user_id, "name": "John Doe", "email": "john@example.com"}


# GET with query parameters
@app.get("api/users")
@SwaggerUI.doc(
    summary="List all users",
    description="Returns a paginated list of users",
    tags=["Users"],
    parameters=[
        {
            "name": "page",
            "in": "query",
            "schema": {"type": "integer", "default": 1},
            "description": "Page number",
        },
        {
            "name": "limit",
            "in": "query",
            "schema": {"type": "integer", "default": 10},
            "description": "Items per page",
        },
    ],
    responses={200: {"description": "Success"}},
)
def get_users(req):
    page = req.query.get("page", 1)
    limit = req.query.get("limit", 10)
    return {"users": [], "page": page, "limit": limit}


# POST with request body
@app.post("api/users")
@SwaggerUI.doc(
    summary="Create a new user",
    description="Creates a new user with the provided data",
    tags=["Users"],
    request_body={
        "required": True,
        "content": {
            "application/json": {
                "schema": {
                    "type": "object",
                    "required": ["name", "email"],
                    "properties": {
                        "name": {"type": "string", "example": "John Doe"},
                        "email": {
                            "type": "string",
                            "format": "email",
                            "example": "john@example.com",
                        },
                        "age": {"type": "integer", "example": 30},
                    },
                }
            }
        },
    },
    responses={
        201: {"description": "User created successfully"},
        400: {"description": "Invalid input"},
    },
)
def create_user(req):
    data = req.body
    return Response().status_code(201).json(
        {"id": 1, "name": data.get("name"), "email": data.get("email")}
    )


# PUT with path parameter and request body
@app.put("api/users/<int:user_id>")
@SwaggerUI.doc(
    summary="Update user",
    description="Updates an existing user",
    tags=["Users"],
    parameters=[
        {
            "name": "user_id",
            "in": "path",
            "required": True,
            "schema": {"type": "integer"},
        }
    ],
    request_body={
        "required": True,
        "content": {
            "application/json": {
                "schema": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "email": {"type": "string"},
                    },
                }
            }
        },
    },
    responses={
        200: {"description": "User updated"},
        404: {"description": "User not found"},
    },
)
def update_user(req, user_id):
    data = req.body
    return {"id": user_id, "updated": True}


# DELETE
@app.delete("api/users/<int:user_id>")
@SwaggerUI.doc(
    summary="Delete user",
    description="Deletes a user by ID",
    tags=["Users"],
    parameters=[
        {
            "name": "user_id",
            "in": "path",
            "required": True,
            "schema": {"type": "integer"},
        }
    ],
    responses={
        200: {"description": "User deleted"},
        404: {"description": "User not found"},
    },
)
def delete_user(req, user_id):
    return {"deleted": True, "id": user_id}


# File upload
@app.post("api/upload")
@SwaggerUI.doc(
    summary="Upload file",
    description="Upload a file to the server",
    tags=["Files"],
    request_body={
        "required": True,
        "content": {
            "multipart/form-data": {
                "schema": {
                    "type": "object",
                    "properties": {"file": {"type": "string", "format": "binary"}},
                }
            }
        },
    },
    responses={
        200: {"description": "File uploaded"},
        400: {"description": "No file provided"},
    },
)
def upload_file(req):
    file = req.files.get("file")
    if file:
        return {"filename": file.name, "size": file.size}
    return Response().status_code(400).json({"error": "No file"})


urlpatterns = app.get_urls()

"""
After running the server, visit:
- http://localhost:8000/docs - Swagger UI
- http://localhost:8000/openapi.json - OpenAPI spec
"""
