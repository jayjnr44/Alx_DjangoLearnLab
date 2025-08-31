# Delete Book Instance

```python
from book_shelf.models import Book
book = Book.objects.get(title="Nineteen Eighty-Four")
book.delete()
print(Book.objects.all())
# Output: <QuerySet []>  # The book has been deleted, so the queryset is empty
```