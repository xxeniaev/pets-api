from datetime import datetime

from django.db import models
import uuid


class PhotoModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    url = models.FileField(null=True)


class PetModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=30)
    type = models.CharField(max_length=15, blank=False)
    photos = models.ManyToManyField(PhotoModel, blank=True)
    created_at = models.DateField(auto_now_add=True)
    birth_date = models.DateField(blank=False, default=datetime.today().strftime('%Y-%m-%d'))

    @property
    def age(self):
        return int(datetime.today().year - self.birth_date.year)
