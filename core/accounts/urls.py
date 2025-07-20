from django.urls import path, include
from . import views

app_name = "accounts"
urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('profile/', views.ProfileView.as_view(), name="profile"),
    path('password/change/', views.CustomPasswordChangeView.as_view(), name='password_change'),
    path('password/change/done/', views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path("api/v1/", include("accounts.api.v1.urls")),
    path('api/v1/',include('accounts.api.v1.urls')),
]