# news/admin.py
from django.contrib import admin
from .models import Article

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    # Các cột hiển thị trong danh sách bài viết
    list_display = ('title', 'is_published', 'views_count', 'author', 'created_at')
    
    # Bộ lọc ở cột bên phải
    list_filter = ('is_published', 'created_at', 'author')
    
    # Ô tìm kiếm
    search_fields = ('title', 'summary', 'content')
    
    # Tự động điền slug khi gõ tiêu đề (Title)
    prepopulated_fields = {'slug': ('title',)}
    
    # Cho phép tích/bỏ tích 'Công khai' trực tiếp ngay tại danh sách
    list_editable = ('is_published',)
    
    # Chỉ đọc các trường tự động
    readonly_fields = ('views_count', 'created_at', 'updated_at')
    
    # Số lượng bài viết trên 1 trang Admin
    list_per_page = 20
    
    # Tự động gán user đang đăng nhập làm tác giả khi tạo bài mới nếu chưa chọn
    def save_model(self, request, obj, form, change):
        if not obj.author:
            obj.author = request.user
        super().save_model(request, obj, form, change)