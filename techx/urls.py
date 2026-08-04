# techx/urls.py
from django.urls import path
from . import views

app_name = 'techx'

urlpatterns = [
    # Route cho Trang chủ
    path('', views.techx_homepage, name='homepage'),
    path('contact/', views.contact, name='contact'),
]