"""Middleware"""


def logger(req, res, next):
    """Log all requests"""
    print(f"[{req.method}] {req.path}")
    return next()
