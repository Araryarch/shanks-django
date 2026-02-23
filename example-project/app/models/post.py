"""Post model"""

from shanks import (CASCADE, SET_NULL, CharField, DateTimeField, ForeignKey,
                    ManyToManyField, Model, SlugField, TextField, User,
                    slugify)

from .category import Category
from .tag import Tag


class Post(Model):
    title = CharField(max_length=200)
    slug = SlugField(unique=True, blank=True)
    content = TextField()
    excerpt = TextField(blank=True)
    author = ForeignKey(User, on_delete=CASCADE, related_name="posts")
    category = ForeignKey(
        Category, on_delete=SET_NULL, null=True, blank=True, related_name="posts"
    )
    tags = ManyToManyField(Tag, blank=True, related_name="posts")
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
