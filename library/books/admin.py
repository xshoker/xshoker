from django.contrib import admin
from django.contrib.admin import ModelAdmin

from .models import Book, Genre, Description, Author

admin.site.register(Book)
admin.site.register(Genre)


class BookModelAdmin(ModelAdmin):
    pass


admin.site.register(Author, BookModelAdmin)
admin.site.register(Description)