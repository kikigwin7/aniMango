from django.db import models
# Use django settings to reference the AUTH_USER_MODEL
from django.conf import settings

class Item(models.Model):
    parent_series = models.ForeignKey(
        'series.Series',
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=100)
    media = models.CharField(max_length=15)
    details = models.CharField(
        max_length=30,
        blank=True
    )
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Loan(models.Model):
    loan_item = models.ForeignKey(
        Item,
        on_delete=models.CASCADE
    )
    loan_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    return_date = models.DateField()
    returned = models.BooleanField(default=False)

    def __str__(self):
        return self.loan_user.str() + self.loan_item.str()