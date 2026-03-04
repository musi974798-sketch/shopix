from django.shortcuts import render,redirect,get_object_or_404
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required(login_url='login')
def customer_home_view(request):
    products = Product.objects.all()
    return render(request, 'core_templates/homepage.html', { 'products' : products })


@login_required(login_url='login')
def profile_view(request):
    user = request.user
    if request.method == "POST":
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.phone_number = request.POST.get('phone')
        image = request.FILES.get('profile_image')
        if image:
            user.profile_image = image
        user.save()

        messages.success(request, "Profile updated successfully")
        return redirect('profile')  

    return render(request, 'customer_templates/profilepage.html', {'user': user})


def dashboard_view(request):
    products = Product.objects.all()
    return render(request, 'customer_templates/coustomer_dashboard.html', {
        'products': products
    })
    

def cart_view(request):
    return render(request,'customer_templates/cart.html')

def add_cart(request,variant_id):
    variant=get_object_or_404(ProductVariant,id=variant_id)
    cart, create=cart.objects.get_or_create(user=request.user, completed= False)
    
