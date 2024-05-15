from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from .manger import UserManager


class AccessToken(models.Model):
    userid = models.IntegerField()
    jti = models.CharField(max_length=100)
    
class UserData(AbstractUser):

    username = None
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    
    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.name
    