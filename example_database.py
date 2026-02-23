"""Example: Database connections with Shanks Django"""

from shanks import App, Response, DatabaseConfig, MongoDB, Redis

app = App()

# ============================================
# Django ORM Examples (PostgreSQL/MySQL/SQLite)
# ============================================

# In settings.py, use DatabaseConfig:
"""
from shanks import DatabaseConfig

# PostgreSQL
DATABASES = {
    'default': DatabaseConfig.postgres(
        host='localhost',
        database='mydb',
        user='myuser',
        password='mypass'
    )
}

# MySQL
DATABASES = {
    'default': DatabaseConfig.mysql(
        host='localhost',
        database='mydb',
        user='root',
        password='mypass'
    )
}

# SQLite
DATABASES = {
    'default': DatabaseConfig.sqlite('db.sqlite3')
}

# From environment variable
import os
DATABASES = {
    'default': DatabaseConfig.from_url(os.getenv('DATABASE_URL'))
}
"""

# Django ORM usage in views
from django.db import models


class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)


@app.get("api/users")
def get_users(req):
    """Get all users from PostgreSQL/MySQL/SQLite"""
    users = User.objects.all()
    return {"users": list(users.values())}


@app.post("api/users")
def create_user(req):
    """Create user in PostgreSQL/MySQL/SQLite"""
    user = User.objects.create(name=req.body.get("name"), email=req.body.get("email"))
    return Response().status_code(201).json({"id": user.id, "name": user.name})


# ============================================
# MongoDB Examples
# ============================================

# Connect to MongoDB (call this in your app startup)
"""
from shanks import MongoDB

# Simple connection
MongoDB.connect(
    host='localhost',
    database='mydb',
    username='user',
    password='pass'
)

# Or using URI
MongoDB.connect_uri(
    'mongodb://user:pass@localhost:27017',
    'mydb'
)
"""


@app.get("api/mongo/users")
def get_mongo_users(req):
    """Get users from MongoDB"""
    try:
        users = list(MongoDB.db.users.find({}, {"_id": 0}))
        return {"users": users}
    except RuntimeError as e:
        return Response().status_code(500).json({"error": str(e)})


@app.post("api/mongo/users")
def create_mongo_user(req):
    """Create user in MongoDB"""
    try:
        user_data = {"name": req.body.get("name"), "email": req.body.get("email")}
        result = MongoDB.db.users.insert_one(user_data)
        return (
            Response()
            .status_code(201)
            .json({"id": str(result.inserted_id), "user": user_data})
        )
    except RuntimeError as e:
        return Response().status_code(500).json({"error": str(e)})


@app.get("api/mongo/users/<name>")
def get_mongo_user(req, name):
    """Get specific user from MongoDB"""
    try:
        user = MongoDB.db.users.find_one({"name": name}, {"_id": 0})
        if user:
            return {"user": user}
        return Response().status_code(404).json({"error": "User not found"})
    except RuntimeError as e:
        return Response().status_code(500).json({"error": str(e)})


# ============================================
# Redis Examples
# ============================================

# Connect to Redis (call this in your app startup)
"""
from shanks import Redis

# Simple connection
Redis.connect(
    host='localhost',
    password='mypass'
)

# Or using URL
Redis.connect_url('redis://:password@localhost:6379/0')
"""


@app.get("api/cache/<key>")
def get_cache(req, key):
    """Get value from Redis cache"""
    try:
        value = Redis.client.get(key)
        if value:
            return {"key": key, "value": value}
        return Response().status_code(404).json({"error": "Key not found"})
    except RuntimeError as e:
        return Response().status_code(500).json({"error": str(e)})


@app.post("api/cache")
def set_cache(req):
    """Set value in Redis cache"""
    try:
        key = req.body.get("key")
        value = req.body.get("value")
        ttl = req.body.get("ttl")  # Time to live in seconds

        if ttl:
            Redis.client.setex(key, ttl, value)
        else:
            Redis.client.set(key, value)

        return {"success": True, "key": key}
    except RuntimeError as e:
        return Response().status_code(500).json({"error": str(e)})


@app.delete("api/cache/<key>")
def delete_cache(req, key):
    """Delete key from Redis cache"""
    try:
        Redis.client.delete(key)
        return {"success": True, "deleted": key}
    except RuntimeError as e:
        return Response().status_code(500).json({"error": str(e)})


# ============================================
# Mixed Database Example
# ============================================


@app.post("api/register")
def register_user(req):
    """
    Register user with multiple databases:
    - Store user in PostgreSQL (Django ORM)
    - Cache user data in Redis
    - Store user activity in MongoDB
    """
    name = req.body.get("name")
    email = req.body.get("email")

    # Save to PostgreSQL
    user = User.objects.create(name=name, email=email)

    # Cache in Redis
    try:
        Redis.client.setex(f"user:{user.id}", 3600, f"{name}:{email}")
    except RuntimeError:
        pass  # Redis not connected

    # Log activity in MongoDB
    try:
        MongoDB.db.activities.insert_one(
            {"user_id": user.id, "action": "register", "email": email}
        )
    except RuntimeError:
        pass  # MongoDB not connected

    return Response().status_code(201).json({"id": user.id, "name": name})


urlpatterns = app.get_urls()
