"""Built-in caching for Shanks - Auto-cache GET requests"""

import hashlib
import json
import time
from functools import wraps


class SimpleCache:
    """Simple in-memory cache with TTL"""

    def __init__(self):
        self._cache = {}
        self._timestamps = {}
        self._path_to_keys = {}  # Map paths to their cache keys

    def get(self, key):
        """Get value from cache if not expired"""
        if key in self._cache:
            timestamp = self._timestamps.get(key, 0)
            if time.time() - timestamp < self._cache[key]["ttl"]:
                return self._cache[key]["value"]
            else:
                # Expired, remove
                del self._cache[key]
                del self._timestamps[key]
                # Clean up path mapping
                for path, keys in list(self._path_to_keys.items()):
                    if key in keys:
                        keys.discard(key)
                        if not keys:
                            del self._path_to_keys[path]
        return None

    def set(self, key, value, ttl=300, path=None):
        """Set value in cache with TTL (default 5 minutes)"""
        self._cache[key] = {"value": value, "ttl": ttl}
        self._timestamps[key] = time.time()
        # Track which path this key belongs to
        if path:
            if path not in self._path_to_keys:
                self._path_to_keys[path] = set()
            self._path_to_keys[path].add(key)

    def delete(self, key):
        """Delete key from cache"""
        if key in self._cache:
            del self._cache[key]
            del self._timestamps[key]
            # Clean up path mapping
            for path, keys in list(self._path_to_keys.items()):
                if key in keys:
                    keys.discard(key)
                    if not keys:
                        del self._path_to_keys[path]

    def clear(self):
        """Clear all cache"""
        self._cache.clear()
        self._timestamps.clear()
        self._path_to_keys.clear()

    def invalidate_pattern(self, pattern):
        """Invalidate all keys for paths matching pattern"""
        keys_to_delete = set()
        for path, keys in list(self._path_to_keys.items()):
            if pattern in path:
                keys_to_delete.update(keys)
        for key in keys_to_delete:
            self.delete(key)


# Global cache instance
_cache = SimpleCache()


def get_cache():
    """Get global cache instance"""
    return _cache


def cache_key(request):
    """Generate cache key from request"""
    # Handle both Shanks Request wrapper and Django request
    if hasattr(request, "django"):
        # Shanks Request wrapper
        django_request = request.django
    else:
        # Direct Django request
        django_request = request

    # Include method, path, and query params
    key_parts = [
        django_request.method,
        django_request.path,
        json.dumps(dict(django_request.GET), sort_keys=True),
    ]
    key_string = "|".join(key_parts)
    return hashlib.md5(key_string.encode()).hexdigest()


def cache(ttl=300, methods=None):
    """
    Decorator to cache endpoint responses

    Args:
        ttl: Time to live in seconds (default 5 minutes)
        methods: List of HTTP methods to cache (default: ['GET'])

    Example:
        @app.get("api/posts")
        @cache(ttl=600)  # Cache for 10 minutes
        def list_posts(req):
            return {"posts": [...]}
    """
    if methods is None:
        methods = ["GET"]

    def decorator(func):
        @wraps(func)
        def wrapper(request, *args, **kwargs):
            # Only cache specified methods
            if request.method not in methods:
                return func(request, *args, **kwargs)

            # Generate cache key
            key = cache_key(request)

            # Try to get from cache
            cached = _cache.get(key)
            if cached is not None:
                return cached

            # Execute function
            response = func(request, *args, **kwargs)

            # Cache the response
            _cache.set(key, response, ttl)

            return response

        return wrapper

    return decorator


def auto_cache(req, res, next):
    """
    Middleware for automatic caching of GET requests

    Usage in routes/__init__.py:
        from shanks import auto_cache
        app.use(auto_cache)
    """
    # Only cache GET requests
    if req.method != "GET":
        return next()

    # Generate cache key
    key = cache_key(req)

    # Try to get from cache
    cached = _cache.get(key)
    if cached is not None:
        # Add cache header
        if hasattr(res, "headers"):
            res.headers["X-Cache"] = "HIT"
        return cached

    # Execute next middleware/handler
    result = next()
    
    # Cache the response with path for invalidation
    if result is not None:
        _cache.set(key, result, ttl=300, path=req.path)  # Pass path for tracking
    
    return result


def invalidate_cache(pattern=None):
    """
    Invalidate cache entries

    Args:
        pattern: Pattern to match (None = clear all)

    Example:
        # Clear all cache
        invalidate_cache()

        # Clear specific pattern
        invalidate_cache("/api/posts")
    """
    if pattern is None:
        _cache.clear()
    else:
        _cache.invalidate_pattern(pattern)


# Smart cache invalidation middleware
def smart_cache_invalidation(req, res, next):
    """
    Middleware to auto-invalidate cache on POST/PUT/DELETE

    Usage:
        app.use(smart_cache_invalidation)
    """
    # Execute the handler first
    result = next()
    
    # Invalidate cache AFTER successful write operations
    if req.method in ["POST", "PUT", "PATCH", "DELETE"]:
        # Extract base resource path (e.g., /api/posts/123 -> /api/posts)
        path = req.path
        # Remove trailing ID if present (e.g., /api/posts/123 -> /api/posts)
        path_parts = path.rstrip("/").split("/")
        if path_parts and path_parts[-1].isdigit():
            base_path = "/".join(path_parts[:-1])
        else:
            base_path = path
        
        # Invalidate all cache entries for this resource
        invalidate_cache(base_path)

    return result


__all__ = [
    "cache",
    "auto_cache",
    "invalidate_cache",
    "smart_cache_invalidation",
    "get_cache",
]
