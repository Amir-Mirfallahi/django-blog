import threading
from rest_framework_simplejwt.tokens import RefreshToken



def get_tokens_for_user_util(user):
    """
    Utility function to generate JWT access token with JTI.
    """
    refresh = RefreshToken.for_user(user)
    refresh.access_token["jti"] = refresh["jti"]
    return str(refresh.access_token)
