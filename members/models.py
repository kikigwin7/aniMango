import os
from PIL import Image
from random import randint

from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from aniMango.bleach_html import bleach_tinymce, bleach_no_tags

def user_avatar_path(instance, filename):
	name, ext = os.path.splitext(filename)
	return 'user_avatars/{0!s}{1!s}'.format(instance.user.username, ext)

class OverwriteStorage(FileSystemStorage):
	def get_available_name(self, name, max_length):
		"""Returns a filename that's free on the target storage system, and
		available for new content to be written to.

		Found at http://djangosnippets.org/snippets/976/

		This file storage solves overwrite on upload problem. Another
		proposed solution was to override the save method on the model
		like so (from https://code.djangoproject.com/ticket/11663):

		def save(self, *args, **kwargs):
			try:
				this = MyModelName.objects.get(id=self.id)
				if this.MyImageFieldName != self.MyImageFieldName:
					this.MyImageFieldName.delete()
			except: pass
			super(MyModelName, self).save(*args, **kwargs)
		"""
		# If the filename already exists, remove it as if it was a true file system
		if self.exists(name):
			os.remove(os.path.join(settings.MEDIA_ROOT, name))
		return name

def get_rand_nick():
	return 'AniSoc member #{0!s}'.format(randint(0,1000000))

# Simple member model to extend the default user model
class Member(models.Model):
	user = models.OneToOneField(
		settings.AUTH_USER_MODEL,
		on_delete=models.CASCADE,
		primary_key=True
	)
	# Setting default nick does not leak uID and full name
	nick = models.CharField(max_length=30, blank=True, default=get_rand_nick)
	show_full_name = models.BooleanField(default=False)
	bio = models.TextField(blank=True, null=True)
	img = models.ImageField(upload_to=user_avatar_path, storage=OverwriteStorage(), height_field='img_height', width_field='img_width', blank=True, null=True)
	img_height=models.PositiveIntegerField(blank=True, null=True)
	img_width=models.PositiveIntegerField(blank=True, null=True)
	discordTag = models.CharField(max_length=40, blank=True)

	def __str__(self):
		# Nick can be set by self and is most anonymous
		# Username is uni ID, which may be somewhat sensitive, so it is used only if nick is not available
		# Full name is, imo, the most sensitive, so it is by default not shown (especially because many
		# may not even connect to site and change settings, so it would be on the web forever)
		# However, if user wants to show their name, then it is displayed instead of uID, because
		# we assume user knows what they are doing and so not showing uID releases less information
		# -Sorc
		if self.nick:
			return self.nick
		elif self.show_full_name:
			return self.user.get_full_name()
		else:
			return self.user.username

	def save(self, *args, **kwargs):
		self.nick = bleach_no_tags(self.nick)
		self.bio = bleach_tinymce(self.bio)
		self.discordTag = bleach_no_tags(self.discordTag)

		#TODO: old images can still stay on the server, as different extensions can be used (.jpeg, .jpg, .png and etc.). Not too problematic but might want to fix - Sorc
		#Save new image to file first -Sorc
		super(Member, self).save(*args,  **kwargs)

		dim = 128, 128
		if self.img and (self.img_height != dim[1] or self.img_width != dim[0]):
			try:
				new_img = Image.open(self.img.path).convert("RGB")
				######
				#http://matthiaseisen.com/pp/patterns/p0202/
				shorter_side_by_half = min(new_img.size) / 2
				half_the_width = new_img.size[0] / 2
				half_the_height = new_img.size[1] / 2
				new_img.crop(
					(
						half_the_width - shorter_side_by_half,
						half_the_height - shorter_side_by_half,
						half_the_width + shorter_side_by_half,
						half_the_height + shorter_side_by_half
					)
				).resize(dim, Image.ANTIALIAS).save(self.img.path, quality=90)
				#######
				self.img_height = dim[1]
				self.img_width = dim[0]
				super(Member, self).save(*args,  **kwargs)
			except Exception as e:
				raise

	def is_privileged(self):
		return self.user.groups.filter(name='President').exists() or self.user.is_superuser

# Ensure a blank member object is created for each user using django post_save
# Would normally do a save override but not safe to do on the django user model
# https://coderwall.com/p/ktdb3g/django-signals-an-extremely-simplified-explanation-for-beginners
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def ensure_profile_exists(sender, **kwargs):
	if kwargs.get('created', False):
		Member.objects.get_or_create(user=kwargs.get('instance'))
