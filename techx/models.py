from django.db import models
from django.core.exceptions import ValidationError
from slugify import slugify  


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True, blank=True, db_index=True)

    class Meta:
        verbose_name_plural = "Categories"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=255, db_index=True)
    brand = models.CharField(max_length=100, default="TechX", db_index=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.brand}-{self.name}")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"[{self.brand}] {self.name}"

    @property
    def default_variant(self):
        """Helper lấy variant mặc định hoặc variant đầu tiên để hiển thị trên UI"""
        return self.variants.filter(is_default=True).first() or self.variants.first()


class ProductVariant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variants')
    sku = models.CharField(max_length=50, unique=True, db_index=True)
    color_name = models.CharField(max_length=50, help_text="Màu sắc: Matte Black, Cyber White...")
    spec_option = models.CharField(max_length=100, blank=True, help_text="Tùy chọn cấu hình: 16GB/512GB, Red Switch...")
    price = models.DecimalField(max_digits=12, decimal_places=0, db_index=True) 
    stock = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    is_default = models.BooleanField(default=False)

    class Meta:
       
        unique_together = ('product', 'color_name', 'spec_option')

    def save(self, *args, **kwargs):
        
        if self.is_default:
            ProductVariant.objects.filter(product=self.product, is_default=True).exclude(pk=self.pk).update(is_default=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product.name} - {self.color_name} ({self.spec_option})"


class ProductSpecification(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='specs')
    key = models.CharField(max_length=100, db_index=True, help_text="VD: Kết nối, Pin, Trọng lượng")
    value = models.CharField(max_length=255, help_text="VD: Bluetooth 5.1 / Type-C, 4000mAh, 790g")

    class Meta:
        
        unique_together = ('product', 'key')

    def __str__(self):
        return f"{self.product.name} - {self.key}: {self.value}"