"""Authentication middleware"""

from app.utils.jwt import decode_token

from shanks import Response, User


def auth_required(req):
    """Require authentication"""
    auth_header = req.headers.get("Authorization", "")

    if not auth_header.startswith("Bearer "):
        return Response().status_code(401).json({"error": "Missing or invalid token"})

    token = auth_header.replace("Bearer ", "")

    try:
        payload = decode_token(token)
        user = User.find_unique(id=payload["user_id"])
        if not user:
            return Response().status_code(401).json({"error": "User not found"})

        req.user = user
        req.user_id = user.id
    except ValueError as e:
        return Response().status_code(401).json({"error": str(e)})
