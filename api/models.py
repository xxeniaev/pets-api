from datetime import datetime

from django.db import models
import uuid


class PhotoModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    url = models.FileField()


class PetModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=30)
    type = models.CharField(max_length=15, blank=False)
    photos = models.ManyToManyField(PhotoModel, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    birth_date = models.DateField(blank=False, default=datetime.today().strftime('%Y-%m-%d'))

    @property
    def age(self):
        """
        Get auto-calculated age based on birthday
        :return: age
        """
        now = datetime.today()
        birthday = datetime.strptime(self.birth_date.strftime('%Y-%m-%d'), '%Y-%m-%d')
        dif = (now - birthday).days
        return int(dif/365.2425)
