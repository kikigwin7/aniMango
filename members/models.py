from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
# Use django settings to reference the AUTH_USER_MODEL
from django.conf import settings
from PIL import Image
import os

# Simple member model to extend the default user model
class Member(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        primary_key=True
    )
    nick = models.CharField(max_length=30, blank=True)
    bio = models.TextField(blank=True)
    img = models.ImageField(blank=True)

    def __str__(self):
        if self.nick:
            return self.nick
        else:
            return self.user.get_full_name()

    def save(self, *args, **kwargs):
        if self.img:
            orig = Member.objects.get(pk=self.pk)
            if orig.img != self.img:
                if orig.img:
                    os.remove(orig.img.path)
                name, ext = os.path.splitext(str(self.img))
                new_img = Image.open(self.img)
                #new_img = new_img.resize((100,100), Image.LANCZOS)
                new_img.thumbnail((100,100))
                new_img_name = str(self.user.username) + ext
                # PIL needs explicit media root defined
                new_img.save(os.path.join(settings.MEDIA_ROOT,new_img_name))
                # Saving to django model automatically prepends media root
                self.img = new_img_name
            super(Member, self).save(*args,  **kwargs) # Call real save
        else:
            super(Member, self).save(*args,  **kwargs) # Call real save

# Ensure a blank member object is created for each user using django post_save
# Would normally do a save override but not safe to do on the django user model
# https://coderwall.com/p/ktdb3g/django-signals-an-extremely-simplified-explanation-for-beginners
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def ensure_profile_exists(sender, **kwargs):
    if kwargs.get('created', False):
        Member.objects.get_or_create(user=kwargs.get('instance'))