# Import necessary modules for serialization and validation
from rest_framework import serializers
from .models import Author, Book
from datetime import datetime


# BookSerializer serializes all fields of the Book model.
# It also includes custom validation to ensure the publication year is not in the future.
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = "__all__"

    def validate_publication_year(self, value):
        """
        Ensure the publication year is not in the future.
        """
        current_year = datetime.now().year
        if value > current_year:
            raise serializers.ValidationError(
                "Publication year cannot be in the future."
            )
        return value


# AuthorSerializer serializes the Author model, including the author's name and a nested list of books.
# The 'books' field uses BookSerializer to serialize all books related to the author (one-to-many relationship).
# This is achieved by setting 'books = BookSerializer(many=True, read_only=True)', which leverages the related_name
# on the Book model's ForeignKey to Author.
class AuthorSerializer(serializers.ModelSerializer):
    # Nested serialization of related books for each author
    books = BookSerializer(many=True, read_only=True)

    class Meta:
        model = Author
        fields = ["name", "books"]


# Relationship explanation:
# In the serializers, the relationship between Author and Book is handled by the 'books' field in AuthorSerializer.
# This field uses the related_name 'books' defined in the Book model's ForeignKey to Author, allowing each author
# to include a list of their books, serialized using BookSerializer. This provides a nested representation of the
# one-to-many relationship from Author to Book in API responses.
