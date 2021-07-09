from django.http import HttpResponse
import json
from rest_framework import viewsets
from rest_framework.decorators import action

from .permissions import HasXAPIKey
from .serializers import PetSerializer, PhotoSerializer, PetNewSerializer
from .models import PetModel, PhotoModel
from rest_framework.response import Response


class PetViewSet(viewsets.ModelViewSet):
    permission_classes = [HasXAPIKey]

    queryset = PetModel.objects
    serializer_class = PetSerializer

    def create(self, request):
        """
        Create pet instance

        :param request: http request

        :return: pet's info
        :rtype: Response
        """
        serializer = PetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            pet = PetModel.objects.get(pk=serializer.data['id'])
            return Response(PetNewSerializer(pet).data)
        return Response(serializer.errors)

    def list(self, request):
        """
        Get all pets with pagination filtered by having photos or not

        :param request: http request

        :return: pets
        :rtype: HttpResponse
        """
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

        # check for photo existence
        qs = self.queryset

        # filter by having photos
        if has_photos:
            qs = qs.exclude(photos=None)[offset:offset + limit]
        # filter by not having photos
        if has_photos is False:
            qs = qs.filter(photos=None)[offset:offset + limit]
        # no filter
        if has_photos is None:
            qs = qs.all()[offset:offset + limit]

        serializer = PetNewSerializer(qs, many=True)
        serializer_data = list(serializer.data)
        response_data = {'count': len(serializer_data), 'items': serializer_data}
        return HttpResponse(json.dumps(response_data), content_type="application/json")

    @action(methods=['delete'], detail=False)
    def delete(self, request, pk=None):
        """
        Delete pets and their photos by given list of ids
        TODO: move deletion login to separated component

        :param request: http request
        :param pk: primary key for deletion, default None

        :return: count of deleted pets and errors occurred
        :rtype: HttpResponse
        """
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

    def create(self, request, **kwargs):
        """
        Post photo to pet's photo list by id

        :param request: http request
        :param kwargs: gets pet's id from url

        :return: posted photo info
        :rtype: Response
        """
        pet_id = kwargs['id']
        pet = PetModel.objects.get(pk=pet_id)
        photo_serializer = PhotoSerializer(data=request.data)
        print(request.data)
        if photo_serializer.is_valid():
            obj = photo_serializer.save()
            pet.photos.add(obj.id)
            return Response(photo_serializer.data)
        return Response(photo_serializer.errors)

    def list(self, request, **kwargs):
        """
        Get all photos of pet by id

        :param request: http request
        :param kwargs: gets pet's id from url

        :return: pet's photos
        :rtype: Response
        """
        pet_id = kwargs['id']
        pet = PetModel.objects.get(pk=pet_id)
        photos = pet.photos.all()
        serializer = PhotoSerializer(photos, many=True)
        return Response(serializer.data)


def render_image(request, **kwargs):
    """
    Render one of pet's photos

    :param request: http request
    :param kwargs: gets path to image from url

    :return: http response
    :rtype: HttpResponse
    """
    path = kwargs['img_path']
    image_data = open(path, "rb").read()
    return HttpResponse(image_data, content_type="image/png")
