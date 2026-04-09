from django.shortcuts import render
from django.template.response import TemplateResponse
from django.http import JsonResponse
from accounts.models import Book, Book_stock, Company, Author


def test_open(request):
    return TemplateResponse(request, "test.html")


def create_book(request):
    book = request.POST.get("book")
    return JsonResponse({"status": "success"})


def get_book(request):
    book_id = request.POST.get("book_id")
    book = Book.objects.get(pk=book_id)
    book_title = book.title
    return JsonResponse({"title": book_title})


def author_filter(request):
    author = request.POST.get("author")
    condition = request.POST.get("condition")

    if condition == "perfect":
        titles = list(
            Book.objects.filter(author__name=author).values_list("title", flat=True)
        )
    elif condition == "contains":
        titles = list(
            Book.objects.filter(author__name__contains=author).values_list(
                "title", flat=True
            )
        )

    return JsonResponse({"titles": titles})


def author_company_filter(request):
    from django.db.models import Q

    author = request.POST.get("author")
    company = request.POST.get("company")
    condition = request.POST.get("condition")

    if condition == "and":
        titles = list(
            Book.objects.filter(
                author__name=author,
                company__name=company,
            ).values_list("title", flat=True)
        )
    elif condition == "or":
        titles = list(
            Book.objects.filter(
                Q(author__name=author) | Q(company__name=company)
            ).values_list("title", flat=True)
        )

    return JsonResponse({"titles": titles})
