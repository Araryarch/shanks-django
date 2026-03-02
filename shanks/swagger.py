"""Built-in Swagger/OpenAPI support for Shanks Django"""

import json
from typing import Any, Dict, List, Optional


class SwaggerUI:
    """
    Built-in Swagger UI for Shanks Django

    Usage:
        from shanks import App, SwaggerUI

        app = App()

        # Enable Swagger UI
        SwaggerUI.enable(app,
            title="My API",
            version="1.0.0",
            description="API documentation"
        )

        # Add documented routes
        @app.get('api/users')
        @SwaggerUI.doc(
            summary="Get all users",
            description="Returns a list of all users",
            responses={200: {"description": "Success"}}
        )
        def get_users(req):
            return {'users': []}
    """

    _spec = None
    _routes = []

    @classmethod
    def enable(
        cls,
        app,
        title: str = "API Documentation",
        version: str = "1.0.0",
        description: str = "",
        docs_url: str = "docs",
        openapi_url: str = "openapi.json",
    ):
        """
        Enable Swagger UI for the app

        Args:
            app: Shanks App instance
            title: API title
            version: API version
            description: API description
            docs_url: URL path for Swagger UI (default: /docs)
            openapi_url: URL path for OpenAPI spec (default: /openapi.json)
        """
        cls._spec = {
            "openapi": "3.0.0",
            "info": {"title": title, "version": version, "description": description},
            "paths": {},
            "components": {"schemas": {}},
        }

        # Add OpenAPI JSON endpoint
        @app.get(openapi_url)
        def openapi_spec(req):
            return cls._generate_spec(app)

        # Add Swagger UI endpoint
        @app.get(docs_url)
        def swagger_ui(req):
            from django.http import HttpResponse

            html = cls._generate_swagger_html(f"/{openapi_url}")
            return HttpResponse(html, content_type="text/html")

    @classmethod
    def doc(
        cls,
        summary: str = "",
        description: str = "",
        tags: Optional[List[str]] = None,
        responses: Optional[Dict[int, Dict[str, Any]]] = None,
        parameters: Optional[List[Dict[str, Any]]] = None,
        request_body: Optional[Dict[str, Any]] = None,
    ):
        """
        Decorator to add documentation to a route

        Example:
            @app.get('api/users/<int:user_id>')
            @SwaggerUI.doc(
                summary="Get user by ID",
                description="Returns a single user",
                parameters=[{
                    "name": "user_id",
                    "in": "path",
                    "required": True,
                    "schema": {"type": "integer"}
                }],
                responses={
                    200: {"description": "Success"},
                    404: {"description": "User not found"}
                }
            )
            def get_user(req, user_id):
                return {'id': user_id}
        """

        def decorator(func):
            func._swagger_doc = {
                "summary": summary,
                "description": description,
                "tags": tags or [],
                "responses": responses or {},
                "parameters": parameters or [],
                "requestBody": request_body,
            }
            return func

        return decorator

    @classmethod
    def _generate_spec(cls, app) -> Dict[str, Any]:
        """Generate OpenAPI specification from routes"""
        spec = cls._spec.copy()

        for route in app.routes:
            path = "/" + route["path"]
            # Convert Django URL patterns to OpenAPI format
            path = path.replace("<int:", "{").replace("<str:", "{").replace(">", "}")

            if path not in spec["paths"]:
                spec["paths"][path] = {}

            # Get method from route
            method = "get"  # Default
            if hasattr(route["view"], "__name__"):
                view_name = route["view"].__name__.lower()
                if "post" in view_name:
                    method = "post"
                elif "put" in view_name:
                    method = "put"
                elif "delete" in view_name:
                    method = "delete"

            # Get documentation from decorator
            doc = {}
            if hasattr(route["view"], "_swagger_doc"):
                doc = route["view"]._swagger_doc

            spec["paths"][path][method] = {
                "summary": doc.get("summary", route["name"]),
                "description": doc.get("description", ""),
                "tags": doc.get("tags", []),
                "parameters": doc.get("parameters", []),
                "responses": doc.get("responses", {"200": {"description": "Success"}}),
            }

            if doc.get("requestBody"):
                spec["paths"][path][method]["requestBody"] = doc["requestBody"]

        return spec

    @classmethod
    def _generate_swagger_html(cls, openapi_url: str) -> str:
        """Generate Swagger UI HTML with Shanks color scheme"""
        return f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>API Documentation - Shanks Django</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui.css">
    <style>
        /* Shanks Color Scheme: Red (#ef4444), Black (#000000), White (#ffffff) */
        body {{
            margin: 0;
            padding: 0;
            background-color: #000000;
        }}
        
        .topbar {{
            display: none;
        }}
        
        /* Main container */
        .swagger-ui {{
            background-color: #000000;
        }}
        
        /* Info section */
        .swagger-ui .info {{
            background-color: #000000;
            border: 1px solid #ef4444;
            border-radius: 0;
        }}
        
        .swagger-ui .info .title {{
            color: #ef4444;
        }}
        
        .swagger-ui .info p,
        .swagger-ui .info li,
        .swagger-ui .info a {{
            color: #ffffff;
        }}
        
        /* Scheme container */
        .swagger-ui .scheme-container {{
            background-color: #1a1a1a;
            border: 1px solid #ef4444;
            border-radius: 0;
        }}
        
        /* Operations */
        .swagger-ui .opblock {{
            background-color: #1a1a1a;
            border: 1px solid #ef4444;
            border-radius: 0;
            margin-bottom: 10px;
        }}
        
        .swagger-ui .opblock .opblock-summary {{
            border-radius: 0;
        }}
        
        .swagger-ui .opblock.opblock-get {{
            background-color: #1a1a1a;
            border-color: #ef4444;
        }}
        
        .swagger-ui .opblock.opblock-get .opblock-summary-method {{
            background-color: #ef4444;
            color: #ffffff;
            border-radius: 0;
        }}
        
        .swagger-ui .opblock.opblock-post {{
            background-color: #1a1a1a;
            border-color: #ef4444;
        }}
        
        .swagger-ui .opblock.opblock-post .opblock-summary-method {{
            background-color: #dc2626;
            color: #ffffff;
            border-radius: 0;
        }}
        
        .swagger-ui .opblock.opblock-put {{
            background-color: #1a1a1a;
            border-color: #ef4444;
        }}
        
        .swagger-ui .opblock.opblock-put .opblock-summary-method {{
            background-color: #b91c1c;
            color: #ffffff;
            border-radius: 0;
        }}
        
        .swagger-ui .opblock.opblock-delete {{
            background-color: #1a1a1a;
            border-color: #ef4444;
        }}
        
        .swagger-ui .opblock.opblock-delete .opblock-summary-method {{
            background-color: #991b1b;
            color: #ffffff;
            border-radius: 0;
        }}
        
        .swagger-ui .opblock .opblock-summary-path,
        .swagger-ui .opblock .opblock-summary-description {{
            color: #ffffff;
        }}
        
        /* Buttons */
        .swagger-ui .btn {{
            background-color: #ef4444;
            color: #ffffff;
            border: none;
            border-radius: 0;
        }}
        
        .swagger-ui .btn:hover {{
            background-color: #dc2626;
        }}
        
        .swagger-ui .btn.cancel {{
            background-color: #1a1a1a;
            border: 1px solid #ef4444;
            color: #ffffff;
        }}
        
        .swagger-ui .btn.execute {{
            background-color: #ef4444;
            border: none;
        }}
        
        /* Tables */
        .swagger-ui table {{
            background-color: #1a1a1a;
            border: 1px solid #ef4444;
            border-radius: 0;
        }}
        
        .swagger-ui table thead tr th,
        .swagger-ui table thead tr td {{
            background-color: #000000;
            color: #ef4444;
            border-bottom: 1px solid #ef4444;
        }}
        
        .swagger-ui table tbody tr td {{
            color: #ffffff;
            border-bottom: 1px solid #333333;
        }}
        
        /* Parameters */
        .swagger-ui .parameters-col_description {{
            color: #ffffff;
        }}
        
        .swagger-ui .parameter__name {{
            color: #ef4444;
        }}
        
        .swagger-ui .parameter__type {{
            color: #ffffff;
        }}
        
        /* Responses */
        .swagger-ui .responses-inner {{
            background-color: #1a1a1a;
            border: 1px solid #ef4444;
            border-radius: 0;
        }}
        
        .swagger-ui .response-col_status {{
            color: #ef4444;
        }}
        
        .swagger-ui .response-col_description {{
            color: #ffffff;
        }}
        
        /* Models */
        .swagger-ui .model-box {{
            background-color: #1a1a1a;
            border: 1px solid #ef4444;
            border-radius: 0;
        }}
        
        .swagger-ui .model {{
            color: #ffffff;
        }}
        
        .swagger-ui .model-title {{
            color: #ef4444;
        }}
        
        /* Input fields */
        .swagger-ui input[type=text],
        .swagger-ui input[type=password],
        .swagger-ui input[type=email],
        .swagger-ui textarea,
        .swagger-ui select {{
            background-color: #1a1a1a;
            color: #ffffff;
            border: 1px solid #ef4444;
            border-radius: 0;
        }}
        
        .swagger-ui input[type=text]:focus,
        .swagger-ui input[type=password]:focus,
        .swagger-ui input[type=email]:focus,
        .swagger-ui textarea:focus,
        .swagger-ui select:focus {{
            border-color: #ef4444;
            outline: none;
        }}
        
        /* Code blocks */
        .swagger-ui .highlight-code {{
            background-color: #1a1a1a;
            border: 1px solid #ef4444;
            border-radius: 0;
        }}
        
        .swagger-ui .highlight-code pre {{
            background-color: #1a1a1a;
            color: #ffffff;
        }}
        
        /* Scrollbar */
        ::-webkit-scrollbar {{
            width: 10px;
            height: 10px;
        }}
        
        ::-webkit-scrollbar-track {{
            background: #1a1a1a;
        }}
        
        ::-webkit-scrollbar-thumb {{
            background: #333333;
            border-radius: 0;
        }}
        
        ::-webkit-scrollbar-thumb:hover {{
            background: #555555;
        }}
        
        /* Authorization */
        .swagger-ui .auth-wrapper {{
            background-color: #1a1a1a;
            border: 1px solid #ef4444;
            border-radius: 0;
        }}
        
        .swagger-ui .auth-container {{
            background-color: #000000;
        }}
        
        /* Links */
        .swagger-ui a {{
            color: #ef4444;
        }}
        
        .swagger-ui a:hover {{
            color: #dc2626;
        }}
        
        /* Try it out */
        .swagger-ui .try-out {{
            background-color: #1a1a1a;
        }}
        
        .swagger-ui .try-out__btn {{
            background-color: #ef4444;
            color: #ffffff;
            border: none;
            border-radius: 0;
        }}
    </style>
