from django.shortcuts import render,redirect
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required(login_url='login')
def customer_home_view(request):
    return render(request, 'customer_templates/homepage.html')


@login_required(login_url='login')
def profile_view(request):
    user = request.user

    if request.method == "POST":
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')

        
        user.phone_number = request.POST.get('phone')
        image = request.FILES.get('profile_pic')

        if image:
            user.profile_image = image
        user.save()

        messages.success(request, "Profile updated successfully")

        return redirect('profile')  

    return render(request, 'customer_templates/profilepage.html', {'user': user})


def dashboard_view(request):
    return render(request,'customer_templates/coustomer_dashboard.html')