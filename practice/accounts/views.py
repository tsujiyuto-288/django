from django.shortcuts import render
from django.template.response import TemplateResponse


def test_open(request):
    return TemplateResponse(request, "test.html")
