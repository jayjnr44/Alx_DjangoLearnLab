from django import forms
from .models import Book
from django.core.exceptions import ValidationError


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ["title", "author", "image"]

    image = forms.ImageField(required=False)

    def clean_image(self):
        image = self.cleaned_data.get("image")
        if not image:
            return image
        max_mb = 5
        if image.size > max_mb * 1024 * 1024:
            raise ValidationError(f"Max file size is {max_mb}MB")
        return image


def validate_image(file):
    max_mb = 5
    if file.size > max_mb * 1024 * 1024:
        raise ValidationError(f"Max file size is {max_mb}MB")
