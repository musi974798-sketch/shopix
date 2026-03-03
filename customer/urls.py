from django.urls import path
from .import views
urlpatterns = [
    path('profile/',views.profile_view,name='profile'),
    path('coustomer_home/',views.customer_home_view,name='customerhome'),
    path('dashboard/',views.dashboard_view,name='dashboard'),
    path('shop/',views.customer_home_view,name='shop'),


]