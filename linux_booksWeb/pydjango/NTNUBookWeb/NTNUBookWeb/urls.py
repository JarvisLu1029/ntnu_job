"""NTNUBookWeb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from django.conf import settings
from django.conf.urls.static import static

# 自己創建App中的views文件
from books import views


urlpatterns = [
    path("admin/", admin.site.urls),

    # 自己增加的路徑
    path("index/", views.index),
    # 使用者所有書籍
    path('books/<str:user>/', views.get_books_by_user, name='get_books_by_user'),
    # 作者或關鍵字搜尋
    path('books/<str:user>/book_search/', views.get_books_by_search, name='books_search'),
    # 作者與年份排序
    path('books/<str:user>/orderby/<str:sort>' ,views.get_books_orderby, name='books_orderby'),
    # 新增書籍
    path('books/<str:user>/add/', views.book_add, name='book_add'),
    # 刪除書籍
    path('books/<str:user>/del_<str:title>', views.book_delete, name='book_delete'),
    # 編輯書籍
    path('books/<str:user>/update_<str:title>', views.book_update, name='book_update'),
    # 編輯心得
    path('books/<str:user>/<str:title>/note', views.book_note_update, name='book_note_update'),
    ]

