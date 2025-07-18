import pytest
from django.utils import timezone
from blog.models import Post, Category
from accounts.models import User, Profile
from comment.models import Comment
from comment.api.v1.serializers import CommentSerializer

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

@pytest.fixture
def create_post(create_profile):
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
    return post

@pytest.mark.django_db
class TestCommentSerializer:
    def test_comment_serializer_valid(self, create_post):
        data = {
            "post": create_post.pk,
            "name": "Test User",
            "email": "test@example.com",
            "message": "This is a test comment."
        }
        serializer = CommentSerializer(data=data)
        assert serializer.is_valid(), serializer.errors

    def test_comment_serializer_empty_message(self, create_post):
        data = {
            "post": create_post.pk,
            "name": "Test User",
            "email": "test@example.com",
            "message": " "
        }
        serializer = CommentSerializer(data=data)
        assert not serializer.is_valid()
        assert "message" in serializer.errors

    def test_comment_serializer_invalid_email(self, create_post):
        data = {
            "post": create_post.pk,
            "name": "Test User",
            "email": "invalid-email",
            "message": "This is a test comment."
        }
        serializer = CommentSerializer(data=data)
        assert not serializer.is_valid()
        assert "email" in serializer.errors

    def test_comment_serializer_with_reply(self, create_post):
        parent_comment = Comment.objects.create(
            post=create_post,
            name="Parent User",
            email="parent@example.com",
            message="This is a parent comment."
        )
        data = {
            "post": create_post.pk,
            "name": "Reply User",
            "email": "reply@example.com",
            "message": "This is a reply.",
            "reply_to": parent_comment.pk
        }
        serializer = CommentSerializer(data=data)
        assert serializer.is_valid(), serializer.errors
        comment = serializer.save()
        assert comment.reply_to == parent_comment
