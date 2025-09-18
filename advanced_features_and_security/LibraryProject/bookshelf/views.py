from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import permission_required
from .models import Book

# Create your views here.

# View books (requires can_view)
@permission_required('relationship_app.can_view', raise_exception=True)
def book_list(request):
    books = Book.objects.all()
    return render(request, "relationship_app/book_list.html", {"books": books})

# Create book (requires can_create)
@permission_required('relationship_app.can_create', raise_exception=True)
def create_book(request):
    if request.method == "POST":
        title = request.POST.get("title")
        author = request.POST.get("author")
        year = request.POST.get("publication_year")
        Book.objects.create(title=title, author=author, publication_year=year)
        return redirect("book_list")
    return render(request, "relationship_app/book_form.html")

# Edit book (requires can_edit)
@permission_required('relationship_app.can_edit', raise_exception=True)
def edit_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == "POST":
        book.title = request.POST.get("title")
        book.author = request.POST.get("author")
        book.publication_year = request.POST.get("publication_year")
        book.save()
        return redirect("book_list")
    return render(request, "relationship_app/book_form.html", {"book": book})

# Delete book (requires can_delete)
@permission_required('relationship_app.can_delete', raise_exception=True)
def delete_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    book.delete()
    return redirect("book_list")



