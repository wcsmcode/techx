from django.contrib import admin
from techx.models import Category, Product, ProductVariant

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)} 


class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'get_price', 'is_active', 'created_at')
    list_filter = ('category', 'is_active')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductVariantInline]

    # Viết hàm lấy giá từ Variant mặc định hoặc Variant đầu tiên
    @admin.display(description='Giá')
    def get_price(self, obj):
        first_variant = obj.variants.first()
        return first_variant.price if first_variant else "Chưa có giá"