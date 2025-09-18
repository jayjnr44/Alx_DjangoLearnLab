from django.urls import path
from . import views

urlpatterns = [
    path("books/", views.book_list, name="book_list"),
    path("books/add/", views.create_book, name="create_book"),
    path("books/<int:pk>/edit/", views.edit_book, name="edit_book"),
    path("books/<int:pk>/delete/", views.delete_book, name="delete_book"),
]
