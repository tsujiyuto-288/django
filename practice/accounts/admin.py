from django.contrib import admin
from accounts.models import Book, Book_stock, Author, Company

admin.site.register(Book)
admin.site.register(Book_stock)
admin.site.register(Author)
admin.site.register(Company)
