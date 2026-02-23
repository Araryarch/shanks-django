"""Comment routes"""

from app.dto import CommentCreateDTO, CommentDTO
from app.middleware import auth_required
from app.models import Comment, Post

from shanks import App, Response, SwaggerUI

router = App()


@router.get("api/posts/<int:post_id>/comments")
@SwaggerUI.doc(summary="List comments for post", tags=["Comments"])
def list_comments(req, post_id):
    """List comments for a post"""
    post = Post.find_unique(id=post_id)
    if not post:
        return Response().status_code(404).json({"error": "Post not found"})

    comments = Comment.find_many(post=post)

    return Response().json(
        {"comments": [CommentDTO(comment).to_dict() for comment in comments]}
    )


@router.post("api/posts/<int:post_id>/comments")
@SwaggerUI.doc(summary="Create comment", tags=["Comments"])
def create_comment(req, post_id):
    """Create comment on post"""
    # Auth required
    auth_response = auth_required(req)
    if auth_response:
        return auth_response

    post = Post.find_unique(id=post_id)
    if not post:
        return Response().status_code(404).json({"error": "Post not found"})

    dto = CommentCreateDTO(req.body)
    errors = dto.validate()

    if errors:
        return Response().status_code(400).json({"errors": errors})

    comment = Comment.create(content=dto.content, author=req.user, post=post)

    return Response().status_code(201).json(CommentDTO(comment).to_dict())


@router.put("api/comments/<int:comment_id>")
@SwaggerUI.doc(summary="Update comment", tags=["Comments"])
def update_comment(req, comment_id):
    """Update comment"""
    # Auth required
    auth_response = auth_required(req)
    if auth_response:
        return auth_response

    comment = Comment.find_unique(id=comment_id)
    if not comment:
        return Response().status_code(404).json({"error": "Comment not found"})

    # Check permission
    if comment.author.id != req.user.id:
        return Response().status_code(403).json({"error": "Permission denied"})

    content = req.body.get("content")
    if content:
        comment.update_self(content=content)

    return Response().json(CommentDTO(comment).to_dict())


@router.delete("api/comments/<int:comment_id>")
@SwaggerUI.doc(summary="Delete comment", tags=["Comments"])
def delete_comment(req, comment_id):
    """Delete comment"""
    # Auth required
    auth_response = auth_required(req)
    if auth_response:
        return auth_response

    comment = Comment.find_unique(id=comment_id)
    if not comment:
        return Response().status_code(404).json({"error": "Comment not found"})

    # Check permission
    if comment.author.id != req.user.id and not req.user.is_staff:
        return Response().status_code(403).json({"error": "Permission denied"})

    comment.delete_self()
    return Response().json({"message": "Comment deleted"})
