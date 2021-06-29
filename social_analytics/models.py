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

    class Meta:
        ordering = ('datetime',)

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

    class Meta:
        ordering = ('-datetime',)

    def __str__(self):
        return str(self.id)


class IGPageMetricsCorrelation(models.Model):
    page = models.ForeignKey(IGPage, on_delete=models.CASCADE, default=None, null=True, blank=True)
    pageID = models.BigIntegerField(default=None, null=True, blank=True)
    created_on = models.DateTimeField(default=None, null=True, blank=True)
    updated_on = models.DateTimeField(default=None, null=True, blank=True)
    impressions_reach = models.DecimalField(default=0, max_digits=4, decimal_places=2)
    impressions_follower_count = models.DecimalField(default=0, max_digits=4, decimal_places=2)
    impression_profile_views = models.DecimalField(default=0, max_digits=4, decimal_places=2)
    reach_follower_count = models.DecimalField(default=0, max_digits=4, decimal_places=2)
    reach_profile_views = models.DecimalField(default=0, max_digits=4, decimal_places=2)
    profile_views_follower_count = models.DecimalField(default=0, max_digits=4, decimal_places=2)

    objects = models.Manager()

    class Meta:
        ordering = ('id',)


class IGPageDailyAnalytics(models.Model):
    page = models.ForeignKey(IGPage, on_delete=models.CASCADE, default=None, null=True, blank=True)
    pageID = models.BigIntegerField(default=None, null=True, blank=True)
    datetime = models.DateTimeField(default=None, null=True, blank=True)
    impressions = models.IntegerField(default=0, null=True, blank=True)
    reach = models.IntegerField(default=0, null=True, blank=True)
    follower_count = models.IntegerField(default=0, null=True, blank=True)
    email_contacts = models.IntegerField(default=0, null=True, blank=True)
    phone_call_clicks = models.IntegerField(default=0, null=True, blank=True)
    text_message_clicks = models.IntegerField(default=0, null=True, blank=True)
    directions_clicks = models.IntegerField(default=0, null=True, blank=True)
    website_clicks = models.IntegerField(default=0, null=True, blank=True)
    profile_views = models.IntegerField(default=0, null=True, blank=True)

    objects = models.Manager()

    class Meta:
        ordering = ('datetime',)

    def __str__(self):
        return str(self.id)


class IGPageDailyImpressions(models.Model):
    page = models.ForeignKey(IGPage, on_delete=models.CASCADE, default=None, null=True, blank=True)
    pageID = models.BigIntegerField(default=None, null=True, blank=True)
    datetime = models.DateTimeField(default=None, null=True, blank=True)
    impressions = models.IntegerField(default=0, null=True, blank=True)

    objects = models.Manager()

    class Meta:
        ordering = ('datetime',)

    def __str__(self):
        return str(self.id)


class IGPageDailyReach(models.Model):
    page = models.ForeignKey(IGPage, on_delete=models.CASCADE, default=None, null=True, blank=True)
    pageID = models.BigIntegerField(default=None, null=True, blank=True)
    datetime = models.DateTimeField(default=None, null=True, blank=True)
    reach = models.IntegerField(default=0, null=True, blank=True)

    objects = models.Manager()

    class Meta:
        ordering = ('datetime',)

    def __str__(self):
        return str(self.id)


class IGPageDailyFollowerCount(models.Model):
    page = models.ForeignKey(IGPage, on_delete=models.CASCADE, default=None, null=True, blank=True)
    pageID = models.BigIntegerField(default=None, null=True, blank=True)
    datetime = models.DateTimeField(default=None, null=True, blank=True)
    follower_count = models.IntegerField(default=0, null=True, blank=True)

    objects = models.Manager()

    class Meta:
        ordering = ('datetime',)

    def __str__(self):
        return str(self.id)


class IGPageDailyEmailContacts(models.Model):
    page = models.ForeignKey(IGPage, on_delete=models.CASCADE, default=None, null=True, blank=True)
    pageID = models.BigIntegerField(default=None, null=True, blank=True)
    datetime = models.DateTimeField(default=None, null=True, blank=True)
    email_contacts = models.IntegerField(default=0, null=True, blank=True)

    objects = models.Manager()

    class Meta:
        ordering = ('datetime',)

    def __str__(self):
        return str(self.id)


