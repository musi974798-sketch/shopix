from django.urls import path
from seller import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('sellerhome/', views.seller_home_view, name='sellerhome'),
    path('addproduct/', views.addproduct, name = "addproduct"),
    path("product_detail/<int:pk>/", views.product_detail, name="product_detail"),
    path('sellerprofile/', views.sellerprofile, name = "sellerprofile"),
    path("profile/edit/", views.edit_seller_profile, name="edit_profile"),
    path("product/edit/<slug:slug>/", views.edit_product, name="edit_product"),
    path('productlist/', views.productlist, name = 'productlist'),
    path('order_view/', views.order_view, name = 'orderview'),
    path('logout/', views.seller_logout, name='logout'),
    path('logout-confirm/', views.logout_confirm, name='logout_confirm'),
]
