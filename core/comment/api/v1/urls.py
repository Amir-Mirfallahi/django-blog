from django.urls import path
from .views import CreateCommentApiView

app_name="api-v1"

urlpatterns = [
    path("create/", CreateCommentApiView.as_view(), name="create"),
]