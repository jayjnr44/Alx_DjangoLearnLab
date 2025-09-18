from django import forms
from .models import Book
from django.core.exceptions import ValidationError


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ["title", "author", "image"]

    image = forms.ImageField(validators=[validate_image], required=False)


def validate_image(file):
    max_mb = 5
    if file.size > max_mb * 1024 * 1024:
        raise ValidationError(f"Max file size is {max_mb}MB")
