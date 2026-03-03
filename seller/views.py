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

    seller_profile = get_object_or_404(SellerProfile, user=request.user)

    if request.method == "POST":
        form = ProductForm(request.POST)
        formset = ProductImageFormSet(request.POST, request.FILES)

        if form.is_valid() and formset.is_valid():
            product = form.save(commit=False)
            product.seller = seller_profile

            if "draft" in request.POST:
                product.is_draft = True

            product.save()

            formset.instance = product
            formset.save()

            messages.success(request, "Product added successfully!")
            return redirect("sellerhome")

    else:
        form = ProductForm()
        formset = ProductImageFormSet()

    return render(request, "seller_templates/add_product.html", {
        "form": form,
        "formset": formset,
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