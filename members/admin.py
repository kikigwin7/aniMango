from django.contrib import admin

# Get the models for the members app
from .models import Member

# Register this model with the admin site
admin.site.register(Member)