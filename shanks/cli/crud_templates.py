"""CRUD generation templates"""


def get_entity_template(model_name, endpoint_name):
    """Entity (Django model) template"""
    return f'''from django.db import models
from django.contrib.auth.models import User


class {model_name}(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='{endpoint_name}_created')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = '{endpoint_name}'
        ordering = ['-created_at']

    def __str__(self):
        return self.title
'''


def get_repository_template(model_name, endpoint_name):
    """Repository (data access) template"""
    return f'''"""
{model_name} Repository - Data Access Layer
"""
from db.entity.{endpoint_name}_entity import {model_name}


def find_all(page=1, limit=10):
    """Get paginated list"""
    offset = (page - 1) * limit
    items = {model_name}.objects.all()[offset:offset + limit]
    total = {model_name}.objects.count()
    return items, total


def find_by_id(item_id):
    """Get single item by ID"""
    try:
        return {model_name}.objects.get(id=item_id)
    except {model_name}.DoesNotExist:
        return None


def create_item(title, description, user):
    """Create new item"""
    return {model_name}.objects.create(
        title=title,
        description=description,
        created_by=user
    )


def update_item(item, title=None, description=None):
    """Update existing item"""
    if title is not None:
        item.title = title
    if description is not None:
        item.description = description
    item.save()


def delete_item(item):
    """Delete item"""
    item.delete()
'''


def get_service_template(model_name, endpoint_name, endpoint_plural):
    """Service (business logic) template"""
    return f'''"""
{model_name} Service - Business Logic Layer
"""
from internal.repository import {endpoint_name}_repository


def get_{endpoint_plural}_list(page=1, limit=10):
    """Get paginated list of items"""
    items, total = {endpoint_name}_repository.find_all(page, limit)
    
    return {{
        "data": [
            {{
                "id": item.id,
                "title": item.title,
                "description": item.description,
                "created_at": item.created_at.isoformat(),
                "updated_at": item.updated_at.isoformat(),
            }}
            for item in items
        ],
        "pagination": {{
            "page": page,
            "limit": limit,
            "total": total,
            "pages": (total + limit - 1) // limit
        }}
    }}


def get_{endpoint_name}_by_id(item_id):
    """Get single item by ID"""
    item = {endpoint_name}_repository.find_by_id(item_id)
    if not item:
        return None
    
    return {{
        "id": item.id,
        "title": item.title,
        "description": item.description,
        "created_at": item.created_at.isoformat(),
        "updated_at": item.updated_at.isoformat(),
        "created_by": {{
            "id": item.created_by.id,
            "username": item.created_by.username
        }}
    }}


def create_{endpoint_name}(title, description, user):
    """Create new item"""
    item = {endpoint_name}_repository.create_item(title, description, user)
    return {{"id": item.id, "message": "Created successfully"}}


def update_{endpoint_name}(item_id, title=None, description=None):
    """Update existing item"""
    item = {endpoint_name}_repository.find_by_id(item_id)
    if not item:
        return None
    
    {endpoint_name}_repository.update_item(item, title, description)
    return {{"message": "Updated successfully"}}


def delete_{endpoint_name}(item_id):
    """Delete item"""
    item = {endpoint_name}_repository.find_by_id(item_id)
    if not item:
        return None
    
    {endpoint_name}_repository.delete_item(item)
    return {{"message": "Deleted successfully"}}
'''


def get_controller_template(model_name, endpoint_name, endpoint_plural):
    """Controller (request handler) template"""
    return f'''"""
{model_name} Controller - Request/Response Handler
"""
from internal.service import {endpoint_name}_service
from dto.base_dto import BaseDTO


def list_{endpoint_plural}(req):
    """Handle list request"""
    page = int(req.query.get("page", 1))
    limit = int(req.query.get("limit", 10))
    
    result = {endpoint_name}_service.get_{endpoint_plural}_list(page, limit)
    return BaseDTO.success(
        data=result["data"],
        pagination=result["pagination"]
    )


def get_by_id(req, id):
    """Handle get by ID request"""
    result = {endpoint_name}_service.get_{endpoint_name}_by_id(id)
    
    if result is None:
        return BaseDTO.error(message="Not found", status=404)
    
    return BaseDTO.success(data=result)


def create(req):
    """Handle create request"""
    if not req.user.is_authenticated:
        return BaseDTO.error(message="Authentication required", status=401)
    
    data = req.body
    title = data.get("title")
    description = data.get("description", "")
    
    if not title:
        return BaseDTO.error(message="Title is required", status=400)
    
    result = {endpoint_name}_service.create_{endpoint_name}(title, description, req.user)
    return BaseDTO.success(data=result, message="Created successfully", status=201)


def update(req, id):
    """Handle update request"""
    if not req.user.is_authenticated:
        return BaseDTO.error(message="Authentication required", status=401)
    
    data = req.body
    title = data.get("title")
    description = data.get("description")
    
    result = {endpoint_name}_service.update_{endpoint_name}(id, title, description)
    
    if result is None:
        return BaseDTO.error(message="Not found", status=404)
    
    return BaseDTO.success(data=result, message="Updated successfully")


def delete(req, id):
    """Handle delete request"""
    if not req.user.is_authenticated:
        return BaseDTO.error(message="Authentication required", status=401)
    
    result = {endpoint_name}_service.delete_{endpoint_name}(id)
    
    if result is None:
        return BaseDTO.error(message="Not found", status=404)
    
    return BaseDTO.success(data=result, message="Deleted successfully")
'''


def get_route_template(model_name, endpoint_name, endpoint_plural):
    """Route template"""
    return f'''"""
{model_name} Routes
"""
from shanks import App
from internal.controller import {endpoint_name}_controller

router = App()


@router.get('/api/{endpoint_plural}')
def list_{endpoint_plural}_route(req):
    return {endpoint_name}_controller.list_{endpoint_plural}(req)


@router.get('/api/{endpoint_plural}/<id>')
def get_{endpoint_name}_route(req, id):
    return {endpoint_name}_controller.get_by_id(req, id)


@router.post('/api/{endpoint_plural}')
def create_{endpoint_name}_route(req):
    return {endpoint_name}_controller.create(req)


@router.put('/api/{endpoint_plural}/<id>')
def update_{endpoint_name}_route(req, id):
    return {endpoint_name}_controller.update(req, id)


@router.delete('/api/{endpoint_plural}/<id>')
def delete_{endpoint_name}_route(req, id):
    return {endpoint_name}_controller.delete(req, id)
'''
