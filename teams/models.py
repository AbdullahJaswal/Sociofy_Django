from django.db import models
from django.utils import timezone
from django.conf import settings

from users.models import User
from sm_accounts.models import Role

from fb_management.models import FBPage
from ig_management.models import IGPage


# Create your models here.
class Team(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=None, null=True, blank=True)
    fb_page = models.ForeignKey(FBPage, on_delete=models.CASCADE, default=None, null=True, blank=True)
    ig_page = models.ForeignKey(IGPage, on_delete=models.CASCADE, default=None, null=True, blank=True)
    created_on = models.DateTimeField(default=None, null=True, blank=True)
    modified_on = models.DateTimeField(default=None, null=True, blank=True)
    name = models.CharField(max_length=128, default=None, null=True, blank=True)

    objects = models.Manager()

    class Meta:
        ordering = ('id',)

    def __str__(self):
        return str(self.id)


class Member(models.Model):
    options = (
        ('pending', 'Pending'),
        ('joined', 'Joined'),
        ('declined', 'Declined'),
        ('left', 'Left')
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None, null=True, blank=True)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, default=None, null=True, blank=True)
    role = models.ForeignKey(Role, on_delete=models.CASCADE, default=None, null=True, blank=True)
    added_on = models.DateTimeField(default=None, null=True, blank=True)
    modified_on = models.DateTimeField(default=None, null=True, blank=True)
    joined_on = models.DateTimeField(default=None, null=True, blank=True)
    declined_on = models.DateTimeField(default=None, null=True, blank=True)
    left_on = models.DateTimeField(default=None, null=True, blank=True)
    status = models.CharField(max_length=16, choices=options, default='pending')

    class Meta:
        ordering = ('id',)

    def __str__(self):
        return str(self.id)


class Task(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, default=None, null=True, blank=True)
    member = models.ManyToManyField(Member, default=None, blank=True)
    created_on = models.DateTimeField(default=None, null=True, blank=True)
    modified_on = models.DateTimeField(default=None, null=True, blank=True)
    due_on = models.DateTimeField(default=None, null=True, blank=True)
    task = models.CharField(max_length=128, default=None, null=True, blank=True)
    description = models.CharField(max_length=2056, default=None, null=True, blank=True)

    class Meta:
        ordering = ('due_on',)

    def __str__(self):
        return str(self.id)
