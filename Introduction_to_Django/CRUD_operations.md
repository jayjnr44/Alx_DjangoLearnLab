# Create Book Instance

```python
from book_shelf.models import Book
book = Book.objects.create(title="1984", author="George Orwell", publication_year=1949)
print(book)
# Output: 1984 by George Orwell (1949)
```

# Retrieve Book Instance

```python
from book_shelf.models import Book
book = Book.objects.get(title="1984")
print(book.title, book.author, book.publication_year)
# Output: 1984 George Orwell 1949
```

# Update Book Instance

```python
from book_shelf.models import Book
book = Book.objects.get(title="1984")
book.title = "Nineteen Eighty-Four"
book.save()
print(book.title)
# Output: Nineteen Eighty-Four
```
# Delete Book Instance

```python
from book_shelf.models import Book
book = Book.objects.get(title="Nineteen Eighty-Four")
book.delete()
print(Book.objects.all())
# Output: <QuerySet []>  # The book has been deleted, so the queryset is empty
```
