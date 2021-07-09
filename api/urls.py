from django.urls import include, path, re_path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
# path to pets list
router.register(r'pets', views.PetViewSet, basename="pets")
# path to all photos
router.register(r'pets/(?P<id>[\d\-\w]+)/photo', views.PhotoViewSet, basename="photos")

urlpatterns = [
    path('', include(router.urls)),
    # path to image
    re_path(r'(?P<img_path>[a-zA-Z0-9\-\_\.]+\.[\w]+)', views.render_image, name="image"),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
