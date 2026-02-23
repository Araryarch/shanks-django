"""Post routes"""

from app.dto import PostCreateDTO, PostDTO, PostUpdateDTO
from app.middleware import auth_required
from app.models import Category, Like, Post, Tag

from shanks import App, Response, SwaggerUI

router = App()


@router.get("api/posts")
@SwaggerUI.doc(summary="List posts", tags=["Posts"])
def list_posts(req):
    """List all posts"""
    page = int(req.query.get("page", 1))
    limit = int(req.query.get("limit", 10))
    category = req.query.get("category")

    posts = Post.find_many()

    if category:
        posts = posts.filter(category__slug=category)

    total = posts.count()
    posts = posts[(page - 1) * limit : page * limit]

    return Response().json(
        {
            "posts": [PostDTO(post).to_dict() for post in posts],
            "total": total,
            "page": page,
            "limit": limit,
        }
    )


@router.post("api/posts")
@SwaggerUI.doc(summary="Create post", tags=["Posts"])
def create_post(req):
    """Create new post"""
    # Auth required
    auth_response = auth_required(req)
    if auth_response:
        return auth_response

    dto = PostCreateDTO(req.body)
    errors = dto.validate()

    if errors:
        return Response().status_code(400).json({"errors": errors})

    # Create post
    post = Post.create(
        title=dto.title,
        content=dto.content,
        excerpt=dto.excerpt,
        author=req.user,
    )

    # Set category
    if dto.category_id:
        category = Category.find_unique(id=dto.category_id)
        if category:
            post.category = category

    # Set tags
    if dto.tag_ids:
        tags = Tag.find_many(id__in=dto.tag_ids)
        post.tags.set(tags)

    post.save()

    return Response().status_code(201).json(PostDTO(post).to_dict())


@router.get("api/posts/<int:post_id>")
@SwaggerUI.doc(summary="Get post by ID", tags=["Posts"])
def get_post(req, post_id):
    """Get post by ID"""
    post = Post.find_unique(id=post_id)
    if not post:
        return Response().status_code(404).json({"error": "Post not found"})

    return Response().json(PostDTO(post).to_dict())


@router.put("api/posts/<int:post_id>")
@SwaggerUI.doc(summary="Update post", tags=["Posts"])
def update_post(req, post_id):
    """Update post"""
    # Auth required
    auth_response = auth_required(req)
    if auth_response:
        return auth_response

    post = Post.find_unique(id=post_id)
    if not post:
        return Response().status_code(404).json({"error": "Post not found"})

    # Check permission
    if post.author.id != req.user.id and not req.user.is_staff:
        return Response().status_code(403).json({"error": "Permission denied"})

    dto = PostUpdateDTO(req.body)

    if dto.title:
        post.title = dto.title
    if dto.content:
        post.content = dto.content
    if dto.excerpt is not None:
        post.excerpt = dto.excerpt
    if dto.category_id:
        category = Category.find_unique(id=dto.category_id)
        if category:
            post.category = category
    if dto.tag_ids is not None:
        tags = Tag.find_many(id__in=dto.tag_ids)
        post.tags.set(tags)

    post.save()

    return Response().json(PostDTO(post).to_dict())


@router.delete("api/posts/<int:post_id>")
@SwaggerUI.doc(summary="Delete post", tags=["Posts"])
def delete_post(req, post_id):
    """Delete post"""
    # Auth required
    auth_response = auth_required(req)
    if auth_response:
        return auth_response

    post = Post.find_unique(id=post_id)
    if not post:
        return Response().status_code(404).json({"error": "Post not found"})

    # Check permission
    if post.author.id != req.user.id and not req.user.is_staff:
        return Response().status_code(403).json({"error": "Permission denied"})

    post.delete_self()
    return Response().json({"message": "Post deleted"})


@router.post("api/posts/<int:post_id>/like")
@SwaggerUI.doc(summary="Like/Unlike post", tags=["Posts"])
def toggle_like(req, post_id):
    """Toggle like on post"""
    # Auth required
    auth_response = auth_required(req)
    if auth_response:
        return auth_response

    post = Post.find_unique(id=post_id)
    if not post:
        return Response().status_code(404).json({"error": "Post not found"})

    # Check if already liked
    like = Like.find_first(user=req.user, post=post)

    if like:
        like.delete_self()
        return Response().json({"liked": False, "likes_count": Like.count(post=post)})
    else:
        Like.create(user=req.user, post=post)
        return Response().json({"liked": True, "likes_count": Like.count(post=post)})
