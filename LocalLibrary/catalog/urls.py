from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # Путь для главной страницы
    path('books/', views.BookListView.as_view(), name='books'),  # Путь для списка книг
    path('book/<int:pk>/', views.BookDetailView.as_view(), name='book-detail'),  # Путь для деталей книги
]


