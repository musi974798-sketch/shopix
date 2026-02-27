from django.urls import path
from .import views
urlpatterns = [

    path('login/',views.login_view,name='login'),
    path('buyerregister/',views.buyer_register,name='buyerregister'),
    path('sellerregister/',views.seller_register,name='sellerregister'),
    path('logout/',views.logout_view,name='logout'),
    path('',views.home_view,name='home'),
]