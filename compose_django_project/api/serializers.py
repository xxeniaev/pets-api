from rest_framework import serializers
from .models import Pet


class PetSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Pet
        fields = ('id', 'name', 'age', 'type', 'photos', 'created_at')
