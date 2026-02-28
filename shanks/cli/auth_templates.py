"""Simple authentication templates"""


def get_simple_auth_controller_template():
    """Simple auth controller template"""
    return '''"""
Authentication Controller - Request/Response Handler
"""
from shanks import authenticate, User, IntegrityError, settings
from dto.base_dto import BaseDTO
import jwt
import datetime


def generate_token(user):
    """Generate JWT token for user"""
    payload = {
        "user_id": user.id,
        "username": user.username,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(days=7),
        "iat": datetime.datetime.utcnow()
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
    return token


def verify_token(token):
    """Verify JWT token and return user"""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        user = User.objects.get(id=payload["user_id"])
        return user
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError, User.DoesNotExist):
        return None


def register(req):
    """Handle user registration"""
    data = req.body
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    # Validation
    if not username or not password:
        return BaseDTO.error(message="Username and password are required", status=400)

    if len(password) < 6:
        return BaseDTO.error(message="Password must be at least 6 characters", status=400)

    # Create user
    try:
        user = User.objects.create_user(
            username=username,
            email=email or "",
            password=password
        )
        
        # Generate token
        token = generate_token(user)
        
        return BaseDTO.success(
            data={
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email
                },
                "token": token
            },
            message="Registration successful",
            status=201
        )
    except IntegrityError:
        return BaseDTO.error(message="Username already exists", status=400)
    except Exception as e:
        return BaseDTO.error(message=f"Registration failed: {str(e)}", status=500)


def login_user(req):
    """Handle user login"""
    data = req.body
    username = data.get("username")
    password = data.get("password")

    # Validation
    if not username or not password:
        return BaseDTO.error(message="Username and password are required", status=400)

    # Authenticate
    user = authenticate(username=username, password=password)
    
    if user is not None:
        # Generate token
        token = generate_token(user)
        
        return BaseDTO.success(
            data={
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email
                },
                "token": token
            },
            message="Login successful"
        )
    else:
        return BaseDTO.error(message="Invalid username or password", status=401)


def logout_user(req):
    """Handle user logout (client-side token removal)"""
    return BaseDTO.success(message="Logout successful. Please remove token from client.")


def get_current_user(req):
    """Get current authenticated user info from token"""
    # Get token from Authorization header
    auth_header = req.headers.get("Authorization", "")
    
    if not auth_header.startswith("Bearer "):
        return BaseDTO.error(message="Authorization header required (Bearer token)", status=401)
    
    token = auth_header.replace("Bearer ", "")
    user = verify_token(token)
    
    if user is None:
        return BaseDTO.error(message="Invalid or expired token", status=401)
    
    return BaseDTO.success(
        data={
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "is_staff": user.is_staff,
            "is_superuser": user.is_superuser,
            "date_joined": user.date_joined.isoformat()
        }
    )
'''


def get_simple_auth_route_template():
    """Simple auth routes template"""
    return '''"""
Authentication Routes
"""
from shanks import App
from internal.controller import auth_controller

# Group all auth routes under /api/v1/auth
router = App(prefix='/api/v1/auth')

@router.post('/register')
def register_route(req):
    """Register new user"""
    return auth_controller.register(req)

@router.post('/login')
def login_route(req):
    """Login user"""
    return auth_controller.login_user(req)

@router.post('/logout')
def logout_route(req):
    """Logout user"""
    return auth_controller.logout_user(req)

@router.get('/me')
def me_route(req):
    """Get current user info"""
    return auth_controller.get_current_user(req)
'''
