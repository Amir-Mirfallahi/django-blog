from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm as BaseUserCreationForm, AuthenticationForm as BaseAuthenticationForm
from .models import Profile

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

class ProfileUpdateForm(forms.ModelForm):
    """
    Form for updating the user's profile information (first name, last name, bio, image).
    """
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'image', 'bio']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'mt-1 block w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-primary focus:border-primary sm:text-sm'}),
            'last_name': forms.TextInput(attrs={'class': 'mt-1 block w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-primary focus:border-primary sm:text-sm'}),
            'image': forms.FileInput(attrs={'class': 'mt-1 block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-primary hover:file:bg-blue-100'}),
            'bio': forms.Textarea(attrs={'class': 'mt-1 block w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-primary focus:border-primary sm:text-sm', 'rows': 4}),
        }


class EmailChangeForm(forms.ModelForm):
    """
    Form for changing the user's email address.
    """
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'mt-1 block w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-primary focus:border-primary sm:text-sm'}),
        help_text="Enter your new email address."
    )

    class Meta:
        model = User
        fields = ['email']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def clean_email(self):
        """
        Validate that the new email address is not already in use by another user.
        """
        new_email = self.cleaned_data.get('email')
        if User.objects.filter(email=new_email).exclude(pk=self.user.pk).exists():
            raise forms.ValidationError("This email address is already in use. Please choose another one.")
        return new_email