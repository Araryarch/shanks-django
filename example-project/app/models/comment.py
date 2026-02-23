"""Comment model"""

from shanks import CASCADE, DateTimeField, ForeignKey, Model, TextField, User

from .post import Post


class Comment(Model):
    content = TextField()
    author = ForeignKey(User, on_delete=CASCADE, related_name="comments")
    post = ForeignKey(Post, on_delete=CASCADE, related_name="comments")
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Comment by {self.author.username} on {self.post.title}"
