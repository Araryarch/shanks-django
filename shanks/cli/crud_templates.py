"""CRUD generation templates"""


def get_entity_template(model_name, endpoint_name):
    """Entity (Django model) template"""
    return f"""from shanks import Model, CharField, TextField, ForeignKey, DateTimeField, CASCADE


class {model_name}(Model):
    title = CharField(max_length=200)
    description = TextField(blank=True)
    created_by = ForeignKey('auth.User', on_delete=CASCADE, related_name='{endpoint_name}_created')
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    class Meta:
        db_table = '{endpoint_name}'
        ordering = ['-created_at']

    def __str__(self):
        return self.title
"""


def get_repository_template(model_name, endpoint_name, operations=None):
    """Repository (data access) template"""
    if operations is None:
        operations = {"create": True, "read": True, "update": True, "delete": True}
    
    functions = []
    
    if operations.get("read"):
        functions.append('''def find_all(page=1, limit=10):
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
        return None'''.format(model_name=model_name))
    
    if operations.get("create"):
        functions.append('''def create_item(title, description, user):
    """Create new item"""
    return {model_name}.objects.create(
        title=title,
        description=description,
        created_by=user
    )'''.format(model_name=model_name))
    
    if operations.get("update"):
        functions.append('''def update_item(item, title=None, description=None):
    """Update existing item"""
    if title is not None:
        item.title = title
    if description is not None:
        item.description = description
    item.save()''')
    
    if operations.get("delete"):
        functions.append('''def delete_item(item):
    """Delete item"""
    item.delete()''')
    
    return f'''"""
{model_name} Repository - Data Access Layer
"""
from db.entity.{endpoint_name}_entity import {model_name}


{chr(10).join([chr(10) + chr(10) + f for f in functions])}
'''


def get_service_template(model_name, endpoint_name, endpoint_plural, operations=None):
    """Service (business logic) template"""
    if operations is None:
        operations = {"create": True, "read": True, "update": True, "delete": True}
    
    functions = []
    
    if operations.get("read"):
        functions.append(f'''def get_{endpoint_plural}_list(page=1, limit=10):
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
    }}''')
    
    if operations.get("create"):
        functions.append(f'''def create_{endpoint_name}(title, description, user):
    """Create new item"""
    item = {endpoint_name}_repository.create_item(title, description, user)
    return {{"id": item.id, "message": "Created successfully"}}''')
    
    if operations.get("update"):
        functions.append(f'''def update_{endpoint_name}(item_id, title=None, description=None):
    """Update existing item"""
    item = {endpoint_name}_repository.find_by_id(item_id)
    if not item:
        return None
    
    {endpoint_name}_repository.update_item(item, title, description)
    return {{"message": "Updated successfully"}}''')
    
    if operations.get("delete"):
        functions.append(f'''def delete_{endpoint_name}(item_id):
    """Delete item"""
    item = {endpoint_name}_repository.find_by_id(item_id)
    if not item:
        return None
    
    {endpoint_name}_repository.delete_item(item)
    return {{"message": "Deleted successfully"}}''')
    
    return f'''"""
{model_name} Service - Business Logic Layer
"""
from internal.repository import {endpoint_name}_repository


{(chr(10) + chr(10) + chr(10)).join(functions)}
'''


def get_controller_template(model_name, endpoint_name, endpoint_plural, operations=None):
    """Controller (request handler) template"""
    if operations is None:
        operations = {"create": True, "read": True, "update": True, "delete": True}
    
    functions = []
    
    if operations.get("read"):
        functions.append(f'''def list_{endpoint_plural}(req):
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
    
    return BaseDTO.success(data=result)''')
    
    if operations.get("create"):
        functions.append(f'''def create(req):
    """Handle create request"""
    data = req.body
    title = data.get("title")
    description = data.get("description", "")
    
    if not title:
        return BaseDTO.error(message="Title is required", status=400)
    
    # Check if user is authenticated (user_id is set by auth middleware)
    if not hasattr(req, 'user_id'):
        return BaseDTO.error(message="Authentication required", status=401)
    
    result = {endpoint_name}_service.create_{endpoint_name}(title, description, req.user)
    return BaseDTO.success(data=result, message="Created successfully", status=201)''')
    
    if operations.get("update"):
        functions.append(f'''def update(req, id):
    """Handle update request"""
    data = req.body
    title = data.get("title")
    description = data.get("description")
    
    result = {endpoint_name}_service.update_{endpoint_name}(id, title, description)
    
    if result is None:
        return BaseDTO.error(message="Not found", status=404)
    
    return BaseDTO.success(data=result, message="Updated successfully")''')
    
    if operations.get("delete"):
        functions.append(f'''def delete(req, id):
    """Handle delete request"""
    result = {endpoint_name}_service.delete_{endpoint_name}(id)
    
    if result is None:
        return BaseDTO.error(message="Not found", status=404)
    
    return BaseDTO.success(data=result, message="Deleted successfully")''')
    
    return f'''"""
{model_name} Controller - Request/Response Handler
"""
from internal.service import {endpoint_name}_service
from dto.base_dto import BaseDTO


{(chr(10) + chr(10) + chr(10)).join(functions)}
'''


def get_route_template(model_name, endpoint_name, endpoint_plural, operations=None, require_auth=False):
    """Route template"""
    if operations is None:
        operations = {"create": True, "read": True, "update": True, "delete": True}
    
    # Build imports
    imports = [f"from shanks import App", f"from internal.controller import {endpoint_name}_controller"]
    if require_auth:
        imports.append("from internal.middleware.auth_middleware import jwt_auth_middleware")
    
    # Build routes
    routes = []
    
    if operations.get("read"):
        routes.append(f'''@router.get('/')
def list_{endpoint_plural}_route(req):
    return {endpoint_name}_controller.list_{endpoint_plural}(req)

@router.get('/<id>')
def get_{endpoint_name}_route(req, id):
    return {endpoint_name}_controller.get_by_id(req, id)''')
    
    if operations.get("create"):
        routes.append(f'''@router.post('/')
def create_{endpoint_name}_route(req):
    return {endpoint_name}_controller.create(req)''')
    
    if operations.get("update"):
        routes.append(f'''@router.put('/<id>')
def update_{endpoint_name}_route(req, id):
    return {endpoint_name}_controller.update(req, id)''')
    
    if operations.get("delete"):
        routes.append(f'''@router.delete('/<id>')
def delete_{endpoint_name}_route(req, id):
    return {endpoint_name}_controller.delete(req, id)''')
    
    # Build middleware line
    middleware_line = ""
    if require_auth:
        middleware_line = "\n# Apply auth middleware to protect all operations\nrouter.use(jwt_auth_middleware)\n"
    
    return f'''"""
{model_name} Routes
"""
{chr(10).join(imports)}

# Group all {endpoint_name} routes under /api/v1/{endpoint_plural}
router = App(prefix='/api/v1/{endpoint_plural}')
{middleware_line}
{(chr(10) + chr(10)).join(routes)}
'''
