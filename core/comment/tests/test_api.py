import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from django.utils import timezone
from blog.models import Post, Category
from accounts.models import User, Profile
from unittest.mock import patch

@pytest.fixture
def api_client():
    return APIClient()

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
class TestCreateCommentApiView:
    @patch('comment.api.v1.views.create_comment_task.apply_async')
    def test_create_comment_api_view(self, mock_apply_async, api_client, create_post):
        mock_apply_async.return_value.id = 'test_task_id'
        url = reverse("comment:api-v1:create")
        data = {
            "post": create_post.id,
            "name": "Test User",
            "email": "test@example.com",
            "message": "This is a test comment."
        }
        response = api_client.post(url, data)
        assert response.status_code == 202
        assert response.data["status"] == "accepted"
        assert response.data["task_id"] == "test_task_id"
        mock_apply_async.assert_called_once()

    def test_create_comment_api_view_invalid_data(self, api_client, create_post):
        url = reverse("comment:api-v1:create")
        data = {
            "post": create_post.id,
            "name": "Test User",
            "email": "invalid-email",
            "message": ""
        }
        response = api_client.post(url, data)
        assert response.status_code == 400
        assert "email" in response.data
        assert "message" in response.data
