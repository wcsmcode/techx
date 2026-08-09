from django.shortcuts import render, get_object_or_404
from techx.models import Category, Product, ProductVariant  
from django.db.models import Prefetch, Q
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

    # 1. Lấy param tìm kiếm và danh mục
    query = request.GET.get('q', '').strip()
    category_slug = request.GET.get('category')

    # 2. Xử lý Lọc theo Từ khóa Tìm kiếm
    if query:
        products = products.filter(
            Q(name__icontains=query) | 
            Q(description__icontains=query)
        ).distinct()

    # 3. Xử lý Lọc danh mục
    if category_slug:
        products = products.filter(category__slug=category_slug)

    # 4. Phân trang
    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    categories = Category.objects.all()

    return render(request, 'products/products.html', {
        'page_obj': page_obj,
        'categories': categories,
        'selected_category': category_slug,
        'query': query,  # Truyền 'query' ra template để giữ chữ trên thanh search & thông báo
    })

def product_detail(request, slug):
    # Lấy sản phẩm theo slug, nếu không thấy thì quăng lỗi 404
    product = get_object_or_404(Product, slug=slug, is_active=True)
    
    # Lấy các variant thuộc sản phẩm này
    variants = product.variants.all()
    
    return render(request, 'products/product_detail.html', {
        'product': product,
        'variants': variants,
    })