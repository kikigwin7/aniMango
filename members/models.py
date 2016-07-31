from django.db import models
# Use django settings to reference the AUTH_USER_MODEL
from django.conf import settings

# Simple member model to extend the default user model
class Member(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        primary_key=True
    )
    nick = models.CharField(max_length=30, blank=True)
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.nick