"""Template rendering utilities for Shanks"""

from django.shortcuts import render as django_render
from django.http import HttpResponse
from django.template.loader import render_to_string


def render(request, template_name, context=None, content_type=None, status=None):
    """
    Render a template with context

    Args:
        request: Shanks Request or Django request object
        template_name: Template file name (e.g., 'index.html', 'users/list.html')
        context: Dictionary of context variables (default: {})
        content_type: Response content type (default: 'text/html')
        status: HTTP status code (default: 200)

    Returns:
        HttpResponse with rendered template

    Example:
        @router.get('/')
        def home(req):
            return render(req, 'home.html', {'title': 'Welcome'})

        @router.get('/users')
        def users(req):
            users = User.objects.all()
            return render(req, 'users/list.html', {'users': users})
    """
    if context is None:
        context = {}

    # Handle Shanks Request wrapper
    django_request = getattr(request, "django", request)

    return django_render(
        django_request,
        template_name,
        context=context,
        content_type=content_type,
        status=status,
    )


def render_string(template_name, context=None):
    """
    Render template to string without request

    Args:
        template_name: Template file name
        context: Dictionary of context variables (default: {})

    Returns:
        Rendered template as string

    Example:
        html = render_string('email/welcome.html', {'user': user})
        send_email(to=user.email, html=html)
    """
    if context is None:
        context = {}

    return render_to_string(template_name, context)


def render_html(html_string, context=None, status=200):
    """
    Render HTML string with optional context

    Args:
        html_string: Raw HTML string
        context: Dictionary for template variables (optional)
        status: HTTP status code (default: 200)

    Returns:
        HttpResponse with rendered HTML

    Example:
        @router.get('/hello')
        def hello(req):
            return render_html('<h1>Hello {{ name }}!</h1>', {'name': 'World'})
    """
    if context:
        from django.template import Context, Template

        template = Template(html_string)
        html = template.render(Context(context))
    else:
        html = html_string

    return HttpResponse(html, status=status)
