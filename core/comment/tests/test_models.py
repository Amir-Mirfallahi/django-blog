import pytest
from django.utils import timezone
from blog.models import Post, Category
from accounts.models import User, Profile
from comment.models import Comment

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
class TestCommentModel:
    def test_create_comment(self, create_post):
        comment = Comment.objects.create(
            post=create_post,
            name="Test User",
            email="test@example.com",
            message="This is a test comment."
        )
        assert comment.post == create_post
        assert comment.name == "Test User"
        assert comment.email == "test@example.com"
        assert comment.message == "This is a test comment."
        assert comment.is_active is True
        assert str(comment) == "Test User:test@example.com | This is a test comment."

    def test_create_reply(self, create_post):
        parent_comment = Comment.objects.create(
            post=create_post,
            name="Parent User",
            email="parent@example.com",
            message="This is a parent comment."
        )
        reply = Comment.objects.create(
            post=create_post,
            name="Reply User",
            email="reply@example.com",
            message="This is a reply.",
            reply_to=parent_comment
        )
        assert reply.reply_to == parent_comment
        assert parent_comment.replies.count() == 1
        assert parent_comment.replies.first() == reply
