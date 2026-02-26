from functools import wraps
from typing import Callable, List
import re
import sys

from django.http import JsonResponse
from django.urls import path, re_path

from .request import Request
from .response import Response


class App:
    def __init__(self, prefix: str = "", enable_cache: bool = True):
        self.routes = []
        self.middlewares = []
        self.prefix = prefix.rstrip("/")
        self._cache_enabled = enable_cache

        # Auto-enable cache and smart invalidation by default
        if enable_cache:
            from .cache import auto_cache, smart_cache_invalidation

            self.middlewares.append(auto_cache)
            self.middlewares.append(smart_cache_invalidation)

        # Auto-register this app instance for urlpatterns export
        self._auto_register()

    def _auto_register(self):
        """Auto-register app instance to caller's module for urlpatterns export"""
        # Get the caller's frame (skip __init__ and this method)
        frame = sys._getframe(2)
        caller_globals = frame.f_globals

        # Only register if not already registered and not in shanks module itself
        if (
            "__shanks_app__" not in caller_globals
            and caller_globals.get("__name__") != "shanks.app"
        ):
            caller_globals["__shanks_app__"] = self

            # Auto-inject urlpatterns getter
            def __getattr__(name):
                if name == "urlpatterns":
                    app = caller_globals.get("__shanks_app__")
                    if app:
                        return app.get_urls()
                raise AttributeError(f"module has no attribute '{name}'")

            # Set __getattr__ on the module
            import types

            module_name = caller_globals.get("__name__")
            if module_name and module_name in sys.modules:
                module = sys.modules[module_name]
                if not hasattr(module, "__getattr__"):
                    module.__getattr__ = __getattr__

    def _convert_route_to_django(self, route: str):
        """
        Convert Express-like route to Django URL pattern with auto-type detection
        Examples:
            'api/posts/<post_id>' -> 'api/posts/(?P<post_id>[0-9]+)'
            'api/users/<username>' -> 'api/users/(?P<username>[^/]+)'
            'api/posts/<int:post_id>' -> 'api/posts/(?P<post_id>[0-9]+)' (explicit)
        """
        # Pattern to match <param> or <type:param>
        pattern = r"<(?:(\w+):)?(\w+)>"

        def replace_param(match):
            type_hint = match.group(1)  # int, str, slug, etc.
            param_name = match.group(2)

            # If type is explicitly specified, use it
            if type_hint:
                if type_hint == "int":
                    return f"(?P<{param_name}>[0-9]+)"
                elif type_hint == "slug":
                    return f"(?P<{param_name}>[-a-zA-Z0-9_]+)"
                elif type_hint == "uuid":
                    return f"(?P<{param_name}>[0-9a-f]{{8}}-[0-9a-f]{{4}}-[0-9a-f]{{4}}-[0-9a-f]{{4}}-[0-9a-f]{{12}})"
                elif type_hint == "path":
                    return f"(?P<{param_name}>.+)"
                else:  # str or any other
                    return f"(?P<{param_name}>[^/]+)"

            # Auto-detect: if param name suggests it's an ID, treat as int
            if param_name.endswith("_id") or param_name == "id":
                return f"(?P<{param_name}>[0-9]+)"

            # Otherwise, treat as string
            return f"(?P<{param_name}>[^/]+)"

        # Replace all parameters
        django_pattern = re.sub(pattern, replace_param, route)
        return django_pattern

    def use(self, middleware: Callable):
        """Add middleware to the app"""
        # Check if it's a swagger middleware
        if hasattr(middleware, "_is_swagger") and middleware._is_swagger:
            # Enable Swagger with the config
            from .swagger import SwaggerUI

            config = middleware._swagger_config
            SwaggerUI.enable(
                self,
                title=config["title"],
                version=config["version"],
                description=config["description"],
                docs_url=config["docs_url"],
            )
        else:
            self.middlewares.append(middleware)
        return self

    def disable_cache(self):
        """
        Disable auto-caching for this app/group

        Example:
            app = App()
            app.disable_cache()  # No auto-cache

            # Or for specific group
            no_cache_routes = app.group('api/realtime')
            no_cache_routes.disable_cache()
        """
        from .cache import auto_cache, smart_cache_invalidation

        # Remove cache middlewares
        self.middlewares = [
            m
            for m in self.middlewares
            if m not in [auto_cache, smart_cache_invalidation]
        ]
        self._cache_enabled = False
        return self

    def cache_config(self, ttl: int = 300, methods: list = None):
        """
        Configure cache settings for this app/group

        Args:
            ttl: Time to live in seconds (default 300 = 5 minutes)
            methods: HTTP methods to cache (default ['GET'])

        Example:
            app = App()
            app.cache_config(ttl=600)  # Cache for 10 minutes

            # For specific group
            api = app.group('api/v1')
            api.cache_config(ttl=60)  # Cache for 1 minute
        """
        if methods is None:
            methods = ["GET"]

        # Remove existing cache middleware
        from .cache import auto_cache, smart_cache_invalidation

        self.middlewares = [
            m
            for m in self.middlewares
            if m not in [auto_cache, smart_cache_invalidation]
        ]

        # Add custom cache middleware
        def custom_cache(req, res, next):
            if req.method not in methods:
                next()
                return

            from .cache import cache_key, get_cache

            cache = get_cache()

            key = cache_key(req.django)
            cached = cache.get(key)
            if cached is not None:
                return cached

            result = next()
            if result is not None:
                cache.set(key, result, ttl)
            return result

        self.middlewares.append(custom_cache)
        self.middlewares.append(smart_cache_invalidation)
        return self

    def _create_view(self, handler: Callable, method: str):
        """Create Django view from handler"""

        @wraps(handler)
        def view(request, *args, **kwargs):
            # Wrap Django request
            app_request = Request(request)
            app_response = Response()

            # Store reference for CORS
            request._shanks_request = app_request

            # Middleware chain
            middleware_index = [0]
            handler_called = [False]

            def next_middleware():
                """Call next middleware in chain"""
                if middleware_index[0] < len(self.middlewares):
                    current = self.middlewares[middleware_index[0]]
                    middleware_index[0] += 1

                    # Call middleware with (req, res, next)
                    import inspect

                    sig = inspect.signature(current)
                    param_count = len(sig.parameters)

                    if param_count == 3:
                        # Express.js style: (req, res, next)
                        result = current(app_request, app_response, next_middleware)
                    elif param_count == 1:
                        # Legacy style: (req)
                        result = current(app_request)
                        if not result:
                            next_middleware()
                    else:
                        # Default: call with req
                        result = current(app_request)
                        if not result:
                            next_middleware()

                    return result
                else:
                    # All middlewares done, call handler
                    if not handler_called[0]:
                        handler_called[0] = True
                        return handler(app_request, *args, **kwargs)

            # Start middleware chain
            result = next_middleware()

            # If middleware returned a response, use it
            if result:
                if isinstance(result, Response):
                    return result.to_django_response(request)
                elif isinstance(result, dict):
                    return JsonResponse(result)
                return result

            # Otherwise use handler response
            if handler_called[0]:
                response = handler(app_request, *args, **kwargs)
                if isinstance(response, Response):
                    return response.to_django_response(request)
                elif isinstance(response, dict):
                    return JsonResponse(response)
                return response

            # Fallback
            return JsonResponse({"error": "No response"}, status=500)

        # Store HTTP method on view for later grouping
        view._http_method = method
        return view

    def get(self, route: str):
        """Decorator for GET routes"""

        def decorator(handler):
            full_path = f"{self.prefix}/{route}".strip("/")
            self.routes.append(
                {
                    "path": full_path,
                    "view": self._create_view(handler, "GET"),
                    "name": handler.__name__,
                }
            )
            return handler

        return decorator

    def post(self, route: str):
        """Decorator for POST routes"""

        def decorator(handler):
            full_path = f"{self.prefix}/{route}".strip("/")
            self.routes.append(
                {
                    "path": full_path,
                    "view": self._create_view(handler, "POST"),
                    "name": handler.__name__,
                }
            )
            return handler

        return decorator

    def put(self, route: str):
        """Decorator for PUT routes"""

        def decorator(handler):
            full_path = f"{self.prefix}/{route}".strip("/")
            self.routes.append(
                {
                    "path": full_path,
                    "view": self._create_view(handler, "PUT"),
                    "name": handler.__name__,
                }
            )
            return handler

        return decorator

    def delete(self, route: str):
        """Decorator for DELETE routes"""

        def decorator(handler):
            full_path = f"{self.prefix}/{route}".strip("/")
            self.routes.append(
                {
                    "path": full_path,
                    "view": self._create_view(handler, "DELETE"),
                    "name": handler.__name__,
                }
            )
            return handler

        return decorator

    def patch(self, route: str):
        """Decorator for PATCH routes"""

        def decorator(handler):
            full_path = f"{self.prefix}/{route}".strip("/")
            self.routes.append(
                {
                    "path": full_path,
                    "view": self._create_view(handler, "PATCH"),
                    "name": handler.__name__,
                }
            )
            return handler

        return decorator

    def group(self, prefix: str, *middlewares):
        """
        Create a route group with prefix (like Gin)

        Args:
            prefix: URL prefix for the group
            *middlewares: Optional middlewares to apply to all routes in this group

        Returns:
            New App instance with the prefix and middlewares

        Example:
            auth_routes = app.group('api/v1/auth')
            auth_routes.post('login', login_handler)
            auth_routes.post('register', register_handler)

            # With middleware
            protected = app.group('api/v1/admin', auth_middleware)
            protected.get('users', get_users)
        """
        # Inherit cache setting from parent
        group_app = App(prefix=f"{self.prefix}/{prefix}".strip("/"), enable_cache=False)

        # Copy parent middlewares (including cache if enabled)
        for middleware in self.middlewares:
            group_app.middlewares.append(middleware)

        # Add additional middlewares to the group
        for middleware in middlewares:
            group_app.use(middleware)

        return group_app

    def include(self, *apps):
        """Include routes from other App instances"""
        for app in apps:
            # Copy routes from other app
            for route in app.routes:
                self.routes.append(route)
            # Copy middlewares
            for middleware in app.middlewares:
                if middleware not in self.middlewares:
                    self.middlewares.append(middleware)
        return self

    def get_urls(self):
        """Get Django URL patterns"""
        from django.http import HttpResponse
        from django.shortcuts import render
        from django.template.loader import get_template
        from django.template import TemplateDoesNotExist
        from collections import defaultdict

        # Check if user has defined root path
        has_root = any(
            route["path"] == "" or route["path"] == "/" for route in self.routes
        )

        # Group routes by path to handle multiple HTTP methods
        routes_by_path = defaultdict(dict)
        for route in self.routes:
            route_path = route["path"].lstrip("/")
            # Extract method from view (stored during route creation)
            method = getattr(route["view"], "_http_method", "GET")
            routes_by_path[route_path][method] = route

        patterns = []
        for route_path, methods_dict in routes_by_path.items():
            # Create a combined view that handles all methods for this path
            def create_combined_view(methods_map):
                def combined_view(request, *args, **kwargs):
                    method = request.method
                    if method in methods_map:
                        return methods_map[method]["view"](request, *args, **kwargs)
                    else:
                        return JsonResponse(
                            {"error": f"Method {method} not allowed"}, status=405
                        )

                return combined_view

            view = create_combined_view(methods_dict)
            # Use name from first method
            name = list(methods_dict.values())[0]["name"]

            # Check if route has parameters
            if "<" in route_path:
                # Convert to regex pattern with auto-type detection
                django_pattern = self._convert_route_to_django(route_path)
                patterns.append(re_path(f"^{django_pattern}$", view, name=name))
            else:
                # Simple path without parameters
                patterns.append(path(route_path, view, name=name))

        # Add default landing page if no root path defined
        if not has_root:

            def default_landing(request):
                # Try to render user's index.html first
                try:
                    get_template("index.html")
                    return render(request, "index.html")
                except TemplateDoesNotExist:
                    # Render Shanks default landing page
                    import os
                    from pathlib import Path

                    landing_path = Path(__file__).parent / "templates" / "landing.html"
                    with open(landing_path, "r") as f:
                        html = f.read()
                    return HttpResponse(html)

            patterns.insert(0, path("", default_landing, name="shanks_landing"))

        return patterns


