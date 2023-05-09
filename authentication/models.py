from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import (PermissionsMixin)
import jwt
from datetime import datetime, timedelta
from django.conf import settings
class User(AbstractUser, PermissionsMixin):
    
    def __str__(self):
        return self.first_name
    
    @property
    def token(self):
        token = jwt.encode({
            "username": self.username,
            "email": self.email,
            "exp": datetime.utcnow() + timedelta(hours=24)
        }, settings.SECRET_KEY, algorithm='HS256')
        return token
