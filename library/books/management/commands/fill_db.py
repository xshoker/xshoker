from random import choice, randint, sample

from django.core.management.base import BaseCommand

from library.books.models import Genre, Book, Author


class Command(BaseCommand):

    def handle(self, *args, **options):
        genres = ['Horror', 'Comedy', 'Detective']
        genres_obj = []
        for animal_kind in genres:
            # animal_kinds_obj[animal_kind] = AnimalKind.objects.create(name=animal_kind)
            _obj, created = Genre.objects.get_or_create(name=Genre)
            genres_obj.append(_obj)

        books = ['War and Piece', 'Artemis Fawl']
        books_obj = []
        for book in books:
            _obj = Book.objects.create(name=Book,
                                       genre=choice(genres_obj),
                                       year=randint(1, 10))
            books_obj.append(_obj)

        authors = ['Tolstoy', 'Ion Kofler']
        author_obj = []
        for author in authors:
            _obj, created = Author.objects.get_or_create(name=author)
            author_obj.append(_obj)

        for author in author_obj:
            books = sample(books_obj, k=randint(1, len(books_obj)))
            for book in books:
                author.book.add(book)
            book.save()