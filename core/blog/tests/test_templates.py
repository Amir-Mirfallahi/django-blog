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
class TestHomeTemplate:
    def test_home_template_renders_correctly(self, client):
        url = reverse("blog:home")
        response = client.get(url)
        assert response.status_code == 200
        assert "Welcome to Blog" in response.content.decode()
        assert "Search articles..." in response.content.decode()

    def test_home_template_with_posts(self, client, create_profile):
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
        assert "Test Post" in response.content.decode()
        assert "Test Category" in response.content.decode()

@pytest.mark.django_db
class TestPostDetailTemplate:
    def test_post-detail_template_renders_correctly(self, client, create_profile):
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
        assert post.title in response.content.decode()
        assert post.content in response.content.decode()
        assert post.author.first_name in response.content.decode()
        assert post.category.name in response.content.decode()
        assert "Leave a Comment" in response.content.decode()

@pytest.mark.django_db
class TestPostCreateTemplate:
    def test_post_create_template_renders_correctly(self, client, create_user):
        user = create_user(email='test@example.com')
        client.login(email='test@example.com', password='password123')
        url = reverse("blog:create")
        response = client.get(url)
        assert response.status_code == 200
        assert "Create new post" in response.content.decode()
        assert '<form method="post">' in response.content.decode()
        assert "Post it" in response.content.decode()
