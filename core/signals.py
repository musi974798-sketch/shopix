from allauth.socialaccount.signals import pre_social_login
from django.dispatch import receiver
from django.contrib import messages
from django.shortcuts import redirect

@receiver(pre_social_login)
def block_admin_google_login(request, sociallogin, **kwargs):
    user = sociallogin.user

    # Check if user already exists in DB
    if sociallogin.is_existing:
        if hasattr(user, 'role') and user.role == 'ADMIN':
            messages.error(request, "Admin cannot login using Google.")
            return redirect('login')  # your login url name