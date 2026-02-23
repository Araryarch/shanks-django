"""Authentication routes"""

from app.dto import UserCreateDTO, UserDTO
from app.middleware import auth_required
from app.utils.jwt import create_token

from shanks import App, Response, SwaggerUI, User, authenticate

router = App()


@router.post("api/auth/register")
@SwaggerUI.doc(
    summary="Register new user",
    tags=["Authentication"],
    request_body={
        "required": True,
        "content": {
            "application/json": {
                "schema": {
                    "type": "object",
                    "required": ["username", "email", "password"],
                    "properties": {
                        "username": {"type": "string"},
                        "email": {"type": "string"},
                        "password": {"type": "string"},
                        "first_name": {"type": "string"},
                        "last_name": {"type": "string"},
                    },
                }
            }
        },
    },
)
def register(req):
    """Register new user"""
    dto = UserCreateDTO(req.body)
    errors = dto.validate()

    if errors:
        return Response().status_code(400).json({"errors": errors})

    # Check if user exists
    if User.find_unique(username=dto.username):
        return Response().status_code(400).json({"error": "Username already exists"})

    if User.find_unique(email=dto.email):
        return Response().status_code(400).json({"error": "Email already exists"})

    # Create user
    user = User.create(
        username=dto.username,
        email=dto.email,
        password=dto.password,
        first_name=dto.first_name,
        last_name=dto.last_name,
    )

    # Generate token
    token = create_token(user.id, user.username)

    return (
        Response()
        .status_code(201)
        .json({"token": token, "user": UserDTO(user).to_dict()})
    )


@router.post("api/auth/login")
@SwaggerUI.doc(
    summary="Login",
    tags=["Authentication"],
    request_body={
        "required": True,
        "content": {
            "application/json": {
                "schema": {
                    "type": "object",
                    "required": ["username", "password"],
                    "properties": {
                        "username": {"type": "string"},
                        "password": {"type": "string"},
                    },
                }
            }
        },
    },
)
def login(req):
    """Login user"""
    username = req.body.get("username")
    password = req.body.get("password")

    if not username or not password:
        return (
            Response()
            .status_code(400)
            .json({"error": "Username and password required"})
        )

    user = authenticate(username=username, password=password)

    if not user:
        return Response().status_code(401).json({"error": "Invalid credentials"})

    token = create_token(user.id, user.username)

    return Response().json({"token": token, "user": UserDTO(user).to_dict()})


@router.get("api/auth/me")
@SwaggerUI.doc(
    summary="Get current user",
    tags=["Authentication"],
    parameters=[
        {
            "name": "Authorization",
            "in": "header",
            "required": True,
            "schema": {"type": "string"},
            "description": "Bearer token",
        }
    ],
)
def me(req):
    """Get current user"""
    # Apply auth middleware
    auth_response = auth_required(req)
    if auth_response:
        return auth_response

    return Response().json(UserDTO(req.user).to_dict())
