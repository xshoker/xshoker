from django.db import models


class Genre(models.Model):
    name = models.CharField(max_length=128, db_index=True, unique=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'жанр'
        verbose_name_plural = 'жанры'
        ordering = ['name']


class Book(models.Model):
    name = models.CharField(max_length=64)
    genre = models.ForeignKey(Genre,
                              on_delete=models.CASCADE,
                              null=True)
    year = models.PositiveSmallIntegerField(null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.name} <{self.genre}>'

    def my_author(self):
        author = self.author_set.all()
        return ', '.join(map(str, author))

    class Meta:
        verbose_name = 'книга'
        verbose_name_plural = 'книги'
        ordering = ['pk']


class Description(models.Model):
    book = models.OneToOneField('books.Book',
                                primary_key=True,
                                on_delete=models.CASCADE)
    description = models.TextField()

    def __str__(self):
        return self.description


class Author(models.Model):
    name = models.CharField(max_length=64, unique=True)
    book = models.ManyToManyField(Book)

    def __str__(self):
        return self.name