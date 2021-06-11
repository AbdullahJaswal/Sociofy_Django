from django.db import models
from django.conf import settings
from django.utils import timezone

from django_cryptography.fields import encrypt  # noqa. <-- Used to suppress error highlight.


# Create your models here.
class Role(models.Model):
    admin = models.BooleanField(default=None, null=True, blank=True)
    observer = models.BooleanField(default=None, null=True, blank=True)
    management = models.BooleanField(default=None, null=True, blank=True)
    analytics = models.BooleanField(default=None, null=True, blank=True)

    objects = models.Manager()

    class Meta:
        ordering = ('id',)

    def __str__(self):
        return str(self.id)


class FacebookApp(models.Model):
    app_id = encrypt(models.CharField(max_length=64, default=None, null=True, blank=True))
    app_secret = encrypt(models.CharField(max_length=128, default=None, null=True, blank=True))
    app_name = models.CharField(max_length=32, default=None, null=True, blank=True)

    objects = models.Manager()

    class Meta:
        ordering = ('id',)

    def __str__(self):
        return self.app_name


class FacebookAccounts(models.Model):
    options = (
        ('short', 'Short'),
        ('long', 'Long')
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=None, null=True, blank=True)
    role = models.ForeignKey(Role, on_delete=models.CASCADE, default=None, null=True, blank=True)
    facebook_id = models.BigIntegerField(default=None, null=True, blank=True)
    length = models.CharField(max_length=8, default='short', choices=options)
    access_token = encrypt(models.CharField(max_length=512, default=None, null=True, blank=True))
    reauthorize_in_seconds = models.BigIntegerField(default=None, null=True, blank=True)
    signed_request = models.CharField(max_length=512, default=None, null=True, blank=True)
    created_on = models.DateTimeField(default=timezone.now, null=True, blank=True)
    expires_on = models.DateTimeField(default=None, null=True, blank=True)

    objects = models.Manager()

    class Meta:
        ordering = ('id',)

    def __str__(self):
        return str(self.id)


class InstagramAccounts(models.Model):
    options = (
        ('short', 'Short'),
        ('long', 'Long')
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=None, null=True, blank=True)
    role = models.ForeignKey(Role, on_delete=models.CASCADE, default=None, null=True, blank=True)
    instagram_id = models.BigIntegerField(default=None, null=True, blank=True)
    length = models.CharField(max_length=8, default='short', choices=options)
    access_token = encrypt(models.CharField(max_length=512, default=None, null=True, blank=True))
    reauthorize_in_seconds = models.BigIntegerField(default=None, null=True, blank=True)
    signed_request = models.CharField(max_length=512, default=None, null=True, blank=True)
    created_on = models.DateTimeField(default=timezone.now, null=True, blank=True)
    expires_on = models.DateTimeField(default=None, null=True, blank=True)

    objects = models.Manager()

    class Meta:
        ordering = ('id',)

    def __str__(self):
        return str(self.id)
