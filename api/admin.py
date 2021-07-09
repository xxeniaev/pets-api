from django.contrib import admin


from .models import PetModel, PhotoModel
admin.site.register(PetModel)
admin.site.register(PhotoModel)
