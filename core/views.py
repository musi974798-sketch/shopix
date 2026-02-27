from django.shortcuts import render,redirect
from .models import *
from django.contrib.auth import authenticate,login,logout
# Create your views here.

def login_view(request):
    if request.method=="POST":
        username=request.POST.get('usernameoremail')
        password=request.POST.get('password')
        try:
            user_obj = User.objects.get(email=username)
            username = user_obj.username
        except User.DoesNotExist:
            username = username
        user=authenticate(username=username,password=password )
        if user is not None:
            login(request,user)
            return redirect('home')
    return render(request,'core_templates/loginpage.html')


def buyer_register(request):
    if request.method=="POST":
        first_name=request.POST.get('first_name')
        last_name=request.POST.get('last_name')
        username=request.POST.get('username')
        email=request.POST.get('email')
        password=request.POST.get('password')
        confirm_password=request.POST.get('confirm_password')
        if password != confirm_password:
            return render(request,'core_templates/buyer_register.html',{'error':'Passwords do not match'})
        user=User.objects.create_user(username=username,email=email,password=password,first_name=first_name,last_name=last_name)
        user.save()
        return redirect('login')
    return render(request,'core_templates/buyer_register.html')

def seller_register(request):
    if request.method=="POST":
        first_name=request.POST.get('first_name')
        last_name=request.POST.get('last_name')
        username=request.POST.get('username')
        email=request.POST.get('email')
        password=request.POST.get('password')
        confirm_password=request.POST.get('confirm_password')
        if password != confirm_password:
            return render(request,'core_templates/seller_register.html',{'error':'Passwords do not match'})
        user=User.objects.create_user(username=username,email=email,password=password,first_name=first_name,last_name=last_name)
        user.save()
        return redirect('login')
    return render(request,'core_templates/seller_register.html')

def logout_view(request):
    logout(request)
    return redirect('/')


def home_view(request):
    return render(request,'core_templates/homepage.html')
