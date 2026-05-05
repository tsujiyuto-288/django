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
from django.urls import path,include
from accounts import views as accounts_views

urlpatterns = [
    path("users/",include("users.urls")),
    path("admin/", admin.site.urls),
    path("", accounts_views.test_open, name="test_open"),
    path("test2/", accounts_views.test2_open, name="test2_open"),
    path("test3/", accounts_views.Test3PageOpen.as_view(), name="test3_open"),
    path("book_list/", accounts_views.BookListView.as_view(), name="book_list_open"),
    path("book/<int:pk>/", accounts_views.BookDetailView.as_view(), name="book_detail_open"),
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
    path(
        "book/reckoning_price/", accounts_views.reckoning_price, name="reckoning_price"
    ),
    path("book/info/", accounts_views.book_info, name="book_info"),
    path("author/register/", accounts_views.author_register, name="author_register"),
    path(
        "book/author/connect/",
        accounts_views.book_author_connect,
        name="book_author_connect",
    ),
    path("company/register/", accounts_views.company_register, name="company_register"),
    path(
        "company/connect/",
        accounts_views.connect_book_company,
        name="connect_book_company",
    ),
    path(
        "book/stock/register/",
        accounts_views.book_stock_register,
        name="book_stock_register",
    ),
    path(
        "book/stock/register/",
        accounts_views.book_stock_register,
        name="book_stock_register",
    ),
    path(
        "django/form/register/",
        accounts_views.django_form_register,
        name="django_form_register",
    ),
    path(
        "django/form/register/ajax/",
        accounts_views.django_form_register_ajax,
        name="django_form_register_ajax",
    ),
    path(
        "django/model/form/register/",
        accounts_views.django_model_form_register,
        name="django_model_form_register",
    ),
]
