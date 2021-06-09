from django.db import models

# Create your models here.


class PhotoModel(models.Model):
    url = models.FileField(null=True)


class PetModel(models.Model):
    # id = models.CharField(max_length=100, unique=True, primary_key=True, editable=False)
    name = models.CharField(max_length=30)
    age = models.IntegerField()
    type = models.CharField(max_length=15, blank=False)
    photos = models.ManyToManyField(PhotoModel, blank=True)
    created_at = models.DateField()
