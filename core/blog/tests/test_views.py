import pytest
from django.test import Client
from django.urls import reverse
from django.utils import timezone
from blog.models import Post, Category
from accounts.models import User, Profile

@pytest.fixture
def client():
    return Client()

@pytest.fixture
def create_user(django_user_model):
    def make_user(**kwargs):
        kwargs.setdefault('password', 'password123')
        if 'email' not in kwargs:
            raise ValueError("Email is required to create a user")
        return django_user_model.objects.create_user(**kwargs)
    return make_user

@pytest.fixture
def create_profile(create_user):
    user = create_user(email='test@example.com')
    profile = Profile.objects.get(user=user)
    return profile

@pytest.mark.django_db
class TestHomeView:
    def test_home_view_get(self, client):
        url = reverse("blog:home")
        response = client.get(url)
        assert response.status_code == 200
        assert "blog/home.html" in [t.name for t in response.templates]

    def test_home_view_with_posts(self, client, create_profile):
        category = Category.objects.create(name="Test Category")
        Post.objects.create(
            author=create_profile,
            title="Test Post",
            slug="test-post",
            content="This is a test post.",
            status=True,
            category=category,
            published_date=timezone.now()
        )
        url = reverse("blog:home")
        response = client.get(url)
        assert response.status_code == 200
        assert "object_list" in response.context
        assert len(response.context["object_list"]) == 1

@pytest.mark.django_db
class TestPostDetailView:
    def test_post-detail_view_get(self, client, create_profile):
        category = Category.objects.create(name="Test Category")
        post = Post.objects.create(
            author=create_profile,
            title="Test Post",
            slug="test-post",
            content="This is a test post.",
            status=True,
            category=category,
            published_date=timezone.now()
        )
        url = reverse("blog:post-detail", kwargs={"slug": post.slug})
        response = client.get(url)
        assert response.status_code == 200
        assert "blog/post-detail.html" in [t.name for t in response.templates]
        assert "post" in response.context
        assert response.context["post"] == post

@pytest.mark.django_db
class TestPostCreateView:
    def test_post_create_view_get_unauthenticated(self, client):
        url = reverse("blog:create")
        response = client.get(url)
        assert response.status_code == 302
        assert "/accounts/login/" in response.url

    def test_post_create_view_get_authenticated(self, client, create_user):
        user = create_user(email="test@example.com")
        client.login(email="test@example.com", password="password123")
        url = reverse("blog:create")
        response = client.get(url)
        assert response.status_code == 200
        assert "blog/post-create.html" in [t.name for t in response.templates]

    def test_post_create_view_post(self, client, create_user, create_profile):
        user = create_user(email="test5@example.com")
        client.login(email="test5@example.com", password="password123")
        category = Category.objects.create(name="Test Category")
        url = reverse("blog:create")
        data = {
            "title": "New Post",
            "slug": "new-post",
            "content": "Some content",
            "status": True,
            "category": category.id,
            "published_date": timezone.now(),
            "author": user.profile
        }
        response = client.post(url, data, follow=True)
        assert response.status_code == 200
