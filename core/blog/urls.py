from django.urls import path, include

from . import views

app_name = "blog"

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    # Manage posts
    path("posts/", views.PostListView.as_view(), name="post-list"),
    path("posts/<slug:slug>", views.PostDetailView.as_view(), name="post-detail"),
    path("posts/<slug:slug>/edit", views.PostUpdateView.as_view(), name="post-update"),
    path("posts/<slug:slug>/delete", views.PostDeleteView.as_view(), name="post-delete"),
    path("create/", views.PostCreateView.as_view(), name="create"),
    # Category create
    path("create/category/", views.CategoryCreateView.as_view(), name="create-category"),
    path("blog/api/v1/", include("blog.api.v1.urls")),
]