from django import forms
from .models import Book
from django.core.exceptions import ValidationError  

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ["title", "author"]


# ✅ Add ExampleForm
class ExampleForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        required=True,
        label="Your Name",
        widget=forms.TextInput(attrs={"placeholder": "Enter your name"})
    )
    email = forms.EmailField(
        required=True,
        label="Email Address",
        widget=forms.EmailInput(attrs={"placeholder": "Enter your email"})
    )
    message = forms.CharField(
        required=True,
        label="Message",
        widget=forms.Textarea(attrs={"placeholder": "Enter your message"})
    )

def validate_image(file):
    max_mb = 5
    if file.size > max_mb * 1024 * 1024:
        raise ValidationError(f"Max file size is {max_mb}MB")