from django.shortcuts import render
from django.template.response import TemplateResponse
from django.http import JsonResponse
from accounts.models import Book, Book_stock, Company, Author


def test_open(request):
    return TemplateResponse(request, "test.html")


def create_book(request):
    book = request.POST.get("book")
    
    return JsonResponse({"status": "success"})


def get_model(request):
    pass
