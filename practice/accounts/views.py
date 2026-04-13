from django.shortcuts import render
from django.template.response import TemplateResponse
from django.http import JsonResponse
from accounts.models import Book, Book_stock, Company, Author


def test_open(request):
    return TemplateResponse(request, "test.html")


def register_book(request):
    title = request.POST.get("title")
    price = request.POST.get("price")

    if not Book.objects.filter(title=title).exists():
        book = Book(title=title)
        book.price = price
        book.save()
        return JsonResponse({"status": "success"})
    else:
        return JsonResponse({"status": "error_tyouhuku"})


def delete_book(request):
    delete_title = request.POST.get("delete_title")

    delete_books = Book.objects.filter(title=delete_title)

    if delete_books:
        delete_books.delete()
        return JsonResponse({"status": "success"})
    elif not delete_books:
        return JsonResponse({"status": "none"})


def get_book(request):
    book_id = request.POST.get("book_id")
    condition = request.POST.get("condition")

    if condition == "get_title":
        result = Book.objects.get(pk=book_id).title
    elif condition == "exists":
        result = Book.objects.filter(pk=book_id).exists()
    elif condition == "count":
        result = Book.objects.filter(pk=book_id).count()

    return JsonResponse({"result": result})


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
    elif condition == "icontains":
        titles = list(
            Book.objects.filter(author__name__icontains=author).values_list(
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


def price_filter(request):
    price = request.POST.get("price")
    condition = request.POST.get("filter")
    price_1 = request.POST.get("price_1")
    price_2 = request.POST.get("price_2")
    price_start = request.POST.get("price_start")
    price_end = request.POST.get("price_end")

    # 以上の場合
    if condition == "gte":
        titles = list(
            Book.objects.filter(price__gte=price).values_list("title", flat=True)
        )
    # 超の場合
    elif condition == "gt":
        titles = list(
            Book.objects.filter(price__gt=price).values_list("title", flat=True)
        )
    # 以下の場合
    elif condition == "lte":
        titles = list(
            Book.objects.filter(price__lte=price).values_list("title", flat=True)
        )
    # 未満の場合
    elif condition == "lt":
        titles = list(
            Book.objects.filter(price__lt=price).values_list("title", flat=True)
        )
    # 複数検索の場合
    elif price_1 and price_2:
        titles = list(
            Book.objects.filter(price__range=[price_1, price_2]).values_list(
                "title", flat=True
            )
        )
    # 範囲選択の場合
    elif price_start and price_end:
        titles = list(
            Book.objects.filter(price__range=[price_start, price_end]).values_list(
                "title", flat=True
            )
        )

    return JsonResponse({"titles": titles})