</head>
<body>
    <div id="swagger-ui"></div>
    <script src="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui-bundle.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui-standalone-preset.js"></script>
    <script>
        window.onload = function() {{
            const ui = SwaggerUIBundle({{
                url: "{openapi_url}",
                dom_id: '#swagger-ui',
                deepLinking: true,
                presets: [
                    SwaggerUIBundle.presets.apis,
                    SwaggerUIStandalonePreset
                ],
                plugins: [
                    SwaggerUIBundle.plugins.DownloadUrl
                ],
                layout: "StandaloneLayout"
            }});
            window.ui = ui;
        }};
    </script>
</body>
</html>
"""


def enable_swagger(
    app,
    title: str = "API Documentation",
    version: str = "1.0.0",
    description: str = "",
    docs_url: str = "docs",
):
    """
    Shortcut to enable Swagger UI

    Example:
        from shanks import App, enable_swagger

        app = App()
        enable_swagger(app, title="My API")
    """
    SwaggerUI.enable(app, title, version, description, docs_url)


def swagger(
    title: str = "API Documentation",
    version: str = "1.0.0",
    description: str = "",
    docs_url: str = "docs",
):
    """
    Middleware-style Swagger UI setup

    Usage:
        from shanks import App, swagger

        app = App()
        app.use(swagger(title="My API", version="1.0.0"))

        @app.get('api/users')
        def get_users(req):
            return {'users': []}
    """

    def middleware(req, res, next):
        # This is called once during app initialization
        # The actual Swagger setup happens when the middleware is added
        next()

    # Store swagger config on the middleware function
    middleware._swagger_config = {
        "title": title,
        "version": version,
        "description": description,
        "docs_url": docs_url,
    }
    middleware._is_swagger = True

    return middleware
