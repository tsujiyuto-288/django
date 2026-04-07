from django.shortcuts import render
from django.template.response import TemplateResponse
from accounts.models import (
    Book,
    Book_stock,
    Company,
    Author
)


def test_open(request):
    return TemplateResponse(request, "test.html")

def create_book(request):
    pass

def get_model(request):
    pass
