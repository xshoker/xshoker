import time

from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView

from .models import Book, Genre
from .celery import celery_app

from .tasks import send_mail_task


def index(request):
    task_id = None
    if request.method == 'POST':
        print(time.time())
        task = send_mail_task.delay('subject', 'abcde')
        print(time.time())
        task_id = task.id
    context = {'task_id': task_id}

    return render(request, 'books/index.html', context=context)


class PageTitleListMixin:
    p_title = ''

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['p_title'] = self.p_title
        return context


class BooksListView(PageTitleListMixin, ListView):
    model = Book
    p_title = 'Library Books'

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.select_related('genre').\
            prefetch_related('author_set').all()
        return qs


def status_view(request, task_id):
    print(task_id)
    task = celery_app.AsyncResult(task_id)
    context = {'task_id': task_id,
               'status': task.status}

    return render(request, 'books/status.html', context=context)


class GenreCreateView(CreateView):
    model = Genre
    success_url = reverse_lazy('books:books_list')
    fields = '__all__'


class GenreUpdateView(UpdateView):
    model = Genre
    success_url = reverse_lazy('books:books_list')
    fields = '__all__'
