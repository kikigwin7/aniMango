from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from tinymce.widgets import TinyMCE

# Get the models for the members app
from .models import Member


class MemberForm(forms.ModelForm):
    bio = forms.CharField(required=False, widget=TinyMCE())


# Define an inline admin descriptor for Member model
# which acts a bit like a singleton
class MemberInline(admin.StackedInline):
    form = MemberForm
    model = Member
    can_delete = False


# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (MemberInline,)


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
