from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Create your models here.
class AccountManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        user = self.model(
            username=username,
            email=email
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password, email=""):
        user = self.create_user(username, email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class Account(AbstractBaseUser):
    objects = AccountManager()

    username = models.CharField(unique=True, max_length=64)
    email = models.EmailField(unique=True, blank=True, null=True)

    #Dates
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)

    #Roles
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'username'

    def has_perm(self, perm, obj=None):
        return self.is_staff

    def has_module_perms(self, package_name):
        return True

    def save(self, *args, **kwargs):
        super(Account, self).save(*args, **kwargs)

    def __str__(self):
        return self.username