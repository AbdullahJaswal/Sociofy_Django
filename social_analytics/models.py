from django.db import models
from django.utils import timezone
from django.conf import settings

from ig_management.models import *


# Create your models here.
class IGPageAnalytic(models.Model):
    page = models.ForeignKey(IGPage, on_delete=models.CASCADE, default=None, null=True, blank=True)
    pageID = models.BigIntegerField(default=None, null=True, blank=True)
    datetime = models.DateTimeField(default=None, null=True, blank=True)
    today = models.BooleanField(default=None, null=True, blank=True)
    impressions = models.IntegerField(default=None, null=True, blank=True)
    reach = models.IntegerField(default=None, null=True, blank=True)
    follower_count = models.IntegerField(default=None, null=True, blank=True)
    email_contacts = models.IntegerField(default=None, null=True, blank=True)
    phone_call_clicks = models.IntegerField(default=None, null=True, blank=True)
    text_message_clicks = models.IntegerField(default=None, null=True, blank=True)
    get_directions_clicks = models.IntegerField(default=None, null=True, blank=True)
    website_clicks = models.IntegerField(default=None, null=True, blank=True)
    profile_views = models.IntegerField(default=None, null=True, blank=True)

    objects = models.Manager()

    def __str__(self):
        return str(self.id)


class IGPageDemographyAnalytic(models.Model):
    page = models.ForeignKey(IGPage, on_delete=models.CASCADE, default=None, null=True, blank=True)
    pageID = models.BigIntegerField(default=None, null=True, blank=True)
    datetime = models.DateTimeField(default=None, null=True, blank=True)
    audience_gender_age = models.JSONField(default=None, null=True, blank=True)
    audience_locale = models.JSONField(default=None, null=True, blank=True)
    audience_country = models.JSONField(default=None, null=True, blank=True)
    audience_city = models.JSONField(default=None, null=True, blank=True)

    objects = models.Manager()

    def __str__(self):
        return self.id
