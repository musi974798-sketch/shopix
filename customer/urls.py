from django.urls import path
from . import views

urlpatterns = [
    path('customer_profile/', views.profile_view, name='profile'),
    
    path('cart/', views.cart_view, name='cart'),
    
    # Cart Actions
    path('add_to_cart/<int:variant_id>/', views.add_cart, name='add_to_cart'),
    path('update_quantity/<uuid:item_id>/<str:action>/', views.cart_update_quantity, name='update_quantity'),
    path('remove_item/<uuid:item_id>/', views.cart_remove_item, name='remove_item'),

    # Products & Reviews
    path('product/<int:id>/', views.variant_page, name='variant_page'), # Fixed to <int:id>
    path('add_review/<int:product_id>/', views.add_review, name='add_review'), # NEW: Review URL

    # Wishlist
    path('wishlist/', views.wishlist_view, name='wishlist_view'),
    path('wishlist/add/<int:variant_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/remove/<int:wishlist_item_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
    path('wishlist/clear/', views.clear_wishlist, name='clear_wishlist'),

    # Addresses
    path('addresses/', views.customer_address, name='customer_address'),
    path('add_addresses/', views.customer_address_add, name='customer_add_address'),
    path('address_update/<uuid:address_id>/', views.customer_address_update, name='customer_update_address'),
    path('address_delete/<uuid:address_id>/', views.customer_address_delete, name='customer_delete_address'),
    
    # --- Order & Checkout URLs ---
    
    # Single product checkout
    path('order/<int:id>/', views.order, name='order'),
    
    # Cart checkout
    path('checkout/<uuid:cart_id>/', views.checkout, name='checkout'),
    
    # Set delivery address during checkout
    path('order/select_address/<uuid:address_id>/', views.order_select_address, name='order_select_address'),
    
    # Process the order (POST request)
    path('place_order/', views.place_order, name='place_order'),
    
    # Payment success callback
    path('payment-success/', views.payment_success, name='payment_success'),
    
    # Success/Confirmation page
    path('order_confirmation/<uuid:order_id>/', views.order_confirmation, name='order_confirmation'),
    
    path('order_history/', views.order_history, name='order_history'), # Fixed missing trailing slash

    path("search/", views.search, name="search"),
]