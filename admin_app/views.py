from django.shortcuts import render

from core.models import User

def admindashboard(request):
    return render(request, 'admin_templates/admindashboard.html')

def customerlisting(request):
    customers = User.objects.filter(role='CUSTOMER')
    return render(request, 'admin_templates/customerlisting.html', {
        'customers': customers
    })

def sellerlisting(request):
    sellers = User.objects.filter(role='SELLER')
    return render(request, 'admin_templates/sellerlisting.html', {
        'sellers': sellers
    })

def productlisting(request):
    return render(request, 'admin_templates/productlisting.html')

