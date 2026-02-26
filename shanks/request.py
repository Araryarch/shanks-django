import json


class Request:
    """Express-like request wrapper for Django"""

    def __init__(self, django_request):
        self._request = django_request
        self.method = django_request.method
        self.path = django_request.path
        self.headers = django_request.headers
        # Expose Django request for full access
        self.django = django_request

    @property
    def body(self):
        """Get parsed request body"""
        if self._request.content_type == "application/json":
            try:
                return json.loads(self._request.body)
            except (json.JSONDecodeError, ValueError, UnicodeDecodeError) as e:
                # Return empty dict for invalid JSON, but could also raise error
                # depending on desired behavior
                return {}
        return self._request.POST.dict()

    @property
    def query(self):
        """Get query parameters"""
        return self._request.GET.dict()

    @property
    def params(self):
        """Get URL parameters (set by router)"""
        return getattr(self, "_params", {})

    def get(self, key, default=None):
        """Get value from query, body, or params"""
        return (
            self.query.get(key) or self.body.get(key) or self.params.get(key, default)
        )

    @property
    def user(self):
        """Get authenticated user"""
        return self._request.user

    @user.setter
    def user(self, value):
        """Set authenticated user"""
        self._request.user = value

    @property
    def session(self):
        """Get session"""
        return self._request.session

    @property
    def cookies(self):
        """Get cookies"""
        return self._request.COOKIES

    @property
    def files(self):
        """Get uploaded files"""
        return self._request.FILES

    @property
    def META(self):
        """Get request META"""
        return self._request.META
