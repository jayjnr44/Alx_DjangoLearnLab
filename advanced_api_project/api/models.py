# Import Django's models module to define database models
from django.db import models


# Author model represents a book author in the system.
# Each author has a name and can be linked to multiple books (one-to-many relationship).
class Author(models.Model):
    # The name of the author
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


# Book model represents a book in the system.
# Each book has a title, a publication year, and is linked to a single author.
# The 'author' field establishes a ForeignKey relationship to Author, meaning each book is written by one author,
# but each author can have multiple books (one-to-many relationship).
class Book(models.Model):
    # The title of the book
    title = models.CharField(max_length=255)
    # The year the book was published
    publication_year = models.IntegerField()
    # ForeignKey to Author: links each book to its author
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="books")

    def __str__(self):
        return self.title
