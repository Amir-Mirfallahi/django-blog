import pytest
from django.test import Client
from django.urls import reverse
from accounts.models import User

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

@pytest.mark.django_db
class TestLoginView:
    def test_login_view_get(self, client):
        url = reverse("accounts:login")
        response = client.get(url)
        assert response.status_code == 200
        assert "accounts/login.html" in [t.name for t in response.templates]

    def test_login_view_post_success(self, client, create_user):
        user = create_user(email="test@example.com")
        user.is_verified = True
        user.save()
        url = reverse("accounts:login")
        data = {"username": "test@example.com", "password": "password123"}
        response = client.post(url, data, follow=True)
        assert response.status_code == 200
        assert "_auth_user_id" in client.session

    def test_login_view_post_fail(self, client, create_user):
        create_user(email="test@example.com")
        url = reverse("accounts:login")
        data = {"username": "test@example.com", "password": "wrongpassword"}
        response = client.post(url, data)
        assert response.status_code == 200 # Stays on the login page
        assert "_auth_user_id" not in client.session

@pytest.mark.django_db
class TestRegisterView:
    def test_register_view_get(self, client):
        url = reverse("accounts:register")
        response = client.get(url)
        assert response.status_code == 200
        assert "accounts/register.html" in [t.name for t in response.templates]

    def test_register_view_post_success(self, client):
        url = reverse("accounts:register")
        data = {
            "email": "test@test.ts",
            "password": "password123",
            "password_confirm": "password123",
        }
        response = client.post(url, data, follow=True)
        assert response.status_code == 200

    def test_register_view_post_password_mismatch(self, client):
        url = reverse("accounts:register")
        data = {
            "email": "test@example.com",
            "password": "password123",
            "password_confirm": "password456",
        }
        response = client.post(url, data)
        assert response.status_code == 200 # Stays on the register page
        assert "form" in response.context
        assert not User.objects.filter(email="test@example.com").exists()
        assert "_auth_user_id" not in client.session

@pytest.mark.django_db
class TestLogoutView:
    def test_logout_view(self, client, create_user):
        user = create_user(email="test@example.com")
        client.login(email="test@example.com", password="password123")
        assert "_auth_user_id" in client.session
        url = reverse("accounts:logout")
        response = client.get(url)
        assert response.status_code == 200
        assert "accounts/logout.html" in [t.name for t in response.templates]
        assert "_auth_user_id" not in client.session
