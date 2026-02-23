"""Post DTOs"""


class PostDTO:
    """Post response DTO"""

    def __init__(self, post):
        self.id = post.id
        self.title = post.title
        self.slug = post.slug
        self.content = post.content
        self.excerpt = post.excerpt
        self.author = {
            "id": post.author.id,
            "username": post.author.username,
        }
        self.category = (
            {"id": post.category.id, "name": post.category.name}
            if post.category
            else None
        )
        self.tags = [{"id": tag.id, "name": tag.name} for tag in post.tags.all()]
        self.likes_count = post.likes.count()
        self.comments_count = post.comments.count()
        self.created_at = post.created_at.isoformat()
        self.updated_at = post.updated_at.isoformat()

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "slug": self.slug,
            "content": self.content,
            "excerpt": self.excerpt,
            "author": self.author,
            "category": self.category,
            "tags": self.tags,
            "likes_count": self.likes_count,
            "comments_count": self.comments_count,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }


class PostCreateDTO:
    """Post creation DTO"""

    def __init__(self, data: dict):
        self.title = data.get("title")
        self.content = data.get("content")
        self.excerpt = data.get("excerpt", "")
        self.category_id = data.get("category_id")
        self.tag_ids = data.get("tag_ids", [])

    def validate(self):
        errors = []
        if not self.title:
            errors.append("Title is required")
        if not self.content:
            errors.append("Content is required")
        return errors


class PostUpdateDTO:
    """Post update DTO"""

    def __init__(self, data: dict):
        self.title = data.get("title")
        self.content = data.get("content")
        self.excerpt = data.get("excerpt")
        self.category_id = data.get("category_id")
        self.tag_ids = data.get("tag_ids")
