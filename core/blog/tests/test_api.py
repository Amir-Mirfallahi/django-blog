import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from django.utils import timezone
from blog.models import Post, Category
from accounts.models import User, Profile

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def create_user(django_user_model):
    def make_user(**kwargs):
        kwargs.setdefault('password', 'password123')
        if 'email' not in kwargs:
            raise ValueError("Email is required to create a user")
        user = django_user_model.objects.create_user(**kwargs)
        user.is_verified = True
        user.save()
        return user
    return make_user

@pytest.fixture
def create_profile(create_user):
    user = create_user(email='test@example.com')
    profile = Profile.objects.get(user=user)
    return profile
    
@pytest.fixture
def authenticate_user(api_client, create_user):
    user = create_user(email='test2@example.com')
    api_client.force_authenticate(user=user)
    return user

@pytest.mark.django_db
class TestPostModelViewSet:
    def test_get_post_list(self, api_client):
        url = reverse("blog:api-v1:post-list")
        response = api_client.get(url)
        assert response.status_code == 200

    def test_create_post(self, api_client, authenticate_user, create_profile):
        category = Category.objects.create(name="Test Category")
        url = reverse("blog:api-v1:post-list")
        data = {
            "title": "New Post",
            "content": "Some content",
            "status": True,
            "category": category.id,
            "published_date": timezone.now()
        }
        response = api_client.post(url, data)
        assert response.status_code == 201
        assert Post.objects.filter(title="New Post").exists()

    def test_update_post(self, api_client, authenticate_user, create_profile):
        user_profile = Profile.objects.get(user=authenticate_user)
        post = Post.objects.create(
            author=user_profile,
            title="Test Post",
            slug="test-post",
            content="This is a test post.",
            status=True,
            published_date=timezone.now()
        )
        url = reverse("blog:api-v1:post-detail", kwargs={"pk": post.pk})
        data = {"title": "Updated Post"}
        response = api_client.patch(url, data)
        assert response.status_code == 200
        post.refresh_from_db()
        assert post.title == "Updated Post"

    def test_delete_post(self, api_client, authenticate_user, create_profile):
        user_profile = Profile.objects.get(user=authenticate_user)
        post = Post.objects.create(
            author=user_profile,
            title="Test Post",
            slug="test-post",
            content="This is a test post.",
            status=True,
            published_date=timezone.now()
        )
        url = reverse("blog:api-v1:post-detail", kwargs={"pk": post.pk})
        response = api_client.delete(url)
        assert response.status_code == 204
        assert not Post.objects.filter(pk=post.pk).exists()

@pytest.mark.django_db
class TestCategoryModelViewSet:
    def test_get_category_list(self, api_client, authenticate_user):
        url = reverse("blog:api-v1:category-list")
        response = api_client.get(url)
        assert response.status_code == 200

    def test_create_category(self, api_client, authenticate_user):
        url = reverse("blog:api-v1:category-list")
        data = {"name": "New Category"}
        response = api_client.post(url, data)
        assert response.status_code == 201
        assert Category.objects.filter(name="New Category").exists()

    def test_unauthenticated_access(self, api_client):
        url = reverse("blog:api-v1:category-list")
        response = api_client.get(url)
        assert response.status_code == 401
        
        url = reverse("blog:api-v1:category-list")
        data = {"name": "New Category"}
        response = api_client.post(url, data)
        assert response.status_code == 401
