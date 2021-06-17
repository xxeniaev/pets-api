from django.http import HttpResponse
import json
from rest_framework import viewsets
from rest_framework.decorators import action

from .permissions import HasXAPIKey
from .serializers import PetSerializer, PhotoSerializer
from .models import PetModel, PhotoModel
from rest_framework.response import Response


class PetViewSet(viewsets.ModelViewSet):
    permission_classes = [HasXAPIKey]

    queryset = PetModel.objects
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
        query_dict = request.GET

        try:
            limit = int(query_dict.get('limit'))
        except TypeError:
            limit = 20

        try:
            offset = int(query_dict.get('offset'))
        except TypeError:
            offset = 0

        has_photos = query_dict.get('has_photos')
        if has_photos:
            if has_photos == u'true' or has_photos == u'True':
                has_photos = True
            else:
                has_photos = False
        else:
            has_photos = None

        # тут проверка на наличие фото
        qs = self.queryset

        # если есть фото
        if has_photos:
            qs = qs.exclude(photos=None)[offset:offset + limit]
        # если нет фото
        if has_photos is False:
            qs = qs.filter(photos=None)[offset:offset + limit]
        # если не важно
        if has_photos is None:
            qs = qs.all().order_by('id')[offset:offset + limit]

        serializer = PetSerializer(qs, many=True)
        serializer_data = list(serializer.data)
        response_data = {'count': len(serializer_data), 'items': serializer_data}
        return HttpResponse(json.dumps(response_data), content_type="application/json")

    # delete
    @action(methods=['delete'], detail=False)
    def delete(self, request, pk=None):
        response_data = {'deleted': 0, 'errors': []}

        delete_ids = request.data['ids']

        i = 0
        for pet_id in delete_ids:
            try:
                pet = PetModel.objects.get(pk=pet_id)
                photos = pet.photos.all()
                for photo in photos:
                    photo.delete()
                pet.delete()
                i += 1
            except PetModel.DoesNotExist:
                response_data['errors'].append({'id': pet_id, 'error': "Pet with the matching ID was not found."})

        response_data['deleted'] = i
        return HttpResponse(json.dumps(response_data), content_type="application/json")


class PhotoViewSet(viewsets.ModelViewSet):
    queryset = PhotoModel.objects.all()
    serializer_class = PhotoSerializer

    permission_classes = [HasXAPIKey]

    # post
    def create(self, request, **kwargs):
        pet_id = int(kwargs['id'])
        pet = PetModel.objects.get(pk=pet_id)
        photo_serializer = PhotoSerializer(data=request.data)
        print(request.data)
        if photo_serializer.is_valid():
            obj = photo_serializer.save()
            pet.photos.add(obj.id)
            return Response(photo_serializer.data)
        return Response(photo_serializer.errors)


def render_image(request, *args, **kwargs):
    path = kwargs['img_path']
    image_data = open(path, "rb").read()
    return HttpResponse(image_data, content_type="image/png")
