from functools import wraps
from typing import Callable, List

from django.http import JsonResponse
from django.urls import path

from .request import Request
from .response import Response


class App:
    def __init__(self, prefix: str = ""):
        self.routes = []
        self.middlewares = []
        self.prefix = prefix.rstrip("/")

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

    def group(self, prefix: str):
        """Create a route group with prefix (like Gin)"""
        return App(prefix=f"{self.prefix}/{prefix}".strip("/"))

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

        # Check if user has defined root path
        has_root = any(
            route["path"] == "" or route["path"] == "/" for route in self.routes
        )

        patterns = [
            path(route["path"].lstrip("/"), route["view"], name=route["name"])
            for route in self.routes
        ]

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
