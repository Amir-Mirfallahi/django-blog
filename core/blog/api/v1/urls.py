from . import viewsets
from django.urls import path, include
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("post", viewsets.PostModelViewSet, basename="post")
router.register("category", viewsets.CategoryModelViewSet, basename="category")

app_name="api-v1"

urlpatterns = router.urls