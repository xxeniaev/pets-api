from django.contrib import admin

# Register your models here.

from .models import PetModel, PhotoModel
admin.site.register(PetModel)
admin.site.register(PhotoModel)
