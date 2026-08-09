# techx_project/urls.py
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve # Import hàm serve

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('', include('techx.urls', namespace='techx')),
    
    path('products/', include(('products.urls', 'products'), namespace='products')),

    path('news/', include(('news.urls', 'news'), namespace='news')),
]



############################################################
#
#   CẢNH BÁO: đoạn mã dưới dây dùng để hiển thị hình anh tĩnh
#   khi DEBUG = False và chỉ nên chạy ở môi trường phát triển, 
#   khi đưa lên production nên vô hiệu hoá hoặc xoá đi.
#
############################################################
urlpatterns += [                                           #
    re_path(r'^media/(?P<path>.*)$', serve, {              #
    'document_root': settings.MEDIA_ROOT,                  #
    }),                                                    #
]                                                          #
############################################################




if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])