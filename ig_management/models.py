from django.db import models
from django.utils import timezone
from django.conf import settings
from sm_accounts.models import InstagramAccounts


# Create your models here.
class IGPage(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=None, null=True, blank=True)
    sm_account = models.ForeignKey(InstagramAccounts, on_delete=models.CASCADE, default=None, null=True, blank=True)
    page_id = models.BigIntegerField(default=None, null=True, blank=True)
    page_ig_id = models.BigIntegerField(default=None, null=True, blank=True)  # Don't know this ID.
    modified_on = models.DateTimeField(default=timezone.now, null=True, blank=True)
    name = models.CharField(max_length=128, default=None, null=True, blank=True)
    username = models.CharField(max_length=128, default=None, null=True, blank=True)
    picture = models.URLField(max_length=4096, null=True, blank=True)
    followers_count = models.BigIntegerField(default=None, null=True, blank=True)
    follows_count = models.BigIntegerField(default=None, null=True, blank=True)
    website = models.URLField(max_length=4096, null=True, blank=True)
    biography = models.TextField(max_length=10000, default=None, null=True, blank=True)
    media_count = models.BigIntegerField(default=None, null=True, blank=True)

    objects = models.Manager()

    class Meta:
        ordering = ('id',)

    def __str__(self):
        return str(self.id)


class IGPost(models.Model):
    page = models.ForeignKey(IGPage, on_delete=models.CASCADE, default=None, null=True, blank=True)
    post_id = models.BigIntegerField(default=None, null=True, blank=True)
    post_ig_id = models.BigIntegerField(default=None, null=True, blank=True)  # Don't know this ID.
    shortcode = models.CharField(max_length=64, default=None, null=True, blank=True)
    owner = models.CharField(max_length=128, default=None, null=True, blank=True)
    username = models.CharField(max_length=128, default=None, null=True, blank=True)
    created_on = models.DateTimeField(default=timezone.now, null=True, blank=True)
    modified_on = models.DateTimeField(default=timezone.now, null=True, blank=True)
    ig_link = models.URLField(max_length=1024, default=None, null=True, blank=True)
    media_type = models.CharField(max_length=64, default=None, null=True, blank=True)
    media = models.JSONField(default=None, null=True, blank=True)
    caption = models.TextField(max_length=2560, default=None, null=True, blank=True)
    like_count = models.BigIntegerField(default=None, null=True, blank=True)
    can_comment = models.BooleanField(default=None, null=True, blank=True)
    comment_count = models.BigIntegerField(default=None, null=True, blank=True)

    rating = models.DecimalField(max_digits=2, decimal_places=1, default=None, null=True, blank=True)

    objects = models.Manager()

    class Meta:
        ordering = ('-created_on',)

    def __str__(self):
        return str(self.id)


class IGPostComment(models.Model):
    post = models.ForeignKey(IGPost, on_delete=models.CASCADE, default=None, null=True, blank=True)
    comment_id = models.BigIntegerField(default=None, null=True, blank=True)
    ig_user_id = models.BigIntegerField(default=None, null=True, blank=True)
    ig_user_name = models.CharField(max_length=128, default=None, null=True, blank=True)
    created_on = models.DateTimeField(default=timezone.now, null=True, blank=True)
    modified_on = models.DateTimeField(default=timezone.now, null=True, blank=True)
    is_hidden = models.BooleanField(default=None, null=True, blank=True)
    text = models.TextField(max_length=2560, default=None, null=True, blank=True)
    like_count = models.BigIntegerField(default=None, null=True, blank=True)
    replies_count = models.BigIntegerField(default=None, null=True, blank=True)
    replies = models.JSONField(default=None, null=True, blank=True)
    comment_post_id = models.BigIntegerField(default=None, null=True, blank=True)
    sentiment = models.CharField(max_length=32, default=None, null=True, blank=True)

    objects = models.Manager()

    class Meta:
        ordering = ('-created_on',)

    def __str__(self):
        return str(self.id)
