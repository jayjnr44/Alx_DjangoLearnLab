from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Post, Comment


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class PostForm(forms.ModelForm):
    # Accept comma-separated tag names from the form (e.g. "django, python, tips")
    tags = forms.CharField(
        required=False,
        help_text="Enter comma-separated tags. New tags will be created.",
        widget=forms.TextInput(attrs={"placeholder": "tag1, tag2, tag3"}),
    )

    class Meta:
        model = Post
        fields = ["title", "content", "tags"]
        widgets = {
            "title": forms.TextInput(attrs={"placeholder": "Post Title"}),
            "content": forms.Textarea(
                attrs={"rows": 10, "placeholder": "Write your post here..."}
            ),
        }

    def save(self, commit=True, author=None):
        """
        Save the Post instance and handle tags.

        - `tags` field accepts comma-separated names. New Tag objects are created if needed.
        - If `author` is provided, attach it to the post before saving.
        """
        # Pop tag string from cleaned_data so ModelForm doesn't try to set it directly
        tag_string = self.cleaned_data.pop("tags", "")

        post = super().save(commit=False)
        if author is not None and hasattr(post, "author"):
            post.author = author

        if commit:
            post.save()

        # Parse tag names, create or get Tag objects, and assign to post
        if tag_string:
            # Split by comma and normalize whitespace, ignore empty names
            tag_names = [t.strip() for t in tag_string.split(",") if t.strip()]
            from .models import Tag

            tag_objs = []
            for name in tag_names:
                tag_obj, _ = Tag.objects.get_or_create(
                    name__iexact=name, defaults={"name": name}
                )
                tag_objs.append(tag_obj)

            # assign tags (replace any existing tags)
            post.Tag.set(tag_objs)
        else:
            # If empty string provided, clear tags
            if post.pk:
                post.Tag.clear()

        return post


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["content"]
        widgets = {
            "content": forms.Textarea(
                attrs={"rows": 3, "placeholder": "Wanna add a comment?..."}
            ),
        }
