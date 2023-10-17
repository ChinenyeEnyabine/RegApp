# from django.db import models
# from django.contrib.auth.models import AbstractUser


# from django.contrib.auth.models import AbstractUser
# from django.db import models

# class Skisubuser(AbstractUser):
#     phone = models.CharField(max_length=14)
#     created_date = models.DateField(auto_now_add=True)
#     updated_date = models.DateField(auto_now=True)
    
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class Skisubuser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    phone = models.CharField(max_length=14)
    first_name=models.CharField(max_length=100)
    last_name=models.CharField(max_length=100)
    phone = models.CharField(max_length=14)
    created_date = models.DateField(auto_now_add=True)
    updated_date = models.DateField(auto_now=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    # Optionally, set email as the primary key for uniqueness.
    EMAIL_FIELD = 'email'

    def __str__(self):
        return self.email


    # status=models.CharField(max_length=20,default='Pending')
    # is_active=models.BooleanField(default=False)
    # is_staff=models.BooleanField(default=False)
    # is_user=models.BooleanField(default=False),
    # is_admin=models.BooleanField(default=False)
    

    def __str__(self):
        return self.email