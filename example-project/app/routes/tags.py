"""Tag routes"""

from app.middleware import auth_required
from app.models import Tag

from shanks import App, Response, SwaggerUI, slugify

router = App()


@router.get("api/tags")
@SwaggerUI.doc(summary="List tags", tags=["Tags"])
def list_tags(req):
    """List all tags"""
    tags = Tag.objects.all()

    return Response().json(
        {
            "tags": [
                {
                    "id": tag.id,
                    "name": tag.name,
                    "slug": tag.slug,
                    "posts_count": tag.posts.count(),
                }
                for tag in tags
            ]
        }
    )


@router.post("api/tags")
@SwaggerUI.doc(summary="Create tag", tags=["Tags"])
def create_tag(req):
    """Create new tag"""
    # Auth required
    auth_response = auth_required(req)
    if auth_response:
        return auth_response

    name = req.body.get("name")

    if not name:
        return Response().status_code(400).json({"error": "Name is required"})

    slug = slugify(name)

    if Tag.objects.filter(slug=slug).exists():
        return Response().status_code(400).json({"error": "Tag already exists"})

    tag = Tag.objects.create(name=name, slug=slug)

    return (
        Response()
        .status_code(201)
        .json({"id": tag.id, "name": tag.name, "slug": tag.slug})
    )


@router.get("api/tags/<int:tag_id>")
@SwaggerUI.doc(summary="Get tag", tags=["Tags"])
def get_tag(req, tag_id):
    """Get tag by ID"""
    try:
        tag = Tag.objects.get(id=tag_id)
        return Response().json(
            {
                "id": tag.id,
                "name": tag.name,
                "slug": tag.slug,
                "posts_count": tag.posts.count(),
            }
        )
    except Tag.DoesNotExist:
        return Response().status_code(404).json({"error": "Tag not found"})


@router.delete("api/tags/<int:tag_id>")
@SwaggerUI.doc(summary="Delete tag", tags=["Tags"])
def delete_tag(req, tag_id):
    """Delete tag"""
    # Auth required (admin only)
    auth_response = auth_required(req)
    if auth_response:
        return auth_response

    if not req.user.is_staff:
        return Response().status_code(403).json({"error": "Admin access required"})

    try:
        tag = Tag.objects.get(id=tag_id)
        tag.delete()
        return Response().json({"message": "Tag deleted"})
    except Tag.DoesNotExist:
        return Response().status_code(404).json({"error": "Tag not found"})
