from django.contrib import admin
from django.urls import path, include

from .settings import DEBUG

urlpatterns = [
    path('', include('books.urls', namespace='books')),
    path('admin/', admin.site.urls),
]

if DEBUG:
    urlpatterns.append(
        path('__debug__/', include('debug_toolbar.urls')),
    )