"""User routes"""

from app.dto import UserDTO, UserUpdateDTO
from app.middleware import auth_required

from shanks import App, Response, SwaggerUI, User

router = App()


@router.get("api/users")
@SwaggerUI.doc(summary="List users", tags=["Users"])
def list_users(req):
    """List all users"""
    page = int(req.query.get("page", 1))
    limit = int(req.query.get("limit", 10))

    users = User.find_many()[(page - 1) * limit : page * limit]
    total = User.count()

    return Response().json(
        {
            "users": [UserDTO(user).to_dict() for user in users],
            "total": total,
            "page": page,
            "limit": limit,
        }
    )


@router.get("api/users/<int:user_id>")
@SwaggerUI.doc(summary="Get user by ID", tags=["Users"])
def get_user(req, user_id):
    """Get user by ID"""
    user = User.find_unique(id=user_id)
    if not user:
        return Response().status_code(404).json({"error": "User not found"})

    return Response().json(UserDTO(user).to_dict())


@router.put("api/users/<int:user_id>")
@SwaggerUI.doc(summary="Update user", tags=["Users"])
def update_user(req, user_id):
    """Update user"""
    # Auth required
    auth_response = auth_required(req)
    if auth_response:
        return auth_response

    # Check permission
    if req.user.id != user_id and not req.user.is_staff:
        return Response().status_code(403).json({"error": "Permission denied"})

    user = User.find_unique(id=user_id)
    if not user:
        return Response().status_code(404).json({"error": "User not found"})

    dto = UserUpdateDTO(req.body)

    if dto.first_name is not None:
        user.first_name = dto.first_name
    if dto.last_name is not None:
        user.last_name = dto.last_name
    if dto.email is not None:
        user.email = dto.email

    user.save()

    return Response().json(UserDTO(user).to_dict())


@router.delete("api/users/<int:user_id>")
@SwaggerUI.doc(summary="Delete user", tags=["Users"])
def delete_user(req, user_id):
    """Delete user"""
    # Auth required
    auth_response = auth_required(req)
    if auth_response:
        return auth_response

    # Check permission
    if req.user.id != user_id and not req.user.is_staff:
        return Response().status_code(403).json({"error": "Permission denied"})

    user = User.find_unique(id=user_id)
    if not user:
        return Response().status_code(404).json({"error": "User not found"})

    user.delete_self()
    return Response().json({"message": "User deleted"})
