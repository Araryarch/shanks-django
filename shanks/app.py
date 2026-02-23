from django.urls import path
from django.http import JsonResponse
from functools import wraps
from typing import Callable, List
from .request import Request
from .response import Response


class App:
    def __init__(self):
        self.routes = []
        self.middlewares = []

    def use(self, middleware: Callable):
        """Add middleware to the app"""
        self.middlewares.append(middleware)
        return self

    def _create_view(self, handler: Callable, method: str):
        """Create Django view from handler"""

        @wraps(handler)
        def view(request, *args, **kwargs):
            # Wrap Django request
            app_request = Request(request)
            
            # Store reference for CORS
            request._shanks_request = app_request

            # Run middlewares
            for middleware in self.middlewares:
                result = middleware(app_request)
                if result:
                    return result

            # Call handler
            response = handler(app_request, *args, **kwargs)

            # Handle response
            if isinstance(response, Response):
                return response.to_django_response(request)
            elif isinstance(response, dict):
                return JsonResponse(response)
            return response

        return view

    def get(self, route: str):
        """Decorator for GET routes"""

        def decorator(handler):
            self.routes.append(
                {
                    "path": route,
                    "view": self._create_view(handler, "GET"),
                    "name": handler.__name__,
                }
            )
            return handler

        return decorator

    def post(self, route: str):
        """Decorator for POST routes"""

        def decorator(handler):
            self.routes.append(
                {
                    "path": route,
                    "view": self._create_view(handler, "POST"),
                    "name": handler.__name__,
                }
            )
            return handler

        return decorator

    def put(self, route: str):
        """Decorator for PUT routes"""

        def decorator(handler):
            self.routes.append(
                {
                    "path": route,
                    "view": self._create_view(handler, "PUT"),
                    "name": handler.__name__,
                }
            )
            return handler

        return decorator

    def delete(self, route: str):
        """Decorator for DELETE routes"""

        def decorator(handler):
            self.routes.append(
                {
                    "path": route,
                    "view": self._create_view(handler, "DELETE"),
                    "name": handler.__name__,
                }
            )
            return handler

        return decorator

    def get_urls(self):
        """Get Django URL patterns"""
        return [
            path(route["path"].lstrip("/"), route["view"], name=route["name"])
            for route in self.routes
        ]
