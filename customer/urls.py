from django.urls import path
from .import views
urlpatterns = [
    path('profile/',views.profile_view,name='profile'),
    path('dashboard/',views.dashboard_view,name='dashboard'),
    path('cart/',views.cart_view,name='cartpage')


]