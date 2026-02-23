"""Category routes"""

from app.middleware import auth_required
from app.models import Category

from shanks import App, Response, SwaggerUI, slugify

router = App()


@router.get("api/categories")
@SwaggerUI.doc(summary="List categories", tags=["Categories"])
def list_categories(req):
    """List all categories"""
    categories = Category.objects.all()

    return Response().json(
        {
            "categories": [
                {
                    "id": cat.id,
                    "name": cat.name,
                    "slug": cat.slug,
                    "description": cat.description,
                    "posts_count": cat.posts.count(),
                }
                for cat in categories
            ]
        }
    )


@router.post("api/categories")
@SwaggerUI.doc(summary="Create category", tags=["Categories"])
def create_category(req):
    """Create new category"""
    # Auth required (admin only)
    auth_response = auth_required(req)
    if auth_response:
        return auth_response

    if not req.user.is_staff:
        return Response().status_code(403).json({"error": "Admin access required"})

    name = req.body.get("name")
    description = req.body.get("description", "")

    if not name:
        return Response().status_code(400).json({"error": "Name is required"})

    slug = slugify(name)

    if Category.objects.filter(slug=slug).exists():
        return Response().status_code(400).json({"error": "Category already exists"})

    category = Category.objects.create(name=name, slug=slug, description=description)

    return (
        Response()
        .status_code(201)
        .json(
            {
                "id": category.id,
                "name": category.name,
                "slug": category.slug,
                "description": category.description,
            }
        )
    )


@router.get("api/categories/<int:category_id>")
@SwaggerUI.doc(summary="Get category", tags=["Categories"])
def get_category(req, category_id):
    """Get category by ID"""
    try:
        category = Category.objects.get(id=category_id)
        return Response().json(
            {
                "id": category.id,
                "name": category.name,
                "slug": category.slug,
                "description": category.description,
                "posts_count": category.posts.count(),
            }
        )
    except Category.DoesNotExist:
        return Response().status_code(404).json({"error": "Category not found"})


@router.put("api/categories/<int:category_id>")
@SwaggerUI.doc(summary="Update category", tags=["Categories"])
def update_category(req, category_id):
    """Update category"""
    # Auth required (admin only)
    auth_response = auth_required(req)
    if auth_response:
        return auth_response

    if not req.user.is_staff:
        return Response().status_code(403).json({"error": "Admin access required"})

    try:
        category = Category.objects.get(id=category_id)

        name = req.body.get("name")
        description = req.body.get("description")

        if name:
            category.name = name
            category.slug = slugify(name)
        if description is not None:
            category.description = description

        category.save()

        return Response().json(
            {
                "id": category.id,
                "name": category.name,
                "slug": category.slug,
                "description": category.description,
            }
        )
    except Category.DoesNotExist:
        return Response().status_code(404).json({"error": "Category not found"})


@router.delete("api/categories/<int:category_id>")
@SwaggerUI.doc(summary="Delete category", tags=["Categories"])
def delete_category(req, category_id):
    """Delete category"""
    # Auth required (admin only)
    auth_response = auth_required(req)
    if auth_response:
        return auth_response

    if not req.user.is_staff:
        return Response().status_code(403).json({"error": "Admin access required"})

    try:
        category = Category.objects.get(id=category_id)
        category.delete()
        return Response().json({"message": "Category deleted"})
    except Category.DoesNotExist:
        return Response().status_code(404).json({"error": "Category not found"})
