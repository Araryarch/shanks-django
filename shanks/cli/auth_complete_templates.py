"""Complete authentication templates with email verification"""


def get_complete_auth_controller_template():
    """Complete auth controller with email verification"""
    return '''"""
Complete Authentication Controller with Email Verification
"""
from shanks import authenticate, User, IntegrityError, settings, send_mail
from dto.base_dto import BaseDTO
import jwt
import datetime
import random
import string


# In-memory storage for verification codes (use Redis in production)
verification_codes = {}
reset_codes = {}


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


def generate_code(length=6):
    """Generate random verification code"""
    return ''.join(random.choices(string.digits, k=length))


def send_verification_email(user, code):
    """Send verification email"""
    subject = "Verify Your Email"
    message = f"""
    Hi {user.username},
    
    Your verification code is: {code}
    
    This code will expire in 10 minutes.
    
    If you didn't request this, please ignore this email.
    """
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL or 'noreply@example.com', [user.email])


def send_reset_email(user, code):
    """Send password reset email"""
    subject = "Reset Your Password"
    message = f"""
    Hi {user.username},
    
    Your password reset code is: {code}
    
    This code will expire in 10 minutes.
    
    If you didn't request this, please ignore this email.
    """
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL or 'noreply@example.com', [user.email])


def register(req):
    """Handle user registration with email verification"""
    data = req.body
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    # Validation
    if not username or not password or not email:
        return BaseDTO.error(message="Username, email and password are required", status=400)

    if len(password) < 6:
        return BaseDTO.error(message="Password must be at least 6 characters", status=400)

    # Create user (inactive until verified)
    try:
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            is_active=False  # User must verify email first
        )
        
        # Generate and store verification code
        code = generate_code()
        verification_codes[user.id] = {
            "code": code,
            "expires": datetime.datetime.utcnow() + datetime.timedelta(minutes=10)
        }
        
        # Send verification email
        try:
            send_verification_email(user, code)
        except Exception as e:
            print(f"Failed to send email: {e}")
        
        return BaseDTO.success(
            data={
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "is_verified": False
                },
                "message": "Please check your email for verification code"
            },
            message="Registration successful. Please verify your email.",
            status=201
        )
    except IntegrityError:
        return BaseDTO.error(message="Username or email already exists", status=400)
    except Exception as e:
        return BaseDTO.error(message=f"Registration failed: {str(e)}", status=500)


def verify_email(req):
    """Verify email with code"""
    data = req.body
    user_id = data.get("user_id")
    code = data.get("code")

    if not user_id or not code:
        return BaseDTO.error(message="User ID and code are required", status=400)

    # Check if code exists and is valid
    if user_id not in verification_codes:
        return BaseDTO.error(message="Invalid or expired verification code", status=400)

    stored = verification_codes[user_id]
    
    # Check expiration
    if datetime.datetime.utcnow() > stored["expires"]:
        del verification_codes[user_id]
        return BaseDTO.error(message="Verification code expired", status=400)

    # Check code match
    if stored["code"] != code:
        return BaseDTO.error(message="Invalid verification code", status=400)

    # Activate user
    try:
        user = User.objects.get(id=user_id)
        user.is_active = True
        user.save()
        
        # Remove used code
        del verification_codes[user_id]
        
        # Generate token
        token = generate_token(user)
        
        return BaseDTO.success(
            data={
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "is_verified": True
                },
                "token": token
            },
            message="Email verified successfully"
        )
    except User.DoesNotExist:
        return BaseDTO.error(message="User not found", status=404)


def resend_verification(req):
    """Resend verification email"""
    data = req.body
    email = data.get("email")

    if not email:
        return BaseDTO.error(message="Email is required", status=400)

    try:
        user = User.objects.get(email=email, is_active=False)
        
        # Generate new code
        code = generate_code()
        verification_codes[user.id] = {
            "code": code,
            "expires": datetime.datetime.utcnow() + datetime.timedelta(minutes=10)
        }
        
        # Send email
        try:
            send_verification_email(user, code)
        except Exception as e:
            print(f"Failed to send email: {e}")
        
        return BaseDTO.success(
            data={"user_id": user.id},
            message="Verification code sent to your email"
        )
    except User.DoesNotExist:
        return BaseDTO.error(message="User not found or already verified", status=404)


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
        if not user.is_active:
            return BaseDTO.error(message="Please verify your email first", status=403)
        
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


def forgot_password(req):
    """Request password reset"""
    data = req.body
    email = data.get("email")

    if not email:
        return BaseDTO.error(message="Email is required", status=400)

    try:
        user = User.objects.get(email=email)
        
        # Generate reset code
        code = generate_code()
        reset_codes[user.id] = {
            "code": code,
            "expires": datetime.datetime.utcnow() + datetime.timedelta(minutes=10)
        }
        
        # Send reset email
        try:
            send_reset_email(user, code)
        except Exception as e:
            print(f"Failed to send email: {e}")
        
        return BaseDTO.success(
            data={"user_id": user.id},
            message="Password reset code sent to your email"
        )
    except User.DoesNotExist:
        # Don't reveal if email exists
        return BaseDTO.success(
            message="If email exists, reset code will be sent"
        )


def reset_password(req):
    """Reset password with code"""
    data = req.body
    user_id = data.get("user_id")
    code = data.get("code")
    new_password = data.get("new_password")

    if not user_id or not code or not new_password:
        return BaseDTO.error(message="User ID, code and new password are required", status=400)

    if len(new_password) < 6:
        return BaseDTO.error(message="Password must be at least 6 characters", status=400)

    # Check if code exists and is valid
    if user_id not in reset_codes:
        return BaseDTO.error(message="Invalid or expired reset code", status=400)

    stored = reset_codes[user_id]
    
    # Check expiration
    if datetime.datetime.utcnow() > stored["expires"]:
        del reset_codes[user_id]
        return BaseDTO.error(message="Reset code expired", status=400)

    # Check code match
    if stored["code"] != code:
        return BaseDTO.error(message="Invalid reset code", status=400)

    # Reset password
    try:
        user = User.objects.get(id=user_id)
        user.set_password(new_password)
        user.save()
        
        # Remove used code
        del reset_codes[user_id]
        
        return BaseDTO.success(message="Password reset successfully")
    except User.DoesNotExist:
        return BaseDTO.error(message="User not found", status=404)


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


def get_complete_auth_route_template():
    """Complete auth routes template"""
    return '''"""
Complete Authentication Routes with Email Verification
"""
from shanks import App
from internal.controller import auth_controller

# Group all auth routes under /api/v1/auth
router = App(prefix='/api/v1/auth')

@router.post('/register')
def register_route(req):
    """Register new user"""
    return auth_controller.register(req)

@router.post('/verify-email')
def verify_email_route(req):
    """Verify email with code"""
    return auth_controller.verify_email(req)

@router.post('/resend-verification')
def resend_verification_route(req):
    """Resend verification email"""
    return auth_controller.resend_verification(req)

@router.post('/login')
def login_route(req):
    """Login user"""
    return auth_controller.login_user(req)

@router.post('/forgot-password')
def forgot_password_route(req):
    """Request password reset"""
    return auth_controller.forgot_password(req)

@router.post('/reset-password')
def reset_password_route(req):
    """Reset password with code"""
    return auth_controller.reset_password(req)

@router.post('/logout')
def logout_route(req):
    """Logout user"""
    return auth_controller.logout_user(req)

@router.get('/me')
def me_route(req):
    """Get current user info"""
    return auth_controller.get_current_user(req)
'''
