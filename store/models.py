from django.db import models


class Book(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    price = models.DecimalField(max_digits=7, decimal_places=2)