def auto_discover_routes(routes_module="routes"):
    """
    Auto-discover and combine all routers from a routes module/package

    Args:
        routes_module: Module name (default: 'routes')

    Returns:
        Combined urlpatterns from all routers

    Example:
        # In your main urls.py:
        from shanks.app import auto_discover_routes

        urlpatterns = [
            path('admin/', admin.site.urls),
        ] + auto_discover_routes('routes')
    """
    import importlib
    import pkgutil
    from pathlib import Path

    combined_patterns = []

    try:
        # Import the routes module
        routes_pkg = importlib.import_module(routes_module)
        routes_path = Path(routes_pkg.__file__).parent

        # Iterate through all Python files in the routes directory
        for importer, module_name, is_pkg in pkgutil.iter_modules([str(routes_path)]):
            if module_name.startswith("_"):
                continue

            full_module_name = f"{routes_module}.{module_name}"
            try:
                module = importlib.import_module(full_module_name)

                # Look for 'router' attribute
                if hasattr(module, "router"):
                    router = getattr(module, "router")
                    if isinstance(router, App):
                        combined_patterns.extend(router.get_urls())
                        print(f"✓ Loaded routes from {full_module_name}")

            except Exception as e:
                print(f"✗ Error loading {full_module_name}: {e}")

    except ImportError as e:
        print(f"✗ Could not import {routes_module}: {e}")

    return combined_patterns


def include_routers(*routers):
    """
    Combine multiple Shanks routers into Django urlpatterns

    Args:
        *routers: Variable number of App instances

    Returns:
        Combined urlpatterns

    Example:
        # In your main urls.py:
        from shanks.app import include_routers
        from routes.task import router as task_router
        from routes.user import router as user_router

        urlpatterns = [
            path('admin/', admin.site.urls),
        ] + include_routers(task_router, user_router)
    """
    combined_patterns = []

    for router in routers:
        if isinstance(router, App):
            combined_patterns.extend(router.get_urls())
        else:
            print(f"Warning: {router} is not a Shanks App instance")

    return combined_patterns
