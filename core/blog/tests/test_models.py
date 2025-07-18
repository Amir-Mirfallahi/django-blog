import pytest
from django.utils import timezone
from blog.models import Post, Category
from accounts.models import User, Profile

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
class TestCategoryModel:
    def test_create_category(self):
        category = Category.objects.create(name="Test Category")
        assert category.name == "Test Category"
        assert str(category) == "Test Category"

@pytest.mark.django_db
class TestPostModel:
    def test_create_post(self, create_profile):
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
        assert post.author == create_profile
        assert post.title == "Test Post"
        assert post.slug == "test-post"
        assert post.content == "This is a test post."
        assert post.status is True
        assert post.category == category
        assert str(post) == "Test Post"

    def test_get_snippet(self, create_profile):
        post = Post.objects.create(
            author=create_profile,
            title="Test Post",
            slug="test-post",
            content="This is a test post.",
            status=True,
            published_date=timezone.now()
        )
        assert post.get_snippet() == "This "

    def test_get_absolute_api_url(self, create_profile):
        post = Post.objects.create(
            author=create_profile,
            title="Test Post",
            slug="test-post",
            content="This is a test post.",
            status=True,
            published_date=timezone.now()
        )
        expected_url = f"/blog/api/v1/post/{post.pk}/"
        assert post.get_absolute_api_url() == expected_url
