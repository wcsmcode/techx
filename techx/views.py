from django.shortcuts import render
from django.db.models import Prefetch, Min
from django.core.paginator import Paginator
from .models import Product, ProductVariant, Category

def base(request):
    return render(request, 'base.html')

def techx_homepage(request):

    products = Product.objects.filter(is_active=True)\
        .select_related('category')\
        .prefetch_related('variants', 'specs')[:8]

    return render(request, 'techx/homepage.html', {'products': products})


def contact(request):
    return render(request, 'techx/contact.html')