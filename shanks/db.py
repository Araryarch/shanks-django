"""Database connection helpers for Shanks Django"""

import os
from typing import Any, Dict, Optional


class DatabaseConfig:
    """Database configuration helper"""

    @staticmethod
    def postgres(
        host: str = "localhost",
        port: int = 5432,
        database: str = "postgres",
        user: str = "postgres",
        password: str = "",
        **options,
    ) -> Dict[str, Any]:
        """
        Generate PostgreSQL database configuration

        Example:
            DATABASES = {
                'default': DatabaseConfig.postgres(
                    host='localhost',
                    database='mydb',
                    user='myuser',
                    password='mypass'
                )
            }
        """
        config = {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": database,
            "USER": user,
            "PASSWORD": password,
            "HOST": host,
            "PORT": port,
        }
        if options:
            config["OPTIONS"] = options
        return config

    @staticmethod
    def mysql(
        host: str = "localhost",
        port: int = 3306,
        database: str = "mysql",
        user: str = "root",
        password: str = "",
        **options,
    ) -> Dict[str, Any]:
        """
        Generate MySQL database configuration

        Example:
            DATABASES = {
                'default': DatabaseConfig.mysql(
                    host='localhost',
                    database='mydb',
                    user='myuser',
                    password='mypass'
                )
            }
        """
        config = {
            "ENGINE": "django.db.backends.mysql",
            "NAME": database,
            "USER": user,
            "PASSWORD": password,
            "HOST": host,
            "PORT": port,
        }
        if options:
            config["OPTIONS"] = options
        return config

    @staticmethod
    def sqlite(path: str = "db.sqlite3") -> Dict[str, Any]:
        """
        Generate SQLite database configuration

        Example:
            DATABASES = {
                'default': DatabaseConfig.sqlite('db.sqlite3')
            }
        """
        return {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": path,
        }

    @staticmethod
    def from_url(url: str) -> Dict[str, Any]:
        """
        Parse database URL and generate configuration

        Supports:
        - postgresql://user:pass@host:port/dbname
        - mysql://user:pass@host:port/dbname
        - sqlite:///path/to/db.sqlite3

        Example:
            DATABASES = {
                'default': DatabaseConfig.from_url(os.getenv('DATABASE_URL'))
            }
        """
        try:
            import dj_database_url

            return dj_database_url.parse(url)
        except ImportError:
            # Fallback manual parsing
            if url.startswith("sqlite"):
                path = url.replace("sqlite:///", "")
                return DatabaseConfig.sqlite(path)

            # Basic parsing for postgres/mysql
            if "://" in url:
                scheme, rest = url.split("://", 1)
                if "@" in rest:
                    auth, location = rest.split("@", 1)
                    user, password = auth.split(":", 1) if ":" in auth else (auth, "")
                    host_port, database = (
                        location.split("/", 1) if "/" in location else (location, "")
                    )
                    host, port = (
                        host_port.split(":", 1)
                        if ":" in host_port
                        else (host_port, None)
                    )

                    if scheme == "postgresql" or scheme == "postgres":
                        return DatabaseConfig.postgres(
                            host=host,
                            port=int(port) if port else 5432,
                            database=database,
                            user=user,
                            password=password,
                        )
                    elif scheme == "mysql":
                        return DatabaseConfig.mysql(
                            host=host,
                            port=int(port) if port else 3306,
                            database=database,
                            user=user,
                            password=password,
                        )

            raise ValueError(f"Unsupported database URL: {url}")


