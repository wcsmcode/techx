from django.shortcuts import render
from .models import Product
# Create your views here.

def base(request):
    return render(request, 'techx/base.html')

def techx_homepage(request):
    # Fetch 8 sản phẩm mới nhất kèm biến thể & thông số
    products = Product.objects.filter(is_active=True)\
        .select_related('category')\
        .prefetch_related('variants', 'specs')[:8]

    return render(request, 'techx/homepage.html', {'products': products})