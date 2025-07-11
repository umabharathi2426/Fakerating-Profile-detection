# Create your models here.
from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models

class CustomUserManager(UserManager):
    def get_by_natural_key(self, username):
        return self.get(**{self.model.USERNAME_FIELD: username})

class User(AbstractUser):
    username = models.CharField(max_length=150, unique=True)  # Override username field
    objects = CustomUserManager()

    # Add the custom related_name to avoid conflict with the default User model
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='accounts_user_set',  # Custom related_name for groups
        blank=True
    )
    
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='accounts_user_permissions_set',  # Custom related_name for user_permissions
        blank=True
    )
    is_blocked = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    email = models.EmailField(unique=True)
