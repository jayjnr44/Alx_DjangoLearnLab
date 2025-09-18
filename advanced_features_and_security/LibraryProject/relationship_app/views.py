from django.shortcuts import render, redirect,get_object_or_404
from django.views.generic.detail import DetailView
from .models import Library,Book
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.contrib.auth import login
from .forms import BookForm
from django.contrib.auth.decorators import permission_required,user_passes_test
from django.db.models import Q


# Create your views here.
#Function-based view:list all books

def list_books(request):
    books = Book.objects.all()
    return render(request, "relationship_app/list_books.html", {"books": books})

#Class-based view: show library details

class LibraryDetailView(DetailView):
    model = Library
    template_name = "relationship_app/library_detail.html"
    context_object_name = "library"

#custom registration view
def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")#After registration, go to login
        else:
            form = UserCreationForm()
        return render(request, "relationship_app/register.html", {"form": form})
    
class CustomLoginView(LoginView):
    template_name = "relationship_app/login.html"

    def get_success_url(self):
        return reverse_lazy("list_books")
    
class CustomLogoutView(LogoutView):
    template_name = "relationship_app/logout.html"


# Role check helpers
def is_admin(user):
    return hasattr(user, 'userprofile') and user.userprofile.role == 'Admin'

def is_librarian(user):
    return hasattr(user, 'userprofile') and user.userprofile.role == 'Librarian'

def is_member(user):
    return hasattr(user, 'userprofile') and user.userprofile.role == 'Member'

# Admin view
@user_passes_test(is_admin)
def admin_view(request):
    return render(request, "relationship_app/admin_view.html")

# Librarian view
@user_passes_test(is_librarian)
def librarian_view(request):
    return render(request, "relationship_app/librarian_view.html")

# Member view
@user_passes_test(is_member)
def member_view(request):
    return render(request, "relationship_app/member_view.html")

@permission_required("relationship_app.can_add_book")
def add_book(request):
    # your form handling logic here
    return render(request, "relationship_app/add_book.html")

@permission_required("relationship_app.can_change_book")
def edit_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    # edit logic here
    return render(request, "relationship_app/edit_book.html", {"book": book})

@permission_required("relationship_app.can_delete_book")
def delete_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    book.delete()
    return redirect("list_books")

@permission_required("relationship_app.can_add_book")
def add_book(request):
    if request.method == "POST":
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("list_books")
    else:
        form = BookForm()
    return render(request, "relationship_app/add_book.html", {"form": form})


@permission_required("relationship_app.can_change_book")
def edit_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == "POST":
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect("list_books")
    else:
        form = BookForm(instance=book)
    return render(request, "relationship_app/edit_book.html", {"form": form, "book": book})


@permission_required("relationship_app.can_delete_book")
def delete_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == "POST":
        book.delete()
        return redirect("list_books")
    return render(request, "relationship_app/delete_book.html", {"book": book})

def search_books(request):
    q = request.GET.get("q", "").strip()
    books = Book.objects.none()
    if q:
        # parameterized ORM filtering (safe)
        books = Book.objects.filter(Q(title__icontains=q) | Q(author__name__icontains=q))
    return render(request, "relationship_app/search_results.html", {"books": books, "q": q})