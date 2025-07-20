from django.views.generic import FormView
from .forms import UserCreationForm, UserLoginForm
from django.contrib.auth.views import LoginView as BaseLoginView
from django.views import View
from django.contrib.auth import login, logout
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib import messages

from .forms import ProfileUpdateForm, EmailChangeForm
from .models import Profile

class ProfileView(LoginRequiredMixin, TemplateView):
    """
    This view handles both displaying the profile and processing form submissions
    for profile updates and email changes.
    """
    template_name = 'accounts/profile.html'

    def get_context_data(self, **kwargs):
        """
        Populate the context with the necessary forms.
        """
        context = super().get_context_data(**kwargs)
        # If a form is not already in the context (from a failed POST), create a new one
        if 'profile_form' not in context:
            context['profile_form'] = ProfileUpdateForm(instance=self.request.user.profile)
        if 'email_form' not in context:
            context['email_form'] = EmailChangeForm(instance=self.request.user, user=self.request.user)
        return context

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests for the profile and email forms.
        """
        # Determine which form was submitted
        if 'update_profile' in request.POST:
            profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
            if profile_form.is_valid():
                profile_form.save()
                messages.success(request, 'Your profile has been updated successfully!')
                return redirect('accounts:profile')
            else:
                # Re-render the page with the invalid form and errors
                context = self.get_context_data(profile_form=profile_form)
                return self.render_to_response(context)

        elif 'change_email' in request.POST:
            email_form = EmailChangeForm(request.POST, instance=request.user, user=request.user)
            if email_form.is_valid():
                email_form.save()
                messages.success(request, 'Your email has been changed successfully!')
                return redirect('accounts:profile')
            else:
                # Re-render the page with the invalid form and errors
                context = self.get_context_data(email_form=email_form)
                return self.render_to_response(context)

        # If the POST request is not recognized, redirect back to the profile page
        return redirect('accounts:profile')


class CustomPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    """
    Custom password change view that specifies the success URL.
    We use Django's built-in view for maximum security.
    """
    template_name = 'accounts/profile.html' # We reuse the profile template
    success_url = reverse_lazy('accounts:password_change_done')

    def get_form_kwargs(self):
        """
        Pass the user to the form.
        """
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        """
        Add the password change form to the context and also include
        the other profile forms so the template can render them.
        """
        context = super().get_context_data(**kwargs)
        # The password change form is named 'form' by default by PasswordChangeView
        context['password_form'] = context.pop('form')
        
        # Add the other forms to the context so the tabs work correctly
        context['profile_form'] = ProfileUpdateForm(instance=self.request.user.profile)
        context['email_form'] = EmailChangeForm(instance=self.request.user, user=self.request.user)
        
        # Add a flag to indicate which tab should be active
        context['active_tab'] = 'password'
        return context


class PasswordChangeDoneView(LoginRequiredMixin, TemplateView):
    """
    Shows a success message after the user has changed their password.
    """
    template_name = 'accounts/password_change_done.html'



class LoginView(BaseLoginView):
    template_name = "accounts/login.html"
    form_class = UserLoginForm
    fields = "email", "password"
    redirect_authenticated_user = True

    def get_success_url(self):
        if self.request.GET.get("next"):
            return self.request.GET.get("next")
        return '/'


class RegisterView(FormView):
    template_name = "accounts/register.html"
    form_class = UserCreationForm
    redirect_authenticated_user = True

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterView, self).form_valid(form)

    def get_success_url(self):
        if self.request.GET.get("next"):
            return self.request.GET.get("next")
        return '/'


class LogoutView(View):
    """
    View for logging out a user.
    """

    def get(self, request):
        if request.user.is_authenticated:
            logout(request)
        return render(request, "accounts/logout.html")
