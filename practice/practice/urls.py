"""
URL configuration for practice project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from accounts import views as accounts_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", accounts_views.test_open, name="test_open"),
    path("book/register/", accounts_views.register_book, name="register_book"),
    path("book/delete/", accounts_views.delete_book, name="delete_book"),
    path("book/get/", accounts_views.get_book, name="get_book"),
    path("book/author_filter/", accounts_views.author_filter, name="author_filter"),
    path(
        "book/author_company_filter/",
        accounts_views.author_company_filter,
        name="author_company_filter",
    ),
    path("book/price_filter/", accounts_views.price_filter, name="price_filter"),
]
