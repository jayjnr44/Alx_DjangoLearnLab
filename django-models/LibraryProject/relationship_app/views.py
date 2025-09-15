from django.shortcuts import render, redirect
from django.views.generic.detail import DetailView
from .models import Library,Book
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.contrib.auth import login


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