from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages

User = get_user_model()

def login_view(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user_obj = User.objects.get(email=email)
            email = user_obj.email
        except User.DoesNotExist:
            pass
            
        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            
            login(request, user)
            return redirect('coustomer_home')
        else:
            messages.error(request, 'Invalid email or password. Please try again.')
            
    return render(request, 'core_templates/loginpage.html')


def register_view(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, 'Passwords do not match. Please try again.')
            return render(request, 'core_templates/registerpage.html')
        if User.objects.filter(email=email).exists():
            messages.error(request, 'An account with this email already exists.')
            return render(request, 'core_templates/registerpage.html')

        if User.objects.filter(phone_number=phone).exists():
            messages.error(request, 'This mobile number is already registered.')
            return render(request, 'core_templates/registerpage.html')
        try:
            user = User.objects.create_user(
                username=email,
                email=email, 
                password=password, 
                first_name=first_name, 
                last_name=last_name,
                phone_number=phone
            )
            user.save()
            messages.success(request, 'Registration successful! You can now login.')
            return redirect('login')
            
        except Exception as e:
            messages.error(request, f'Something went wrong: {e}')
            return render(request, 'core_templates/registerpage.html')
            
    return render(request, 'core_templates/registerpage.html')

def logout_view(request):
    logout(request)
    return redirect('/')


def home_view(request):
    user=request.user
    if user.is_authenticated:
        return render(request, 'core_templates/homepage.html')
    return render(request, 'core_templates/homepage.html')
