"""Logger middleware"""

import time


def logger_middleware(req):
    """Log requests"""
    start_time = time.time()
    print(f"[{req.method}] {req.path}")

    # Store start time for response logging
    req._start_time = start_time
