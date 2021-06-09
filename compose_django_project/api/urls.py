from django.urls import include, path, re_path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'pets', views.PetViewSet, basename="pets")
router.register(r'pets/(?P<id>\d+)/photo', views.PhotoViewSet, basename="photo")

urlpatterns = [
    path('', include(router.urls)),
    re_path(r'(?P<img_path>[a-zA-Z0-9\-\_]+\.[\w]+)', views.render_image),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
