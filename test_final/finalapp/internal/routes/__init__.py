"""API Routes"""

# Import all routers
from .health_route import router as health_router
from .auth_route import router as auth_router

# Export urlpatterns for Django
urlpatterns = [*auth_router, *health_router]
