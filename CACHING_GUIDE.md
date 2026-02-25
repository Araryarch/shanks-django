# Caching Guide

Shanks has built-in caching that's **enabled by default** for all GET requests. No configuration needed!

## Auto-Caching (Default Behavior)

```python
from shanks import App

# Cache is automatically enabled!
app = App()

@app.get('api/posts')
def list_posts(req):
    # First request: Fetches from database, caches result
    # Subsequent requests: Served from cache (10x faster!)
    posts = Post.find_many()
    return {'posts': [...]}

@app.post('api/posts')
def create_post(req):
    # Automatically invalidates /api/posts cache
    post = Post.create(**req.body)
    return {'id': post.id}
```

## How It Works

1. **First GET request**: Fetches data from database, stores in cache
2. **Subsequent GET requests**: Returns cached data (10x faster!)
3. **Write operations** (POST/PUT/DELETE): Automatically invalidate related cache
4. **Cache expiry**: Data expires after TTL (default 5 minutes)

## Disable Cache

### For Entire App

```python
app = App(enable_cache=False)  # No caching at all
```

### For Specific Group

```python
app = App()  # Cache enabled

# Disable cache for realtime endpoints
realtime = app.group('api/realtime')
realtime.disable_cache()

@realtime.get('updates')
def get_updates(req):
    # This endpoint is NOT cached
    return {'updates': [...]}
```

## Customize Cache Settings

### Change TTL (Time To Live)

```python
# Cache for 10 minutes instead of default 5
app.cache_config(ttl=600)

# Cache for 1 hour
app.cache_config(ttl=3600)

# Cache for 30 seconds (for frequently changing data)
app.cache_config(ttl=30)
```

### Different TTL per Group

```python
app = App()

# API v1: Cache for 1 minute (frequently updated)
api_v1 = app.group('api/v1')
api_v1.cache_config(ttl=60)

# API v2: Cache for 10 minutes (stable data)
api_v2 = app.group('api/v2')
api_v2.cache_config(ttl=600)

# Static data: Cache for 1 hour
static = app.group('api/static')
static.cache_config(ttl=3600)
```

### Cache Specific Methods

```python
# Cache GET and HEAD requests
app.cache_config(ttl=300, methods=['GET', 'HEAD'])

# Only cache GET (default)
app.cache_config(ttl=300, methods=['GET'])
```

## Manual Cache Control

### Invalidate Cache

```python
from shanks import invalidate_cache

# Clear all cache
invalidate_cache()

# Clear specific pattern
invalidate_cache('/api/posts')
invalidate_cache('/api/users')

# In your endpoint
@app.delete('api/posts/<id>')
def delete_post(req, id):
    post = Post.find_unique(id=id)
    post.delete_self()
    
    # Manually invalidate cache
    invalidate_cache('/api/posts')
    
    return {'deleted': True}
```

### Direct Cache Access

```python
from shanks import get_cache

cache = get_cache()

# Set value
cache.set('my_key', {'data': 'value'}, ttl=300)

# Get value
value = cache.get('my_key')

# Delete value
cache.delete('my_key')

# Clear all
cache.clear()

# Invalidate pattern
cache.invalidate_pattern('/api/posts')
```

## Smart Cache Invalidation

Shanks automatically invalidates cache on write operations:

```python
# GET /api/posts -> Cached
# POST /api/posts -> Invalidates /api/posts cache
# PUT /api/posts/123 -> Invalidates /api/posts cache
# DELETE /api/posts/123 -> Invalidates /api/posts cache
```

Pattern matching:
- `/api/posts/123` → invalidates `/api/posts`
- `/api/users/456/posts` → invalidates `/api/users/456/posts`

## Per-Endpoint Cache (Advanced)

If you need different cache settings per endpoint:

```python
from shanks import cache

app = App()

# This endpoint uses default cache (5 minutes)
@app.get('api/posts')
def list_posts(req):
    return {'posts': [...]}

# This endpoint has custom cache (10 minutes)
@app.get('api/categories')
@cache(ttl=600)
def list_categories(req):
    return {'categories': [...]}

# This endpoint has no cache
@app.get('api/realtime')
@cache(ttl=0)  # TTL=0 means no cache
def realtime_data(req):
    return {'data': [...]}
```

## Best Practices

### 1. Use Default Cache for Most Endpoints

```python
# Just create the app, cache is enabled!
app = App()

@app.get('api/posts')
def list_posts(req):
    return {'posts': Post.find_many()}
```

### 2. Disable Cache for Realtime Data

```python
realtime = app.group('api/realtime')
realtime.disable_cache()

@realtime.get('updates')
def get_updates(req):
    return {'updates': get_live_updates()}
```

### 3. Different TTL for Different Data Types

```python
# Frequently changing data: Short TTL
trending = app.group('api/trending')
trending.cache_config(ttl=60)  # 1 minute

# Stable data: Long TTL
static = app.group('api/static')
static.cache_config(ttl=3600)  # 1 hour

# User-specific data: No cache
user_data = app.group('api/user')
user_data.disable_cache()
```

### 4. Manual Invalidation for Complex Operations

```python
@app.post('api/posts/<id>/publish')
def publish_post(req, id):
    post = Post.find_unique(id=id)
    post.update_self(published=True)
    
    # Invalidate multiple caches
    invalidate_cache('/api/posts')
    invalidate_cache('/api/published')
    invalidate_cache(f'/api/posts/{id}')
    
    return {'published': True}
```

## Performance Benefits

With caching enabled:

- **First request**: ~100ms (database query)
- **Cached requests**: ~10ms (memory read)
- **10x faster** response times!

Example benchmark:
```
Without cache:
  GET /api/posts -> 120ms
  GET /api/posts -> 115ms
  GET /api/posts -> 118ms

With cache:
  GET /api/posts -> 120ms (first request, cached)
  GET /api/posts -> 12ms (from cache)
  GET /api/posts -> 11ms (from cache)
```

## Cache Headers

Cached responses include `X-Cache` header:

```
X-Cache: HIT   # Response from cache
X-Cache: MISS  # Response from database
```

## Troubleshooting

### Cache Not Working?

1. Check if cache is enabled:
```python
app = App()  # Should be enabled by default
```

2. Check if endpoint is GET:
```python
@app.get('api/posts')  # Only GET is cached by default
```

3. Check TTL:
```python
app.cache_config(ttl=300)  # Make sure TTL > 0
```

### Cache Not Invalidating?

1. Check if write operation is POST/PUT/DELETE
2. Check path pattern matching
3. Manually invalidate if needed:
```python
invalidate_cache('/api/posts')
```

### Memory Usage?

Cache is in-memory with TTL. Old entries are automatically removed when:
- TTL expires
- Cache is invalidated
- Server restarts

For production with multiple servers, consider using Redis cache (coming soon).

## Summary

- ✅ Cache is **enabled by default**
- ✅ GET requests are automatically cached
- ✅ Write operations automatically invalidate cache
- ✅ Default TTL is 5 minutes
- ✅ Customize per app/group/endpoint
- ✅ 10x faster response times!

No configuration needed - just build your API and enjoy the speed! 🚀
