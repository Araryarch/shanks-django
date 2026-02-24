"""JSON-like schema for defining models - Super simple!"""

from django.db import models


class Schema:
    """Define models with JSON-like syntax"""

    @staticmethod
    def model(name, fields, options=None):
        """
        Create a Django model from JSON-like schema

        Example:
            Post = Schema.model("Post", {
                "title": "string",
                "content": "text",
                "published": "boolean",
                "views": "integer",
                "author": {"type": "relation", "model": "User"},
                "created_at": "datetime"
            })
        """
        import inspect

        # Get the calling module to set app_label correctly
        frame = inspect.currentframe().f_back
        module = inspect.getmodule(frame)
        module_name = module.__name__ if module else "app"

        # Extract app name from module path (e.g., "entity.products" -> "entity")
        app_label = module_name.split(".")[0] if "." in module_name else module_name

        attrs = {"__module__": module_name}

        # Add Meta class
        meta_attrs = {"app_label": app_label}

        if options:
            if "table" in options:
                meta_attrs["db_table"] = options["table"]
            if "ordering" in options:
                meta_attrs["ordering"] = options["ordering"]

        attrs["Meta"] = type("Meta", (), meta_attrs)

        # Convert JSON-like fields to Django fields
        for field_name, field_def in fields.items():
            attrs[field_name] = Schema._create_field(field_def)

        # Create model class with Prisma-like methods
        model_class = type(name, (models.Model,), attrs)

        # Add Prisma-like methods
        Schema._add_prisma_methods(model_class)

        return model_class

    @staticmethod
    def _create_field(field_def):
        """Convert JSON field definition to Django field"""
        # Simple string type
        if isinstance(field_def, str):
            return Schema._parse_field_string(field_def)

        # Dict with options
        if isinstance(field_def, dict):
            field_type = field_def.get("type")
            options = {k: v for k, v in field_def.items() if k != "type"}

            # Handle relations
            if field_type == "relation":
                model = options.pop("model")
                on_delete = options.pop("on_delete", models.CASCADE)
                return models.ForeignKey(model, on_delete=on_delete, **options)

            if field_type == "many":
                model = options.pop("model")
                return models.ManyToManyField(model, **options)

            # Regular field with options
            field_class = Schema._get_field_by_type(field_type)
            return field_class(**options)

        return field_def

    @staticmethod
    def _parse_field_string(field_str):
        """
        Parse field string like 'string:100:unique' or 'number:auto_now_add'
        JavaScript-like types: string, number, boolean, date
        """
        parts = field_str.split(":")
        field_type = parts[0]
        options = {}

        # Parse options from string
        for part in parts[1:]:
            if part.isdigit():
                options["max_length"] = int(part)
            elif part == "unique":
                options["unique"] = True
            elif part == "blank":
                options["blank"] = True
            elif part == "null":
                options["null"] = True
            elif part == "auto_now":
                options["auto_now"] = True
            elif part == "auto_now_add":
                options["auto_now_add"] = True

        # Get field class
        field_class = Schema._get_field_class_by_type(field_type)

        # Create field instance
        if field_class:
            return field_class(**options)

        return models.CharField(max_length=255)

    @staticmethod
    def _get_field_class_by_type(field_type):
        """Get Django field class by JavaScript-like type string"""
        type_map = {
            # JavaScript-like types
            "string": models.CharField,
            "number": models.IntegerField,
            "boolean": models.BooleanField,
            "date": models.DateTimeField,
            # Additional types
            "text": models.TextField,
            "float": models.FloatField,
            "email": models.EmailField,
            "url": models.URLField,
            "slug": models.SlugField,
            "json": models.JSONField,
        }
        return type_map.get(field_type)

    @staticmethod
    def _get_field_by_type(field_type):
        """Get Django field class by type string (legacy)"""
        type_map = {
            "string": models.CharField(max_length=255),
            "text": models.TextField(),
            "number": models.IntegerField(),
            "integer": models.IntegerField(),
            "float": models.FloatField(),
            "boolean": models.BooleanField(default=False),
            "date": models.DateTimeField(auto_now_add=True),
            "datetime": models.DateTimeField(auto_now_add=True),
            "email": models.EmailField(),
            "url": models.URLField(),
            "slug": models.SlugField(),
            "json": models.JSONField(),
        }
        return type_map.get(field_type, models.CharField(max_length=255))

    @staticmethod
    def _add_prisma_methods(model_class):
        """Add Prisma-like methods to model"""

        @classmethod
        def find_many(cls, **filters):
            return cls.objects.filter(**filters)

        @classmethod
        def find_first(cls, **filters):
            return cls.objects.filter(**filters).first()

        @classmethod
        def find_unique(cls, **filters):
            try:
                return cls.objects.get(**filters)
            except cls.DoesNotExist:
                return None

        @classmethod
        def create(cls, **data):
            return cls.objects.create(**data)

        @classmethod
        def count(cls, **filters):
            if filters:
                return cls.objects.filter(**filters).count()
            return cls.objects.count()

        def update_self(self, **data):
            for key, value in data.items():
                setattr(self, key, value)
            self.save()
            return self

        def delete_self(self):
            self.delete()

        # Attach methods
        model_class.find_many = find_many
        model_class.find_first = find_first
        model_class.find_unique = find_unique
        model_class.create = create
        model_class.count = count
        model_class.update_self = update_self
        model_class.delete_self = delete_self


# Shorthand function
def model(name, fields, options=None):
    """Shorthand for Schema.model()"""
    return Schema.model(name, fields, options)
