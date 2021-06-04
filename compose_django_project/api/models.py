from django.db import models

# Create your models here.


class Pet(models.Model):
    name = models.CharField(max_length=60)
    age = models.IntegerField()
    type = models.CharField(max_length=60)
    photos = models.CharField(max_length=60)
    created_at = models.DateField()
