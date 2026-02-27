from django.urls import path
from .import views
urlpatterns = [
    path('profile/',views.profile_view,name='profile'),
    path('shop/',views.customer_home_view,name='shop'),

]