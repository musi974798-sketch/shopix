from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages

from seller.models import Product, SellerProfile
import random
from django.core.mail import send_mail

User = get_user_model()

def login_view(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)

            if user.role == 'SELLER':
                return redirect('sellerhome')

            elif user.role == 'CUSTOMER':
                return redirect('home')

            elif user.role == 'ADMIN':
                return redirect('admin_dashboard')

        else:
            messages.error(request, 'Invalid email or password. Please try again.')

    return render(request, 'core_templates/loginpage.html')


def customer_register(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'core_templates/customer_register.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists.')
            return render(request, 'core_templates/customer_register.html')

        if User.objects.filter(phone_number=phone).exists():
            messages.error(request, 'Phone number already registered.')
            return render(request, 'core_templates/customer_register.html')

        otp = str(random.randint(100000, 999999))

        request.session['register_data'] = {
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'phone': phone,
            'password': password,
            'role': 'CUSTOMER'
        }
        request.session['otp'] = otp

        send_mail(
            'Your OTP Code',
            f'Your OTP is {otp}',
            'your_email@gmail.com',
            [email],
            fail_silently=False,
        )

        return redirect('verify_otp')

    return render(request, 'core_templates/customer_register.html')

def seller_register(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'core_templates/seller_register.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists.')
            return render(request, 'core_templates/seller_register.html')

        if User.objects.filter(phone_number=phone).exists():
            messages.error(request, 'Phone number already registered.')
            return render(request, 'core_templates/seller_register.html')

        otp = str(random.randint(100000, 999999))

        request.session['register_data'] = {
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'phone': phone,
            'password': password,
            'role': 'SELLER'
        }

        request.session['otp'] = otp

        send_mail(
            'Your OTP Code',
            f'Your OTP is {otp}',
            'your_email@gmail.com',
            [email],
            fail_silently=False,
        )

        messages.success(request, 'OTP sent to your email. Please verify.')
        return redirect('verify_otp')

    return render(request, 'core_templates/seller_register.html')

def verify_otp(request):
    if request.method == "POST":
        entered_otp = request.POST.get('otp')
        session_otp = request.session.get('otp')
        data = request.session.get('register_data')

        if not session_otp or not data:
            messages.error(request, "Session expired. Please register again.")
            return redirect('customer_register')

        if entered_otp == session_otp:

            user = User.objects.create_user(
                username=data['email'],
                email=data['email'],
                password=data['password'],
                first_name=data['first_name'],
                last_name=data['last_name'],
                phone_number=data['phone'],
                role=data['role']
            )

            if data['role'] == 'SELLER':
                SellerProfile.objects.create(user=user)

            request.session.flush()

            messages.success(request, "Account created successfully!")
            return redirect('login')
        else:
            messages.error(request, "Invalid OTP")

    return render(request, 'core_templates/verify_otp.html')


def logout_view(request):
    logout(request)
    return redirect('/')


def home_view(request):
    products = Product.objects.all()
    

    user=request.user
    if user.is_authenticated:
        return render(request, 'core_templates/homepage.html', { 'products' : products })
    return render(request, 'core_templates/homepage.html', { 'products' : products })
