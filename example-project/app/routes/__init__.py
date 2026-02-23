"""API Routes - Simple grouping like Gin"""

from app.config import (API_DESCRIPTION, API_TITLE, API_VERSION,
                        CORS_ALLOWED_ORIGINS)
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

# Include all route groups - Simple!
app.include(
    auth.router,
    users.router,
    posts.router,
    comments.router,
    categories.router,
    tags.router,
)


# Health check
@app.get("api/health")
@SwaggerUI.doc(summary="Health check", tags=["System"])
def health(req):
    return {"status": "ok", "version": API_VERSION}


# Export URL patterns
urlpatterns = app.get_urls()
