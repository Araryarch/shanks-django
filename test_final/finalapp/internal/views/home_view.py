"""Home View"""
from shanks import App, render

router = App()


@router.get("/")
def home(req):
    """Home page"""
    return render(req, "index.html", {"title": "finalapp"})
