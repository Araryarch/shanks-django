"""Template Views"""

# Import all view routers
from .home_view import router as home_router

# Export urlpatterns for Django
urlpatterns = [*home_router]
