"""Built-in CORS support for Shanks Django"""

from typing import List, Union, Optional
from .response import Response


class CORS:
    """
    Built-in CORS middleware for Shanks Django

    Usage:
        from shanks import App, CORS

        app = App()

        # Enable CORS for all routes
        CORS.enable(app)

        # Or with custom settings
        CORS.enable(app,
            origins=['http://localhost:3000', 'https://myapp.com'],
            methods=['GET', 'POST', 'PUT', 'DELETE'],
            headers=['Content-Type', 'Authorization'],
            credentials=True
        )
    """

    @staticmethod
    def enable(
        app,
        origins: Union[str, List[str]] = "*",
        methods: Union[str, List[str]] = "*",
        headers: Union[str, List[str]] = "*",
        credentials: bool = False,
        max_age: int = 86400,
    ):
        """
        Enable CORS for the app

        Args:
            app: Shanks App instance
            origins: Allowed origins ('*' or list of origins)
            methods: Allowed methods ('*' or list of methods)
            headers: Allowed headers ('*' or list of headers)
            credentials: Allow credentials (cookies, auth headers)
            max_age: Preflight cache duration in seconds

        Example:
            # Allow all origins
            CORS.enable(app)

            # Specific origins
            CORS.enable(app, origins=['http://localhost:3000'])

            # With credentials
            CORS.enable(app,
                origins=['http://localhost:3000'],
                credentials=True
            )
        """

        def cors_middleware(req):
            # Get origin from request
            origin = req.headers.get("Origin", "")

            # Check if origin is allowed
            if origins == "*":
                allowed_origin = "*"
            elif isinstance(origins, list):
                if origin in origins:
                    allowed_origin = origin
                else:
                    allowed_origin = None
            else:
                allowed_origin = origins if origin == origins else None

            # Handle preflight OPTIONS request
            if req.method == "OPTIONS":
                response = Response().status_code(204)

                if allowed_origin:
                    response.header("Access-Control-Allow-Origin", allowed_origin)

                if credentials:
                    response.header("Access-Control-Allow-Credentials", "true")

                # Methods
                if methods == "*":
                    response.header(
                        "Access-Control-Allow-Methods",
                        "GET, POST, PUT, DELETE, PATCH, OPTIONS",
                    )
                elif isinstance(methods, list):
                    response.header("Access-Control-Allow-Methods", ", ".join(methods))
                else:
                    response.header("Access-Control-Allow-Methods", methods)

                # Headers
                if headers == "*":
                    requested_headers = req.headers.get(
                        "Access-Control-Request-Headers", ""
                    )
                    if requested_headers:
                        response.header(
                            "Access-Control-Allow-Headers", requested_headers
                        )
                    else:
                        response.header(
                            "Access-Control-Allow-Headers",
                            "Content-Type, Authorization, X-Requested-With",
                        )
                elif isinstance(headers, list):
                    response.header("Access-Control-Allow-Headers", ", ".join(headers))
                else:
                    response.header("Access-Control-Allow-Headers", headers)

                response.header("Access-Control-Max-Age", str(max_age))

                return response.to_django_response(req.django)

            # For actual requests, we'll add headers in the response wrapper
            # Store CORS config in request for later use
            req._cors_config = {
                "allowed_origin": allowed_origin,
                "credentials": credentials,
            }

        # Add CORS middleware
        app.use(cors_middleware)

        # Wrap the _create_view to add CORS headers to responses
        original_create_view = app._create_view

        def create_view_with_cors(handler, method):
            view = original_create_view(handler, method)

            def wrapped_view(request, *args, **kwargs):
                response = view(request, *args, **kwargs)

                # Add CORS headers to response
                if hasattr(request, "_shanks_request"):
                    shanks_req = request._shanks_request
                    if hasattr(shanks_req, "_cors_config"):
                        cors_config = shanks_req._cors_config
                        if cors_config["allowed_origin"]:
                            response["Access-Control-Allow-Origin"] = cors_config[
                                "allowed_origin"
                            ]
                        if cors_config["credentials"]:
                            response["Access-Control-Allow-Credentials"] = "true"

                return response

            return wrapped_view

        app._create_view = create_view_with_cors

    @staticmethod
    def middleware(
        origins: Union[str, List[str]] = "*",
        methods: Union[str, List[str]] = "*",
        headers: Union[str, List[str]] = "*",
        credentials: bool = False,
        max_age: int = 86400,
    ):
        """
        Create a CORS middleware function

        Example:
            from shanks import App, CORS

            app = App()

            # Add CORS middleware
            app.use(CORS.middleware(
                origins=['http://localhost:3000'],
                credentials=True
            ))
        """

        def cors_middleware(req):
            origin = req.headers.get("Origin", "")

            # Check if origin is allowed
            if origins == "*":
                allowed_origin = "*"
            elif isinstance(origins, list):
                allowed_origin = origin if origin in origins else None
            else:
                allowed_origin = origins if origin == origins else None

            # Handle preflight
            if req.method == "OPTIONS":
                response = Response().status_code(204)

                if allowed_origin:
                    response.header("Access-Control-Allow-Origin", allowed_origin)

                if credentials:
                    response.header("Access-Control-Allow-Credentials", "true")

                if methods == "*":
                    response.header(
                        "Access-Control-Allow-Methods",
                        "GET, POST, PUT, DELETE, PATCH, OPTIONS",
                    )
                elif isinstance(methods, list):
                    response.header("Access-Control-Allow-Methods", ", ".join(methods))

                if headers == "*":
                    requested_headers = req.headers.get(
                        "Access-Control-Request-Headers", ""
                    )
                    response.header(
                        "Access-Control-Allow-Headers",
                        requested_headers
                        or "Content-Type, Authorization, X-Requested-With",
                    )
                elif isinstance(headers, list):
                    response.header("Access-Control-Allow-Headers", ", ".join(headers))

                response.header("Access-Control-Max-Age", str(max_age))
                return response

            # Store for actual requests
            req._cors_origin = allowed_origin
            req._cors_credentials = credentials

        return cors_middleware


def enable_cors(
    app,
    origins: Union[str, List[str]] = "*",
    methods: Union[str, List[str]] = "*",
    headers: Union[str, List[str]] = "*",
    credentials: bool = False,
    max_age: int = 86400,
):
    """
    Shortcut function to enable CORS

    Example:
        from shanks import App, enable_cors

        app = App()
        enable_cors(app)
    """
    CORS.enable(app, origins, methods, headers, credentials, max_age)
