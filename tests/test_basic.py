"""Basic tests for Shanks Django"""
import json
from django.test import RequestFactory
from shanks import Ace, Request, Response


def test_shanks_import():
    """Test that Shanks can be imported"""
    assert Ace is not None


def test_simple_route():
    """Test simple GET route"""
    app = Ace()
    
    @app.get('api/test')
    def test_view(req):
        return {'status': 'ok'}
    
    assert len(app.routes) == 1
    assert app.routes[0]['path'] == 'api/test'


def test_request_wrapper():
    """Test Request wrapper"""
    factory = RequestFactory()
    django_req = factory.get('/test?name=john')
    
    req = Request(django_req)
    assert req.method == 'GET'
    assert req.path == '/test'
    assert req.query.get('name') == 'john'


def test_response_builder():
    """Test Response builder"""
    resp = Response().status_code(201).json({'created': True})
    
    assert resp.status == 201
    assert resp.data == {'created': True}


def test_middleware():
    """Test middleware support"""
    app = Ace()
    
    called = []
    
    def middleware(req):
        called.append(True)
    
    app.use(middleware)
    
    @app.get('test')
    def view(req):
        return {'ok': True}
    
    assert len(app.middlewares) == 1
