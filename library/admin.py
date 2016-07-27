from django.contrib import admin
# Import the models for the library app
from .models import Item, Loan

# Register model with admin site
admin.site.register(Item)
admin.site.register(Loan)