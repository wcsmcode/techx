from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import F, Q
from .models import Article

def news_list(request):
    articles = Article.objects.filter(is_published=True)
    
    # Xử lý tìm kiếm
    query = request.GET.get('q', '').strip()
    if query:
        articles = articles.filter(
            Q(title__icontains=query) | 
            Q(content__icontains=query)
        ).distinct()

    paginator = Paginator(articles, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'news/news.html', {
        'page_obj': page_obj,
        'query': query
    })

def news_detail(request, slug):
    article = get_object_or_404(Article, slug=slug, is_published=True)
    
    # Tăng lượt xem an toàn (chống race condition)
    Article.objects.filter(pk=article.pk).update(views_count=F('views_count') + 1)
    article.refresh_from_db()

    # Lấy 3 bài viết mới nhất để làm "Bài viết liên quan"
    related_articles = Article.objects.filter(is_published=True).exclude(id=article.id)[:3]

    return render(request, 'news/news_detail.html', {
        'article': article,
        'related_articles': related_articles,
    })