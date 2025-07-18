from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm as BaseUserCreationForm, AuthenticationForm as BaseAuthenticationForm

User = get_user_model()

class UserCreationForm(BaseUserCreationForm):
    class Meta:
        model = User
        fields = ["email", "password1", "password2"]
        widgets = {
            "email": forms.EmailInput(attrs={"placeholder": "Enter your email."}),
            "password1": forms.PasswordInput(attrs={"placeholder": "Enter your password."}),
            "password2": forms.PasswordInput(attrs={"placeholder": "Confirm your passwrd."}),
        }
        labels = {
            "email": "Email",
            "password1": "Password",
            "password2": "Confirm Password",
        }
    email = forms.EmailField(error_messages={"required": "Email is required.", "invalid": "Email is invalid.", "unique": "This email has already been used.", "max_length": "Email must be less that 254 characters."})
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput, error_messages={"required": "Password is required.", "min_length": "Password must be at least 8 characters."})
    password2 = forms.CharField(label="Repeat Password", widget=forms.PasswordInput, error_messages={"required": "Password repeat is required.", "min_length": "Password repeat must be at least 8 characters."})

    def form_valid(self, form):
        user = User.objects.create_user(
            email=form.cleaned_data["email"],
            password=form.cleaned_data["password1"],
        )
        return user


class UserLoginForm(BaseAuthenticationForm):
    class Meta:
        model = User
        fields = ["email", "password"]
        widgets = {
            "email": forms.EmailInput(attrs={"placeholder": "Enter your email."}),
            "password": forms.PasswordInput(attrs={"placeholder": "Enter your password"}),
        }
        labels = {
            "email": "Email",
            "password": "Password",
        }

