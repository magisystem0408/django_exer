from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
# Create your models here.

from django.urls import reverse_lazy


class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        if not email:
            raise ValueError('Enter email')
        user = self.model(
            username=username,
            email=email
        )
        user.set_password(password)
        user.save(using=self._db)
        return user


class Users(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=150)
    email = models.EmailField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    # このテーブルを一意に識別するためのFIELD
    USERNAME_FIELD = 'email'

    # SUPERUSERを作成するために必要なフィールド
    REQUIRED_FIELDS = ['username', ]

    objects = UserManager()

    def get_absolute_url(self):
        return reverse_lazy("accounts:home")