class MongoDB:
    """MongoDB connection helper"""

    _client = None
    _db = None

    @classmethod
    def connect(
        cls,
        host: str = "localhost",
        port: int = 27017,
        database: str = "test",
        username: Optional[str] = None,
        password: Optional[str] = None,
        **kwargs,
    ):
        """
        Connect to MongoDB

        Example:
            from shanks.db import MongoDB

            MongoDB.connect(
                host='localhost',
                database='mydb',
                username='user',
                password='pass'
            )

            # Use in views
            @app.get('api/users')
            def get_users(req):
                users = MongoDB.db.users.find()
                return {'users': list(users)}
        """
        try:
            from pymongo import MongoClient
        except ImportError:
            raise ImportError(
                "pymongo is required for MongoDB support. "
                "Install it with: pip install pymongo"
            )

        if username and password:
            uri = f"mongodb://{username}:{password}@{host}:{port}/{database}"
        else:
            uri = f"mongodb://{host}:{port}/{database}"

        cls._client = MongoClient(uri, **kwargs)
        cls._db = cls._client[database]
        return cls._db

    @classmethod
    def connect_uri(cls, uri: str, database: str):
        """
        Connect to MongoDB using URI

        Example:
            MongoDB.connect_uri(
                'mongodb://user:pass@host:27017',
                'mydb'
            )
        """
        try:
            from pymongo import MongoClient
        except ImportError:
            raise ImportError(
                "pymongo is required for MongoDB support. "
                "Install it with: pip install pymongo"
            )

        cls._client = MongoClient(uri)
        cls._db = cls._client[database]
        return cls._db

    @classmethod
    def get_client(cls):
        """Get MongoDB client"""
        if cls._client is None:
            raise RuntimeError("MongoDB not connected. Call MongoDB.connect() first.")
        return cls._client

    @classmethod
    def get_db(cls):
        """Get MongoDB database"""
        if cls._db is None:
            raise RuntimeError("MongoDB not connected. Call MongoDB.connect() first.")
        return cls._db

    # Backward compatibility properties
    @property
    def client(self):
        """Get MongoDB client (instance property for backward compatibility)"""
        return self.__class__.get_client()

    @property
    def db(self):
        """Get MongoDB database (instance property for backward compatibility)"""
        return self.__class__.get_db()


class Redis:
    """Redis connection helper"""

    _client = None

    @classmethod
    def connect(
        cls,
        host: str = "localhost",
        port: int = 6379,
        db: int = 0,
        password: Optional[str] = None,
        **kwargs,
    ):
        """
        Connect to Redis

        Example:
            from shanks.db import Redis

            Redis.connect(
                host='localhost',
                password='mypass'
            )

            # Use in views
            @app.get('api/cache')
            def get_cache(req):
                value = Redis.client.get('key')
                return {'value': value}
        """
        try:
            import redis
        except ImportError:
            raise ImportError(
                "redis is required for Redis support. "
                "Install it with: pip install redis"
            )

        cls._client = redis.Redis(
            host=host,
            port=port,
            db=db,
            password=password,
            decode_responses=True,
            **kwargs,
        )
        return cls._client

    @classmethod
    def connect_url(cls, url: str):
        """
        Connect to Redis using URL

        Example:
            Redis.connect_url('redis://localhost:6379/0')
            Redis.connect_url('redis://:password@localhost:6379/0')
        """
        try:
            import redis
        except ImportError:
            raise ImportError(
                "redis is required for Redis support. "
                "Install it with: pip install redis"
            )

        cls._client = redis.from_url(url, decode_responses=True)
        return cls._client

    @classmethod
    def get_client(cls):
        """Get Redis client"""
        if cls._client is None:
            raise RuntimeError("Redis not connected. Call Redis.connect() first.")
        return cls._client

    # Backward compatibility property
    @property
    def client(self):
        """Get Redis client (instance property for backward compatibility)"""
        return self.__class__.get_client()


# Convenience functions
def setup_postgres(**kwargs) -> Dict[str, Any]:
    """Shortcut for PostgreSQL configuration"""
    return DatabaseConfig.postgres(**kwargs)


def setup_mysql(**kwargs) -> Dict[str, Any]:
    """Shortcut for MySQL configuration"""
    return DatabaseConfig.mysql(**kwargs)


def setup_sqlite(path: str = "db.sqlite3") -> Dict[str, Any]:
    """Shortcut for SQLite configuration"""
    return DatabaseConfig.sqlite(path)


def setup_mongodb(**kwargs):
    """Shortcut for MongoDB connection"""
    return MongoDB.connect(**kwargs)


def setup_redis(**kwargs):
    """Shortcut for Redis connection"""
    return Redis.connect(**kwargs)
