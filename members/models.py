from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
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

    def nick_or_name(self):
        if self.nick is not '':
            return self.nick
        elif self.user.get_full_name() is not '':
            return self.user.get_full_name()
        else:
            return self.user.username

# Ensure a blank member object is created for each user using django post_save
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def ensure_profile_exists(sender, **kwargs):
    if kwargs.get('created', False):
        Member.objects.get_or_create(user=kwargs.get('instance'))