from django.urls import path
from admin_app import views

urlpatterns = [
    path('admindashboard/', views.admindashboard, name='admindashboard'),
    path('customerlisting/', views.customerlisting, name='customerlisting'),
    path('productlisting/', views.productlisting, name='productlisting'),
    path('sellerlisting/', views.sellerlisting, name='sellerlisting'),
]