class IGPageDailyPhoneCallClicks(models.Model):
    page = models.ForeignKey(IGPage, on_delete=models.CASCADE, default=None, null=True, blank=True)
    pageID = models.BigIntegerField(default=None, null=True, blank=True)
    datetime = models.DateTimeField(default=None, null=True, blank=True)
    phone_call_clicks = models.IntegerField(default=0, null=True, blank=True)

    objects = models.Manager()

    class Meta:
        ordering = ('datetime',)

    def __str__(self):
        return str(self.id)


class IGPageDailyTextMessageClicks(models.Model):
    page = models.ForeignKey(IGPage, on_delete=models.CASCADE, default=None, null=True, blank=True)
    pageID = models.BigIntegerField(default=None, null=True, blank=True)
    datetime = models.DateTimeField(default=None, null=True, blank=True)
    text_message_clicks = models.IntegerField(default=0, null=True, blank=True)

    objects = models.Manager()

    class Meta:
        ordering = ('datetime',)

    def __str__(self):
        return str(self.id)


class IGPageDailyDirectionsClicks(models.Model):
    page = models.ForeignKey(IGPage, on_delete=models.CASCADE, default=None, null=True, blank=True)
    pageID = models.BigIntegerField(default=None, null=True, blank=True)
    datetime = models.DateTimeField(default=None, null=True, blank=True)
    directions_clicks = models.IntegerField(default=0, null=True, blank=True)

    objects = models.Manager()

    class Meta:
        ordering = ('datetime',)

    def __str__(self):
        return str(self.id)


class IGPageDailyWebsiteClicks(models.Model):
    page = models.ForeignKey(IGPage, on_delete=models.CASCADE, default=None, null=True, blank=True)
    pageID = models.BigIntegerField(default=None, null=True, blank=True)
    datetime = models.DateTimeField(default=None, null=True, blank=True)
    website_clicks = models.IntegerField(default=0, null=True, blank=True)

    objects = models.Manager()

    class Meta:
        ordering = ('datetime',)

    def __str__(self):
        return str(self.id)


class IGPageDailyProfileViews(models.Model):
    page = models.ForeignKey(IGPage, on_delete=models.CASCADE, default=None, null=True, blank=True)
    pageID = models.BigIntegerField(default=None, null=True, blank=True)
    datetime = models.DateTimeField(default=None, null=True, blank=True)
    profile_views = models.IntegerField(default=0, null=True, blank=True)

    objects = models.Manager()

    class Meta:
        ordering = ('datetime',)

    def __str__(self):
        return str(self.id)


class IGPostAnalytic(models.Model):
    post = models.ForeignKey(IGPost, on_delete=models.CASCADE, default=None, null=True, blank=True)
    pageID = models.BigIntegerField(default=None, null=True, blank=True)
    postID = models.BigIntegerField(default=None, null=True, blank=True)
    created_on = models.DateTimeField(default=None, null=True, blank=True)
    updated_on = models.DateTimeField(default=None, null=True, blank=True)
    impressions = models.IntegerField(default=0, null=True, blank=True)
    reach = models.IntegerField(default=0, null=True, blank=True)
    engagement = models.IntegerField(default=0, null=True, blank=True)
    saved = models.IntegerField(default=0, null=True, blank=True)
    video_views = models.IntegerField(default=0, null=True, blank=True)

    objects = models.Manager()

    class Meta:
        ordering = ('created_on',)

    def __str__(self):
        return str(self.id)


class IGPostRating(models.Model):
    page = models.ForeignKey(IGPage, on_delete=models.CASCADE, default=None, null=True, blank=True)
    post = models.ForeignKey(IGPost, on_delete=models.CASCADE, default=None, null=True, blank=True)
    pageID = models.BigIntegerField(default=None, null=True, blank=True)
    postID = models.BigIntegerField(default=None, null=True, blank=True)
    datetime = models.DateTimeField(default=None, null=True, blank=True)
    rating = models.DecimalField(default=0, max_digits=2, decimal_places=1)

    objects = models.Manager()

    class Meta:
        ordering = ('datetime',)

    def __str__(self):
        return str(self.id)


class IGBestPostTime(models.Model):
    page = models.ForeignKey(IGPage, on_delete=models.CASCADE, default=None, null=True, blank=True)
    pageID = models.BigIntegerField(default=None, null=True, blank=True)
    modified_on = models.DateTimeField(default=None, null=True, blank=True)
    start = models.IntegerField(default=None, null=True, blank=True)
    end = models.IntegerField(default=None, null=True, blank=True)

    objects = models.Manager()

    class Meta:
        ordering = ('id',)

    def __str__(self):
        return str(self.id)
