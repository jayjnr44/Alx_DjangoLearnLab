# Create Operation

```python
from bookshelf.models import Book
book = Book.objects.create(title="1984", author="George Orwell", publication_year=1949)
print(book)
```

# Expected Output
```
<Book: 1984>
# (or similar, depending on __str__ method)
# Book instance created successfully.
```
