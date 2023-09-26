from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=255)
    amount = models.IntegerField()
    description = models.TextField()

    def __unicode__(self):
        return self
