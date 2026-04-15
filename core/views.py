import os

from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from django.db.models import Q
from core.adapter import get_redirect_by_role
from customer.models import *
from pro1 import settings
from .models import *
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

from seller.models import *
import random
from django.core.mail import send_mail

User = get_user_model()

def login_view(request):
    show_google_login = True 

    if request.method == "POST":
        identifier = request.POST.get('login') 
        password = request.POST.get('password')

        user = authenticate(request, username=identifier, password=password)

        if user is not None:
            if user.is_superuser and "@" in identifier:
                messages.error(request, "Admins must login using their username, not email.")
                return redirect('login')

            login(request, user)
            return redirect(get_redirect_by_role(user))
        
        else:
            messages.error(request, 'Invalid credentials. Please try again.')

    return render(request, 'core_templates/loginpage.html', {
        'show_google_login': show_google_login
    })

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
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False,
        )

        return redirect('verify_otp')

    return render(request, 'core_templates/customer_register.html')

def seller_register(request):
    if request.method == "POST":
        data = request.POST
        files = request.FILES
        
        if data.get('password') != data.get('confirm_password'):
            messages.error(request, 'Passwords do not match.')
            return render(request, 'core_templates/seller_register.html')

        if User.objects.filter(email=data.get('email')).exists():
            messages.error(request, 'Email already exists.')
            return render(request, 'core_templates/seller_register.html')

        doc1 = files.get('document_1')
        doc2 = files.get('document_2')
        
        path1 = default_storage.save(f'tmp/docs/{doc1.name}', ContentFile(doc1.read())) if doc1 else None
        path2 = default_storage.save(f'tmp/docs/{doc2.name}', ContentFile(doc2.read())) if doc2 else None

        otp = str(random.randint(100000, 999999))
        request.session['register_data'] = {
            'first_name': data.get('first_name'),
            'last_name': data.get('last_name'),
            'email': data.get('email'),
            'phone': data.get('phone'),
            'password': data.get('password'),
            'role': 'SELLER',
            'shop_name': data.get('shop_name'),
            'account_number': data.get('account_number'),
            'ifsc_code': data.get('ifsc_code'),
            'branch_name': data.get('branch_name'),
            'doc1_path': path1,
            'doc2_path': path2,
        }
        request.session['otp'] = otp

        send_mail(
            'Verify your Email',
            f'Your OTP is {otp}',
            settings.EMAIL_HOST_USER,
            [data.get('email')],
        )

        return redirect('verify_otp')

    return render(request, 'core_templates/seller_register.html')

def verify_otp(request):
    if request.method == "POST":
        user_otp = request.POST.get('otp')
        session_otp = request.session.get('otp')
        data = request.session.get('register_data')

        if user_otp == session_otp:
            user = User.objects.create_user(
                username=data['email'],
                email=data['email'],
                password=data['password'],
                first_name=data['first_name'],
                last_name=data['last_name'],
                phone_number=data['phone'],
                role='SELLER',
                is_active=False
            )

            profile = SellerProfile.objects.create(
                user=user,
                shop_name=data['shop_name'],
                account_number=data['account_number'],
                ifsc_code=data['ifsc_code'],
                branch_name=data['branch_name']
            )

            if data['doc1_path']:
                profile.document_1.save(os.path.basename(data['doc1_path']), default_storage.open(data['doc1_path']))
            if data['doc2_path']:
                profile.document_2.save(os.path.basename(data['doc2_path']), default_storage.open(data['doc2_path']))

            messages.success(request, "Registration successful! Please wait for Admin approval.")
            return redirect('login')
        else:
            messages.error(request, "Invalid OTP.")
            
    return render(request, 'core_templates/verify_otp.html')


def logout_view(request):
    logout(request)
    return redirect('/')


def home_view(request):
    products = ProductVariant.objects.all()
    user_wishlist_ids = [] 

    if request.user.is_authenticated:
        user_wishlist_ids = WishlistItem.objects.filter(
            wishlist__user=request.user
        ).values_list('variant_id', flat=True)

    print(products)
    context = {
        'products': products,
        'user_wishlist_ids': list(user_wishlist_ids),
    }
    
    return render(request, 'core_templates/homepage.html', context)


def single_variant_view(request, id):
    """Render HTML for a single product variant."""
    variant = get_object_or_404(
        ProductVariant.objects.select_related('product__seller', 'product__subcategory')
                              .prefetch_related('product__images'),
        id=id
    )
    context = {
        'variant': variant,
    }
    return render(request, 'customer_templates/single_fetch.html', context)



def products(request):
    """View to display products page with New Arrivals section and All Products section"""
    from django.db.models import Count
    
    # Get filter/sort params
    category_id = request.GET.get('category_id')
    sort = request.GET.get('sort', 'newest')
    
    # Base queryset for all approved/active products
    base_qs = ProductVariant.objects.filter(
        product__approval_status='APPROVED',
        product__is_active=True
    ).select_related('product', 'product__subcategory__category').prefetch_related('images')
    
    # Apply category filter
    if category_id:
        base_qs = base_qs.filter(product__subcategory__category_id=category_id)
    
    # Apply sorting
    if sort == 'price_asc':
        base_qs = base_qs.order_by('selling_price')
    elif sort == 'price_desc':
        base_qs = base_qs.order_by('-selling_price')
    elif sort == 'name_asc':
        base_qs = base_qs.order_by('product__name')
    elif sort == 'name_desc':
        base_qs = base_qs.order_by('-product__name')
    elif sort == 'newest':
        base_qs = base_qs.order_by('-created_at')
    elif sort == 'oldest':
        base_qs = base_qs.order_by('created_at')
    
    all_products = base_qs
    
    # New arrivals (filtered/sorted same way, last 7 days)
    seven_days_ago = timezone.now() - timedelta(days=7)
    new_arrivals = all_products.filter(created_at__gte=seven_days_ago)
    
# Categories with product counts for sidebar - ALL active categories
    categories_qs = Category.objects.filter(is_active=True).annotate(
        product_count=Count(
            'subcategories__products',
            filter=Q(subcategories__products__approval_status='APPROVED', subcategories__products__is_active=True),
            distinct=True
        )
    )
    
    if category_id:
        categories_qs = categories_qs.filter(id=category_id)
    
    categories = categories_qs
    
    context = {
        'all_products': all_products,
        'new_arrivals': new_arrivals,
        'categories': categories,
        'category_filter': category_id,
        'sort_filter': sort,
        'total_products': all_products.count(),
    }
    
    if request.user.is_authenticated:
        context['data'] = request.user
    
    return render(request, 'core_templates/products.html', context)



