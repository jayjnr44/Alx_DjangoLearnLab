# CRUD Operations Documentation

## Create
```python
from bookshelf.models import Book
book = Book.objects.create(title="1984", author="George Orwell", publication_year=1949)
print(book)
```
# Output
<Book: 1984>

## Retrieve
```python
retrieved_book = Book.objects.get(title="1984")
print(retrieved_book.title, retrieved_book.author, retrieved_book.publication_year)
```
# Output
1984 George Orwell 1949

## Update
```python
retrieved_book.title = "Nineteen Eighty-Four"
retrieved_book.save()
print(retrieved_book.title)
```
# Output
Nineteen Eighty-Four

## Delete
```python
retrieved_book.delete()
print(Book.objects.all())
```
# Output
<QuerySet []>
