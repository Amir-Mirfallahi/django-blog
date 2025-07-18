import pytest
from django.db import IntegrityError
from accounts.models.users import User, UsedToken
from accounts.models.profiles import Profile

@pytest.mark.django_db
class TestUserModel:
    def test_create_user(self):
        user = User.objects.create_user(email="test@example.com", password="password123")
        assert user.email == "test@example.com"
        assert user.is_active
        assert not user.is_staff
        assert not user.is_superuser
        assert not user.is_verified
        assert user.check_password("password123")

    def test_create_user_no_email(self):
        with pytest.raises(ValueError):
            User.objects.create_user(email="", password="password123")

    def test_create_superuser(self):
        superuser = User.objects.create_superuser(email="super@example.com", password="password123")
        assert superuser.email == "super@example.com"
        assert superuser.is_active
        assert superuser.is_staff
        assert superuser.is_superuser
        assert superuser.is_verified
        assert superuser.check_password("password123")

    def test_create_superuser_not_staff(self):
        with pytest.raises(ValueError):
            User.objects.create_superuser(email="super@example.com", password="password123", is_staff=False)

    def test_create_superuser_not_superuser(self):
        with pytest.raises(ValueError):
            User.objects.create_superuser(email="super@example.com", password="password123", is_superuser=False)
    
    def test_create_superuser_not_verified(self):
        with pytest.raises(ValueError):
            User.objects.create_superuser(email="super@example.com", password="password123", is_verified=False)

    def test_user_str(self):
        user = User.objects.create_user(email="test@example.com", password="password123")
        assert str(user) == "test@example.com"

    def test_user_email_unique(self):
        User.objects.create_user(email="test@example.com", password="password123")
        with pytest.raises(IntegrityError):
            User.objects.create_user(email="test@example.com", password="password456")


@pytest.mark.django_db
class TestUsedTokenModel:
    def test_create_used_token(self):
        user = User.objects.create_user(email="test@example.com", password="password123")
        used_token = UsedToken.objects.create(user=user, token_jti="test_jti")
        assert used_token.user == user
        assert used_token.token_jti == "test_jti"

    def test_used_token_str(self):
        user = User.objects.create_user(email="test@example.com", password="password123")
        used_token = UsedToken.objects.create(user=user, token_jti="test_jti")
        assert str(used_token) == f"Used token test_jti for {user.email}"

    def test_used_token_jti_unique(self):
        user = User.objects.create_user(email="test@example.com", password="password123")
        UsedToken.objects.create(user=user, token_jti="test_jti")
        with pytest.raises(IntegrityError):
            UsedToken.objects.create(user=user, token_jti="test_jti")


@pytest.mark.django_db
class TestProfileModel:
    def test_profile_creation_on_user_creation(self):
        user = User.objects.create_user(email="test@example.com", password="password123")
        assert Profile.objects.filter(user=user).exists()

    def test_profile_str(self):
        user = User.objects.create_user(email="test@example.com", password="password123")
        profile = Profile.objects.get(user=user)
        assert str(profile) == user.email

    def test_profile_fields(self):
        user = User.objects.create_user(email="test@example.com", password="password123")
        profile = Profile.objects.get(user=user)
        profile.first_name = "Test"
        profile.last_name = "User"
        profile.bio = "This is a test bio."
        profile.save()

        updated_profile = Profile.objects.get(user=user)
        assert updated_profile.first_name == "Test"
        assert updated_profile.last_name == "User"
        assert updated_profile.bio == "This is a test bio."
