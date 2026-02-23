"""Category model"""

from shanks import CharField, DateTimeField, Model, SlugField, TextField


class Category(Model):
    name = CharField(max_length=100, unique=True)
    slug = SlugField(unique=True)
    description = TextField(blank=True)
    created_at = DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ["name"]

    def __str__(self):
        return self.name
