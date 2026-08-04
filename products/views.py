
from django.shortcuts import render
from techx.models import Category, Product, ProductVariant  
from django.shortcuts import render
from django.db.models import Prefetch
from django.core.paginator import Paginator

def product_list(request):
    default_variants = ProductVariant.objects.filter(is_default=True)
    
    products = Product.objects.filter(is_active=True)\
        .select_related('category')\
        .prefetch_related(
            Prefetch('variants', queryset=ProductVariant.objects.all(), to_attr='all_variants'),
            Prefetch('variants', queryset=default_variants, to_attr='default_variants_list')
        )\
        .order_by('-created_at')

    # Lọc danh mục
    category_slug = request.GET.get('category')
    if category_slug:
        products = products.filter(category__slug=category_slug)

    # Phân trang
    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    categories = Category.objects.all()

    return render(request, 'products/products.html', {
        'page_obj': page_obj,
        'categories': categories,
        'selected_category': category_slug,
    })

def contact(request):
    return render(request, 'techx/contact.html')