"""API Routes"""

from app.config import (
    API_DESCRIPTION,
    API_TITLE,
    API_VERSION,
    CORS_ALLOWED_ORIGINS,
)
from app.middleware import logger_middleware

from shanks import CORS, App, SwaggerUI

# Import routers
from . import auth, categories, comments, posts, tags, users

# Create main app
app = App()

# Enable CORS
CORS.enable(app, origins=CORS_ALLOWED_ORIGINS, credentials=True)

# Enable Swagger
SwaggerUI.enable(app, title=API_TITLE, version=API_VERSION, description=API_DESCRIPTION)

# Add global middleware
app.use(logger_middleware)

# Combine all routes
for route in auth.router.routes:
    app.routes.append(route)

for route in users.router.routes:
    app.routes.append(route)

for route in posts.router.routes:
    app.routes.append(route)

for route in comments.router.routes:
    app.routes.append(route)

for route in categories.router.routes:
    app.routes.append(route)

for route in tags.router.routes:
    app.routes.append(route)


# Health check
@app.get("api/health")
@SwaggerUI.doc(summary="Health check", tags=["System"])
def health(req):
    return {"status": "ok", "version": API_VERSION}


# Export URL patterns
urlpatterns = app.get_urls()
