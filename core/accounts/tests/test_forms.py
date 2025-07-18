import pytest
from accounts.forms import UserCreationForm, UserLoginForm
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.mark.django_db
class TestUserCreationForm:
    def test_user_creation_form_valid(self):
        form_data = {
            "email": "test@example.com",
            "password1": "ValidPassword123!",
            "password2": "ValidPassword123!",
        }
        form = UserCreationForm(data=form_data)
        assert form.is_valid(), form.errors

    def test_user_creation_form_password_mismatch(self):
        form_data = {
            "email": "test@example.com",
            "password1": "ValidPassword123!",
            "password2": "password456",
        }
        form = UserCreationForm(data=form_data)
        assert not form.is_valid()
        assert "password2" in form.errors

    def test_user_creation_form_existing_email(self):
        User.objects.create_user(email="test@example.com", password="ValidPassword123!")
        form_data = {
            "email": "test@example.com",
            "password1": "ValidPassword123!",
            "password2": "ValidPassword123!",
        }
        form = UserCreationForm(data=form_data)
        assert not form.is_valid()
        assert "email" in form.errors


@pytest.mark.django_db
class TestUserLoginForm:
    def test_user_login_form_valid(self):
        User.objects.create_user(email="test@example.com", password="ValidPassword123!")
        form_data = {"username": "test@example.com", "password": "ValidPassword123!"}
        form = UserLoginForm(data=form_data)
        assert form.is_valid()

    def test_user_login_form_invalid_credentials(self):
        form_data = {"username": "test@example.com", "password": "wrongpassword"}
        form = UserLoginForm(data=form_data)
        assert not form.is_valid()
        assert "__all__" in form.errors
