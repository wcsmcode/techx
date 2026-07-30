# models.py
from django.db import models
from django.utils.text import slugify

class Category(models.Model):
    name = models.CharField(max_length=100) # Ví dụ: Bàn phím cơ, Tai nghe, Chuột
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=255, db_index=True) # Ví dụ: Keychron K2 V2
    brand = models.CharField(max_length=100, default="TechX") # Ví dụ: Keychron, Sony, Logitech
    slug = models.SlugField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"[{self.brand}] {self.name}"

class ProductVariant(models.Model):
    """Lưu biến thể theo MÀU SẮC và Option cấu hình chính (Ví dụ: Đen / Red Switch)"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variants')
    sku = models.CharField(max_length=50, unique=True) # VD: TX-K2-BLK-RED
    color_name = models.CharField(max_length=50, help_text="Màu sắc: Matte Black, Cyber White...")
    spec_option = models.CharField(max_length=100, blank=True, help_text="Tùy chọn cấu hình: 16GB/512GB, Red Switch...")
    price = models.DecimalField(max_digits=12, decimal_places=0) # Đồ công nghệ xài VND nên dùng decimal_places=0
    stock = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    is_default = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.product.name} - {self.color_name} ({self.spec_option})"

class ProductSpecification(models.Model):
    """Lưu bảng thông số kỹ thuật chi tiết để show lên UI và dùng để Filter"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='specs')
    key = models.CharField(max_length=100, help_text="VD: Kết nối, Pin, Trọng lượng")
    value = models.CharField(max_length=255, help_text="VD: Bluetooth 5.1 / Type-C, 4000mAh, 790g")

    def __str__(self):
        return f"{self.product.name} - {self.key}: {self.value}"