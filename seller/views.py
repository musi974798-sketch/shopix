from django.shortcuts import get_object_or_404, render,redirect
from seller.forms import ProductForm, ProductImageFormSet
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from core import urls

@login_required(login_url='login')
def seller_home_view(request):
    
    seller_profile = get_object_or_404(SellerProfile, user=request.user)

    products = Product.objects.filter(seller=seller_profile)
    print(seller_profile)

    return render(request, 'seller_templates/homepage.html',{
        'products': products,
        'seller_profile':seller_profile,
    })

@login_required(login_url='login')
def addproduct(request):

    seller = request.user.seller_profile
    product = Product(seller=seller)

    if request.method == "POST":

        form = ProductForm(request.POST, instance=product)
        formset = ProductImageFormSet(request.POST, request.FILES, instance=product)

        if form.is_valid() and formset.is_valid():

            product = form.save()
            formset.save()

            return redirect("sellerhome")

    else:
        form = ProductForm(instance=product)
        formset = ProductImageFormSet(instance=product)

    return render(request, "seller_templates/add_product.html", {
        "form": form,
        "formset": formset
    })
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, "seller_templates/product_detail.html", {"product": product})

@login_required(login_url='login')
def sellerprofile(request):
    seller_profile = get_object_or_404(SellerProfile, user=request.user)
    products_count = Product.objects.filter(seller=seller_profile).count()

    return render(request, "seller_templates/seller_profile.html", {
        "seller": seller_profile,
        "products_count": products_count,
    })

@login_required(login_url='login')
def logout(request):
    return redirect('login')