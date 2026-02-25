"""Basic tests for Shanks Django"""

import json

from django.test import RequestFactory

from shanks import App, Request, Response


def test_shanks_import():
    """Test that Shanks can be imported"""
    assert App is not None


def test_simple_route():
    """Test simple GET route"""
    app = App()

    @app.get("api/test")
    def test_view(req):
        return {"status": "ok"}

    assert len(app.routes) == 1
    assert app.routes[0]["path"] == "api/test"


def test_request_wrapper():
    """Test Request wrapper"""
    factory = RequestFactory()
    django_req = factory.get("/test?name=john")

    req = Request(django_req)
    assert req.method == "GET"
    assert req.path == "/test"
    # query returns a dict from QueryDict
    query_dict = req.query
    assert query_dict["name"] == "john"


def test_response_builder():
    """Test Response builder"""
    resp = Response().status_code(201).json({"created": True})

    assert resp.status == 201
    assert resp.data == {"created": True}


def test_middleware():
    """Test middleware support"""
    # Disable cache for testing
    app = App(enable_cache=False)

    called = []

    def middleware(req):
        called.append(True)

    app.use(middleware)

    @app.get("test")
    def view(req):
        return {"ok": True}

    assert len(app.middlewares) == 1


def test_auto_cache_enabled():
    """Test that cache is enabled by default"""
    app = App()

    # Should have 2 middlewares: auto_cache and smart_cache_invalidation
    assert len(app.middlewares) == 2

    # Can disable cache
    app2 = App(enable_cache=False)
    assert len(app2.middlewares) == 0


def test_cache_config():
    """Test cache configuration"""
    app = App()

    # Configure cache
    app.cache_config(ttl=600)

    # Should still have cache middlewares
    assert len(app.middlewares) > 0

    # Disable cache
    app.disable_cache()
    assert app._cache_enabled is False

