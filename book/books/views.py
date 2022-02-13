from django.shortcuts import render

from books.models import Books


def index(request):
    return render(request, 'books/index.html')


def books_list(request):
    books = Books.objects.all()
    context = {
        'books': books
    }
    return render(request, 'books/books_list.html', context=context)