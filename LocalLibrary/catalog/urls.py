from django.urls import path, include
from . import views
from .views import LoanedBooksByUserListView

urlpatterns = [
    path('catalog/', views.catalog_view, name='catalog'),
    # другие маршруты
]

urlpatterns = [
    path('', views.index, name='index'),  # Путь для главной страницы
    path('books/', views.BookListView.as_view(), name='book_list'),  # Перечень книг
    path('book/<int:pk>/', views.BookDetailView.as_view(), name='book_detail'),  # Детальная информация о книге
    path('authors/', views.AuthorListView.as_view(), name='author_list'),  # Путь для списка авторов
    path('author/<int:id>/', views.AuthorDetailView.as_view(), name='author_detail'),  # Путь для деталей автора
]

urlpatterns += [
    path(r'^mybooks/$', views.LoanedBooksByUserListView.as_view(), name='my-borrowed'),
]





