from django.urls import path, include

from . import views

app_name = "blog"

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("post/<slug:slug>/", views.PostDetailView.as_view(), name="post_detail"),
    path("create/", views.PostCreateView.as_view(), name="create"),
    path("blog/api/v1/", include("blog.api.v1.urls")),
]