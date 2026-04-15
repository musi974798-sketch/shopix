from django.http import HttpResponse
from django.shortcuts import redirect
from functools import wraps

def seller_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponse("Unauthorized", status=401)
        if request.user.role != 'SELLER':
            return HttpResponse("Forbidden", status=403)
        if not hasattr(request.user, 'seller_profile') or request.user.seller_profile.status != 'APPROVED':
            return HttpResponse("Seller not approved", status=403)

        return view_func(request, *args, **kwargs)
    return _wrapped_view

def customer_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            # Redirecting to login is usually better for customers than a raw 401 error
            return redirect('login') 
        
        if request.user.role != 'CUSTOMER':
            return HttpResponse("Forbidden: Customer access only", status=403)

        return view_func(request, *args, **kwargs)
    return _wrapped_view