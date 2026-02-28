"""Authentication middleware template"""


def get_auth_middleware_template():
    """JWT authentication middleware template"""
    return '''"""
JWT Authentication Middleware
"""
from shanks import User, settings
import jwt
from dto.base_dto import BaseDTO


def jwt_auth_middleware(req, res, next):
    """
    JWT Authentication Middleware
    
    Validates JWT token from Authorization header and attaches user to request.
    Protected routes should use this middleware.
    
    Usage in routes:
        @router.get('/protected', middleware=[jwt_auth_middleware])
        def protected_route(req):
            user = req.user  # Authenticated user
            return {"user_id": user.id}
    """
    # Get token from Authorization header
    auth_header = req.headers.get("Authorization", "")
    
    if not auth_header.startswith("Bearer "):
        return BaseDTO.error(
            message="Authorization header required (Bearer token)",
            status=401
        )
    
    token = auth_header.replace("Bearer ", "")
    
    try:
        # Decode and verify token
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        user = User.objects.get(id=payload["user_id"])
        
        # Attach user to request
        req.user = user
        req.user_id = user.id
        
        # Continue to next middleware/handler
        return next()
        
    except jwt.ExpiredSignatureError:
        return BaseDTO.error(message="Token has expired", status=401)
    except jwt.InvalidTokenError:
        return BaseDTO.error(message="Invalid token", status=401)
    except User.DoesNotExist:
        return BaseDTO.error(message="User not found", status=401)
    except Exception as e:
        return BaseDTO.error(message=f"Authentication failed: {str(e)}", status=401)


def optional_auth_middleware(req, res, next):
    """
    Optional JWT Authentication Middleware
    
    Validates JWT token if present, but allows request to continue even without token.
    Useful for routes that work differently for authenticated vs anonymous users.
    
    Usage in routes:
        @router.get('/public', middleware=[optional_auth_middleware])
        def public_route(req):
            if hasattr(req, 'user'):
                return {"message": f"Hello {req.user.username}"}
            return {"message": "Hello guest"}
    """
    # Get token from Authorization header
    auth_header = req.headers.get("Authorization", "")
    
    if auth_header.startswith("Bearer "):
        token = auth_header.replace("Bearer ", "")
        
        try:
            # Decode and verify token
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user = User.objects.get(id=payload["user_id"])
            
            # Attach user to request
            req.user = user
            req.user_id = user.id
        except:
            # Token invalid, but continue anyway
            pass
    
    # Continue to next middleware/handler
    return next()
'''
