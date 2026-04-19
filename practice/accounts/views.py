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
            Book.objects.filter(price__gte=price)
            .order_by("price")
            .values_list("title", flat=True)
        )
    # 超の場合
    elif condition == "gt":
        titles = list(
            Book.objects.filter(price__gt=price)
            .order_by("price")
            .values_list("title", flat=True)
        )
    # 以下の場合
    elif condition == "lte":
        titles = list(
            Book.objects.filter(price__lte=price)
            .order_by("price")
            .values_list("title", flat=True)
        )
    # 未満の場合
    elif condition == "lt":
        titles = list(
            Book.objects.filter(price__lt=price)
            .order_by("price")
            .values_list("title", flat=True)
        )
    # 複数検索の場合
    elif price_1 and price_2:
        titles = list(
            Book.objects.filter(price__range=[price_1, price_2])
            .order_by("price")
            .values_list("title", flat=True)
        )
    # 範囲選択の場合
    elif price_start and price_end:
        titles = list(
            Book.objects.filter(price__range=[price_start, price_end])
            .order_by("price")
            .values_list("title", flat=True)
        )

    return JsonResponse({"titles": titles})


def reckoning_price(request):
    from django.db.models import Max, Min, Sum, Avg

    condition = request.POST.get("reckoning_condition")

    if condition == "max":
        result = Book.objects.aggregate(val=Max("price"))
    elif condition == "min":
        result = Book.objects.aggregate(val=Min("price"))
    elif condition == "sum":
        result = Book.objects.aggregate(val=Sum("price"))
    elif condition == "avg":
        result = Book.objects.aggregate(val=Avg("price"))

    return JsonResponse({"result": result.get("val")})


def book_info(request):
    from django.db.models import F, Value, Count

    book_id = request.POST.get("book_id")

    book_info = (
        Book.objects.filter(id=book_id)
        .annotate(
            tax=F("price") * 1.1,
            stock=F("book_stock__quantity"),
            label=Value("おすすめ！"),
        )
        .values()
        .first()
    )

    return JsonResponse({"info": book_info})


def author_register(request):
    author_name = request.POST.get("author_name")

    author = Author(name=author_name)
    author.save()

    return JsonResponse({"status": "success"})


def book_author_connect(request):
    title = request.POST.get("book_title")
    name = request.POST.get("author_name")

    author = Author.objects.filter(name=name).first()
    book = Book.objects.filter(title=title).first()

    if not title or not name:
        return JsonResponse({"status": "error", "message": "空欄があります"})

    if not book:
        return JsonResponse(
            {"status": "error", "message": "このタイトルの本は登録されていません"}
        )
    if not author:
        return JsonResponse(
            {"status": "error", "message": "この名前の著者は登録されていません"}
        )

    if title and name:
        book.author.add(author)
        return JsonResponse({"status": "success"})


def company_register(request):
    company_name = request.POST.get("company_name")
    has_company = Company.objects.filter(name=company_name).exists()

    if has_company:
        return JsonResponse({"status": "error", "message": "すでに登録されています"})
    if company_name.strip() == "":
        return JsonResponse({"status": "error", "message": "空欄です"})

    company = Company(name=company_name)
    company.save()

    return JsonResponse({"status": "success"})


def connect_book_company(request):
    book_title = request.POST.get("book_title")
    company_name = request.POST.get("company_name")

    book = Book.objects.filter(title=book_title).first()
    company = Company.objects.filter(name=company_name).first()

    if book_title.strip() == "" or company_name.strip() == "":
        return JsonResponse({"status": "error", "message": "空欄があります。"})

    if not book:
        return JsonResponse(
            {"status": "error", "message": "このタイトルの本は登録されていません。"}
        )

    if not company:
        return JsonResponse(
            {"status": "error", "message": "この出版社は登録されていません。"}
        )

    company.book_set.add(book)
    return JsonResponse({"status": "success"})


def book_stock_register(request):
    book_title = request.POST.get("book_title")
    book_stock = request.POST.get("book_stock")

    book = Book.objects.get(title=book_title)
    Book_stock.objects.create(book=book, quantity=int(book_stock))

    return JsonResponse({"status": "success"})


def test2_open(request):
    from django.utils import timezone

    book = Book.objects.get(id=1)
    book_dict = Book.objects.all()
    today = timezone.localdate()

    return render(
        request, "test2.html", {"book": book, "book_dict": book_dict, "today": today}
    )
