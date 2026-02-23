from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.shortcuts import render as django_render


class Response:
    """Express-like response builder"""

    def __init__(self, data=None, status=200):
        self.data = data
        self.status = status
        self._headers = {}
        self._cookies = []
        self._template = None
        self._context = {}

    def json(self, data):
        """Send JSON response"""
        self.data = data
        return self

    def status_code(self, code):
        """Set status code"""
        self.status = code
        return self

    def header(self, key, value):
        """Set response header"""
        self._headers[key] = value
        return self

    def cookie(self, key, value, **options):
        """Set cookie"""
        self._cookies.append((key, value, options))
        return self

    def redirect(self, url):
        """Redirect to URL"""
        self.data = url
        self._template = "redirect"
        return self

    def render(self, request, template, context=None):
        """Render Django template"""
        self._template = template
        self._context = context or {}
        self._context["request"] = request
        return self

    def to_django_response(self, request=None):
        """Convert to Django response"""
        # Handle redirect
        if self._template == "redirect":
            response = HttpResponseRedirect(self.data)
        # Handle template rendering
        elif self._template and self._template != "redirect":
            response = django_render(request, self._template, self._context)
            response.status_code = self.status
        # Handle JSON
        elif isinstance(self.data, dict):
            response = JsonResponse(self.data, status=self.status)
        # Handle plain text/HTML
        else:
            response = HttpResponse(self.data, status=self.status)

        # Set headers
        for key, value in self._headers.items():
            response[key] = value

        # Set cookies
        for key, value, options in self._cookies:
            response.set_cookie(key, value, **options)

        return response
