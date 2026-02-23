"""Comment DTOs"""


class CommentDTO:
    """Comment response DTO"""

    def __init__(self, comment):
        self.id = comment.id
        self.content = comment.content
        self.author = {
            "id": comment.author.id,
            "username": comment.author.username,
        }
        self.post_id = comment.post.id
        self.created_at = comment.created_at.isoformat()
        self.updated_at = comment.updated_at.isoformat()

    def to_dict(self):
        return {
            "id": self.id,
            "content": self.content,
            "author": self.author,
            "post_id": self.post_id,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }


class CommentCreateDTO:
    """Comment creation DTO"""

    def __init__(self, data: dict):
        self.content = data.get("content")

    def validate(self):
        errors = []
        if not self.content:
            errors.append("Content is required")
        return errors
