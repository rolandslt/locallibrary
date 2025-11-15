from django.shortcuts import render

# Create your views here.
from .models import Book, Author, BookInstance, Genre
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

def index(request):
    """View function for home page of site"""

    # Generate counts of some of the main objects
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    # Available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()

    # The 'all()' is implied by default.
    num_authors = Author.objects.count()
    num_genre = Genre.objects.count()
    num_science_books = Book.objects.filter(title__icontains='Science').count()
    num_visits = request.session.get('num_visits', 0)
    num_visits += 1
    request.session['num_visits'] = num_visits
    context = {
        'num_books': num_books,
        'num_instance': num_instances,
        'num_instance_available': num_instances_available,
        'num_authors': num_authors,
        'num_genre': num_genre,
        'num_science_books': num_science_books,
        'num_visits': num_visits,
    }

    # Render the HTML template index.html with the data in the context variable

    return render(request, 'index.html', context=context)

class BookListView(generic.ListView):
    model = Book
    context_object_name = 'book_list' # name for the list as a template variable
    #queryset = Book.objects.filter(title__icontains='The')[:5] # Get 5 books containing the title war
    template_name = 'books/book_list.html'
    paginate_by = 10

class BookDetailView(generic.DetailView):
    model = Book

class AuthorListView(generic.ListView):
    model = Author
    context_object_name = 'author_list'
    template_name = 'authors/author_list.html'

class AuthorDetailView(generic.DetailView):
    model = Author

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['books'] = Book.objects.filter(author=self.object)
        return context
    
class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    """Generic class-base view listing books on loan to current user."""
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return (
            BookInstance.objects.filter(borrower=self.request.user)
            .filter(status__exact='o')
            .order_by('due_back')
        )