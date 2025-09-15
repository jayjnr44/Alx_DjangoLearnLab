# Delete Operation
from bookshelf.models import Book
```python
retrieved_book.delete()
print(Book.objects.all())
```

# Expected Output
```
<QuerySet []>
# Book deleted successfully. No books found.
```
