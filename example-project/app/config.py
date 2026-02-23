"""Application configuration"""

import os
from pathlib import Path

# Build paths
BASE_DIR = Path(__file__).resolve().parent.parent

# Security
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
DEBUG = os.getenv("DEBUG", "True") == "True"
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "*").split(",")

# JWT Configuration
JWT_SECRET = os.getenv("JWT_SECRET", SECRET_KEY)
JWT_ALGORITHM = "HS256"
JWT_EXPIRATION_HOURS = 24

# CORS Configuration
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:5173",
    "http://127.0.0.1:3000",
]

# API Configuration
API_VERSION = "v1"
API_TITLE = "Blog API"
API_DESCRIPTION = "Complete blog API with authentication"

# Pagination
DEFAULT_PAGE_SIZE = 10
MAX_PAGE_SIZE = 100
