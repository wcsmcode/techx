from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

class Article(models.Model):
    title = models.CharField(max_length=255, verbose_name="Tiêu đề")
    slug = models.SlugField(unique=True, max_length=255, blank=True)
    summary = models.TextField(blank=True, verbose_name="Tóm tắt ngắn")
    content = models.TextField(verbose_name="Nội dung bài viết")
    image = models.ImageField(upload_to='news/', blank=True, null=True, verbose_name="Ảnh đại diện")
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    views_count = models.PositiveIntegerField(default=0, verbose_name="Lượt xem")
    is_published = models.BooleanField(default=True, verbose_name="Công khai")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Bài viết"
        verbose_name_plural = "Danh sách bài viết"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title