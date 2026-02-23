"""User DTOs"""

from typing import Optional


class UserDTO:
    """User response DTO"""

    def __init__(self, user):
        self.id = user.id
        self.username = user.username
        self.email = user.email
        self.first_name = user.first_name
        self.last_name = user.last_name
        self.is_active = user.is_active
        self.date_joined = user.date_joined.isoformat()

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "is_active": self.is_active,
            "date_joined": self.date_joined,
        }


class UserCreateDTO:
    """User creation DTO"""

    def __init__(self, data: dict):
        self.username = data.get("username")
        self.email = data.get("email")
        self.password = data.get("password")
        self.first_name = data.get("first_name", "")
        self.last_name = data.get("last_name", "")

    def validate(self):
        errors = []
        if not self.username:
            errors.append("Username is required")
        if not self.email:
            errors.append("Email is required")
        if not self.password:
            errors.append("Password is required")
        if self.password and len(self.password) < 8:
            errors.append("Password must be at least 8 characters")
        return errors


class UserUpdateDTO:
    """User update DTO"""

    def __init__(self, data: dict):
        self.first_name = data.get("first_name")
        self.last_name = data.get("last_name")
        self.email = data.get("email")
