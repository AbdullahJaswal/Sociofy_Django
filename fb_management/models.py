from django.db import models
from django.utils import timezone
from django.conf import settings
from sm_accounts.models import FacebookAccounts


# Create your models here.
class FBPage(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=None, null=True, blank=True)
    sm_account = models.ForeignKey(FacebookAccounts, on_delete=models.CASCADE, default=None, null=True, blank=True)
    page_id = models.BigIntegerField(default=None, null=True, blank=True)
    created_on = models.DateTimeField(default=timezone.now, null=True, blank=True)
    modified_on = models.DateTimeField(default=timezone.now, null=True, blank=True)
    name = models.CharField(max_length=128, default=None, null=True, blank=True)
    username = models.CharField(max_length=128, default=None, null=True, blank=True)
    fb_link = models.URLField(max_length=1024, default=None, null=True, blank=True)
    verification_status = models.CharField(max_length=16, default=None, null=True, blank=True)
    followers_count = models.BigIntegerField(default=None, null=True, blank=True)
    likes = models.BigIntegerField(default=None, null=True, blank=True)
    picture = models.URLField(max_length=4096, null=True, blank=True)
    cover = models.URLField(max_length=4096, null=True, blank=True)
    category = models.CharField(max_length=64, default=None, null=True, blank=True)
    about = models.TextField(max_length=10000, default=None, null=True, blank=True)
    email = models.EmailField(max_length=128, default=None, null=True, blank=True)
    phone = models.CharField(max_length=64, default=None, null=True, blank=True)
    whatsapp_number = models.CharField(max_length=64, default=None, null=True, blank=True)
    website = models.URLField(max_length=2048, default=None, null=True, blank=True)
    can_post = models.BooleanField(default=True, null=True, blank=True)
    connected_instagram_account = models.BigIntegerField(default=None, null=True, blank=True)

    objects = models.Manager()

    class Meta:
        ordering = ('id',)

    def __str__(self):
        return str(self.id)


class FBPost(models.Model):
    page = models.ForeignKey(FBPage, on_delete=models.CASCADE, default=None, null=True, blank=True)
    post_id = models.CharField(max_length=128, default=None, null=True, blank=True)
    created_time = models.DateTimeField(default=None, null=True, blank=True)
    updated_time = models.DateTimeField(default=None, null=True, blank=True)
    modified_on = models.DateTimeField(default=timezone.now, null=True, blank=True)
    application = models.BooleanField(default=None, null=True, blank=True)
    message = models.TextField(max_length=64000, default=None, null=True, blank=True)
    link = models.URLField(max_length=2048, default=None, null=True, blank=True)
    media = models.JSONField(default=None, null=True, blank=True)
    timeline_visibility = models.CharField(max_length=32, default=None, null=True, blank=True)
    is_hidden = models.BooleanField(default=None, null=True, blank=True)
    is_published = models.BooleanField(default=None, null=True, blank=True)
    is_expired = models.BooleanField(default=None, null=True, blank=True)
    permalink_url = models.URLField(max_length=2048, default=None, null=True, blank=True)
    reactions = models.JSONField(default=None, null=True, blank=True)
    comment_count = models.IntegerField(default=None, null=True, blank=True)
    shares = models.IntegerField(default=None, null=True, blank=True)
    privacy = models.CharField(max_length=64, default=None, null=True, blank=True)
    status_type = models.CharField(max_length=64, default=None, null=True, blank=True)

    objects = models.Manager()

    class Meta:
        ordering = ('-created_time',)

    def __str__(self):
        return str(self.id)


class FBPostComment(models.Model):
    post = models.ForeignKey(FBPost, on_delete=models.CASCADE, default=None, null=True, blank=True)
    comment_id = models.CharField(max_length=128, default=None, null=True, blank=True)
    created_time = models.DateTimeField(default=None, null=True, blank=True)
    modified_on = models.DateTimeField(default=timezone.now, null=True, blank=True)
    fb_user_id = models.CharField(max_length=128, default=None, null=True, blank=True)
    fb_user_name = models.CharField(max_length=128, default=None, null=True, blank=True)
    can_comment = models.BooleanField(default=None, null=True, blank=True)
    attachment_type = models.CharField(max_length=128, default=None, null=True, blank=True)
    attachment = models.URLField(max_length=2048, default=None, null=True, blank=True)
    message = models.TextField(max_length=64000, default=None, null=True, blank=True)
    reactions_count = models.IntegerField(default=None, null=True, blank=True)
    reactions = models.JSONField(default=None, null=True, blank=True)
    replies_count = models.IntegerField(default=None, null=True, blank=True)
    replies = models.JSONField(default=None, null=True, blank=True)

    objects = models.Manager()

    class Meta:
        ordering = ('-created_time',)

    def __str__(self):
        return str(self.id)


class FBPostTag(models.Model):
    page = models.ForeignKey(FBPage, on_delete=models.CASCADE, default=None, null=True, blank=True)
    tag_id = models.CharField(max_length=128, default=None, null=True, blank=True)
    tag = models.CharField(max_length=128, default=None, null=True, blank=True)
    created_on = models.DateTimeField(default=timezone.now, null=True, blank=True)
    modified_on = models.DateTimeField(default=timezone.now, null=True, blank=True)

    objects = models.Manager()

    class Meta:
        ordering = ('id',)

    def __str__(self):
        return str(self.id)
