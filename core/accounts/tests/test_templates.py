import pytest
from django.test import Client
from django.urls import reverse
from django.template.loader import render_to_string


@pytest.fixture
def client():
    return Client()

@pytest.mark.django_db
class TestLoginTemplate:
    def test_login_template_renders_correctly(self, client):
        url = reverse("accounts:login")
        response = client.get(url)
        assert response.status_code == 200
        # Check for specific content in the rendered template
        assert "Login" in response.content.decode()
        assert "Don't have an account?" in response.content.decode()
        # Check that the form is rendered
        assert '<form' in response.content.decode()
        assert 'method="post"' in response.content.decode()
        assert 'action="/accounts/login/"' in response.content.decode()
        assert 'name="username"' or 'name="email"' in response.content.decode()
        assert 'name="password"' in response.content.decode()
        assert 'type="submit"' in response.content.decode()


@pytest.mark.django_db
class TestRegisterTemplate:
    def test_register_template_renders_correctly(self, client):
        url = reverse("accounts:register")
        response = client.get(url)
        assert response.status_code == 200
        # Check for specific content in the rendered template
        assert "Register in Blog" in response.content.decode()
        assert "Already registered?" in response.content.decode()
        # Check that the form is rendered
        assert '<form' in response.content.decode()
        assert 'method="post"' in response.content.decode()
        assert 'name="email"' in response.content.decode()
        assert 'name="password1"' in response.content.decode()
        assert 'name="password2"' in response.content.decode()
        assert 'type="submit"' in response.content.decode()


@pytest.mark.django_db
class TestLogoutTemplate:
    def test_logout_template_renders_correctly(self, client):
        url = reverse("accounts:logout")
        response = client.get(url)
        assert response.status_code == 200
        # Check for specific content in the rendered template
        assert "Logout from Blog" in response.content.decode()
        assert "You have successfully logged out from your account." in response.content.decode()
        assert "Go to Login" in response.content.decode()
        assert "Don't have an account?" in response.content.decode()
