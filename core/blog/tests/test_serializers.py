import pytest
from django.utils import timezone
from django.test import RequestFactory
from rest_framework.request import Request
from blog.api.v1.serializers import PostSerializer, CategorySerializer
from blog.models import Post, Category
from accounts.models import User, Profile

@pytest.fixture
def create_user(django_user_model):
    def make_user(**kwargs):
        kwargs.setdefault('password', 'ValidPassword123!')
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
def request_factory():
    return RequestFactory()

@pytest.mark.django_db
class TestCategorySerializer:
    def test_category_serializer(self):
        category = Category.objects.create(name="Test Category")
        serializer = CategorySerializer(instance=category)
        expected_data = {
            "id": category.id,
            "name": "Test Category"
        }
        assert serializer.data == expected_data

@pytest.mark.django_db
class TestPostSerializer:
    def test_post_serializer_list_view(self, create_profile, request_factory):
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
        request = request_factory.get(f'/blog/api/v1/post/')
        # DRF's Request object is needed for the serializer context
        drf_request = Request(request)
        drf_request.parser_context = {'kwargs': {}}
        serializer = PostSerializer(instance=post, context={'request': drf_request})
        
        assert "content" not in serializer.data
        assert "snippet" in serializer.data
        assert "relative_url" in serializer.data
        assert "absolute_url" in serializer.data

    def test_post_serializer_detail_view(self, create_profile, request_factory):
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
        request = request_factory.get(f'/blog/api/v1/post/{post.pk}/')
        # DRF's Request object is needed for the serializer context
        drf_request = Request(request)
        # Mocking the kwargs that DRF would set
        drf_request.parser_context = {'kwargs': {'pk': post.pk}}
        serializer = PostSerializer(instance=post, context={'request': drf_request})

        assert "content" in serializer.data
        assert "snippet" not in serializer.data
        assert "relative_url" not in serializer.data
        assert "absolute_url" not in serializer.data

    def test_post_serializer_create(self, create_profile, request_factory, create_user):
        category = Category.objects.create(name="Test Category")
        user = create_user(email='test2@example.com')
        request = request_factory.post('/blog/api/v1/post/')
        request.user = user
        
        data = {
            "title": "New Post",
            "content": "Some content",
            "status": True,
            "category": category.id,
            "published_date": timezone.now()
        }
        
        # Manually create a DRF request object and set the user
        drf_request = Request(request)
        drf_request.user = user

        serializer = PostSerializer(data=data, context={'request': drf_request})
        assert serializer.is_valid(), serializer.errors
        post = serializer.save()
        
        assert post.title == "New Post"
        assert post.author == Profile.objects.get(user=user)
