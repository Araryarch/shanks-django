"""Like model"""

from shanks import CASCADE, DateTimeField, ForeignKey, Model

from .post import Post


class Like(Model):
    user = ForeignKey("auth.User", on_delete=CASCADE, related_name="likes")
    post = ForeignKey(Post, on_delete=CASCADE, related_name="likes")
    created_at = DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ["user", "post"]
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.username} likes {self.post.title}"
