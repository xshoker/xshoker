from django.contrib import admin
from books.models import Books, Genre, Description, Author
# Register your models here.
from django.contrib.admin import ModelAdmin
admin.site.register(Books)
admin.site.register(Genre)
admin.site.register(Description)
admin.site.register(Author)