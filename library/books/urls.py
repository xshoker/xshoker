from django.urls import path
from django.views.generic import TemplateView

from . import views as books

app_name = 'books'

urlpatterns = [
    path('', books.index, name='index'),
    # path('books/', books.animals_list, name='animals_list'),
    path('about/', TemplateView.as_view(template_name='books/about.html'), name='about'),
    path('books/', books.BooksListView.as_view(), name='books_list'),
    path('books/create/', books.GenreCreateView.as_view(), name='genre_create'),
    path('books/update/<int:pk>', books.GenreUpdateView.as_view(), name='genre_update'),
    path('status/<str:task_id>/', books.status_view, name='status_view'),
]