from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


# Create your models here.
class CustomAccountManager(BaseUserManager):
    def create_superuser(self, email_address, username, first_name, last_name, password, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError('Superuser must be assigned to is_staff=True')

        if other_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must be assigned to is_superuser=True')

        return self.create_user(email_address, username, first_name, last_name, password, **other_fields)

    def create_user(self, email_address, username, first_name, last_name, password, **other_fields):
        if not email_address:
            raise ValueError(gettext_lazy(
                'You must provide an email address!'))

        email_address = self.normalize_email(email_address)
        user = self.model(email_address=email_address, username=username,
                          first_name=first_name, last_name=last_name, **other_fields)

        user.set_password(password)
        user.save()

        return user


class User(AbstractBaseUser, PermissionsMixin):
    email_address = models.EmailField(gettext_lazy('email address'), unique=True)
    username = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    created_on = models.DateTimeField(default=timezone.now)
    # about = models.TextField(gettext_lazy('about'), max_length=500, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = CustomAccountManager()

    USERNAME_FIELD = 'email_address'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def __str__(self):
        return str(self.id)
