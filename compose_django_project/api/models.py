from django.db import models


class PhotoModel(models.Model):
    url = models.FileField(null=True)


class PetModel(models.Model):
    name = models.CharField(max_length=30)
    age = models.IntegerField()
    type = models.CharField(max_length=15, blank=False)
    photos = models.ManyToManyField(PhotoModel, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
