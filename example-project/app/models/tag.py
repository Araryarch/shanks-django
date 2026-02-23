"""Tag model"""

from shanks import CharField, DateTimeField, Model, SlugField


class Tag(Model):
    name = CharField(max_length=50, unique=True)
    slug = SlugField(unique=True)
    created_at = DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name
