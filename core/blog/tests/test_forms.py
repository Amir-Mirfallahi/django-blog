import pytest
from django.utils import timezone
from blog.forms import PostForm
from blog.models import Category, Post
from accounts.models import Profile, User

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
class TestPostForm:
    def test_post_form_valid(self):
        category = Category.objects.create(name="Test Category")
        form_data = {
            "title": "Test Post",
            "slug": "test-post",
            "read_time": 5,
            "content": "This is a test post.",
            "status": True,
            "category": category.id,
            "published_date": timezone.now().strftime("%Y-%m-%d")
        }
        form = PostForm(data=form_data)
        assert form.is_valid(), form.errors

    def test_post_form_missing_required_fields(self):
        form_data = {}
        form = PostForm(data=form_data)
        assert not form.is_valid()
        assert "title" in form.errors
        assert "slug" in form.errors
        assert "content" in form.errors
        assert "category" in form.errors
        assert "published_date" in form.errors

    def test_post_form_slug_not_unique(self, create_profile):
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
        form_data = {
            "title": "Test Post",
            "slug": "test-post",
            "read_time": 5,
            "content": "This is a test post.",
            "status": True,
            "category": category.id,
            "published_date": timezone.now().strftime("%Y-%m-%d")
        }
        form = PostForm(data=form_data)
        assert not form.is_valid()
        assert "slug" in form.errors
