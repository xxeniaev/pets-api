from rest_framework import serializers
from .models import PetModel, PhotoModel


class PhotoSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.FileField()

    class Meta:
        model = PhotoModel
        fields = ('id', 'url')


class PetSerializer(serializers.HyperlinkedModelSerializer):
    photos = PhotoSerializer(read_only=True, many=True)
    age = serializers.ReadOnlyField()

    class Meta:
        model = PetModel
        fields = ('id', 'name', 'age', 'type', 'photos', 'created_at', 'birth_date')


class PetNewSerializer(serializers.HyperlinkedModelSerializer):
    photos = PhotoSerializer(read_only=True, many=True)
    age = serializers.ReadOnlyField()

    class Meta:
        model = PetModel
        fields = ('id', 'name', 'age', 'type', 'photos', 'created_at')
