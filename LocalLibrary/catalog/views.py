from django.shortcuts import render, get_object_or_404
from .models import Book, Author, BookInstance, Genre
from django.views import generic, View
from django.contrib.auth import logout
from django.shortcuts import redirect


def catalog_view(request):
    # логика представления
    return render(request, 'catalog.html')


def logout_view(request):
    logout(request)
    return redirect('base_generic')


def index(request):
    """
    Функция отображения для домашней страницы сайта.
    """
    # Генерация "количеств" некоторых главных объектов
    num_genres = Genre.objects.all().count()
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    # Доступные книги (статус = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    num_authors = Author.objects.count()  # Метод 'all()' применён по умолчанию.
    num_books_with_word = Book.objects.filter(title__icontains='счастье').count()

    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    # Отрисовка HTML-шаблона index.html с данными внутри переменной контекста context
    return render(
        request,
        'index.html',
        context={
            'num_books': num_books,
            'num_instances': num_instances,
            'num_instances_available': num_instances_available,
            'num_authors': num_authors,
            'num_genres': num_genres,  # Количество жанров
            'num_books_with_word': num_books_with_word,  # Количество книг с "счастье"
            'num_visits': num_visits,  # num_visits appended
        }
    )


class BookListView(generic.ListView):
    model = Book
    template_name = 'catalog/book_list.html'  # Укажите путь к вашему шаблону, если необходимо
    context_object_name = 'book_list'  # Укажите имя контекста, если хотите использовать его в шаблоне


class BookDetailView(generic.DetailView):
    model = Book
    template_name = 'catalog/book_detail.html'  # Укажите путь к вашему шаблону, если необходимо
    context_object_name = 'book_detail'  # Укажите имя контекста, если хотите использовать его в шаблоне


class AuthorListView(generic.ListView):
    model = Author
    template_name = 'catalog/author_list.html'  # Укажите путь к вашему шаблону, если необходимо
    context_object_name = 'authors'  # Укажите имя контекста, если хотите использовать его в шаблоне


class AuthorDetailView(generic.DetailView):
    model = Author
    template_name = 'catalog/author_detail.html'  # Укажите путь к вашему шаблону, если необходимо
    context_object_name = 'author'  # Укажите имя контекста, если хотите использовать его в шаблоне


class AuthorDetailView(generic.DetailView):
    model = Author
    template_name = 'catalog/author_detail.html'  # Укажите путь к вашему шаблону, если необходимо
    context_object_name = 'author'  # Укажите имя контекста, если хотите использовать его в шаблоне


from django.contrib.auth.mixins import LoginRequiredMixin


class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    """
    Generic class-based view listing books on loan to current user.
    """
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')


class MyView(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'

    list_display = ('book', 'status', 'borrower', 'due_back', 'id')
    list_filter = ('status', 'due_back')

    fieldsets = (
        (None, {
            'fields': ('book', 'imprint', 'id')
        }),
        ('Доступность', {
            'fields': ('status', 'due_back', 'borrower')
        }),
    )
