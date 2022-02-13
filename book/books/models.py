from django.db import models


class Genre(models.Model):
    name = models.CharField(max_length=128, db_index=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Жанр книги'
        verbose_name_plural = 'Жанры книг'
        ordering = ['name']


class Books(models.Model):
    name = models.CharField(max_length=64)
    genre = models.ForeignKey(Genre,
                             on_delete=models.CASCADE)
    year = models.PositiveSmallIntegerField(null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'книга'
        verbose_name_plural = 'книги'
        ordering = ['pk']


class Description(models.Model):
    book = models.OneToOneField('books.Books',
                                  primary_key=True,
                                  on_delete=models.CASCADE)
    description = models.TextField()

    def __str__(self):
        return f'{self.description}'


class Author(models.Model):
    name = models.CharField(max_length=64)
    Author = models.ManyToManyField(Books)

    def __str__(self):
        return f'{self.name}'