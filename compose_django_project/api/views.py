from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import viewsets, status
from .serializers import PetSerializer, PhotoSerializer
from .models import PetModel, PhotoModel
from rest_framework.response import Response

# Create your views here.


class PetViewSet(viewsets.ModelViewSet):
    queryset = PetModel.objects.all().order_by('id')
    serializer_class = PetSerializer

    # post
    def create(self, request):
        serializer = PetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    # get
    def list(self, request):
        qs = self.queryset
        serializer = PetSerializer(qs, many=True)
        return Response(serializer.data)

    # delete
    def destroy(self, request, pk=None):
        self.queryset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PhotoViewSet(viewsets.ModelViewSet):
    queryset = PhotoModel.objects.all()
    serializer_class = PhotoSerializer

    # post
    def create(self, request, **kwargs):
        pet_id = int(kwargs['id'])
        pet = PetModel.objects.get(pk=pet_id)
        photo_serializer = PhotoSerializer(data=request.data)
        if photo_serializer.is_valid():
            obj = photo_serializer.save()
            pet.photos.add(obj.id)
            return Response(photo_serializer.data)
        return Response(photo_serializer.errors)


def render_image(request, *args, **kwargs):
    path = kwargs['img_path']
    image_data = open(path, "rb").read()
    return HttpResponse(image_data, content_type="image/png")
