from django.contrib import admin
# Import the series model
from .models import Series

# Register model with admin site
admin.site.register(Series)