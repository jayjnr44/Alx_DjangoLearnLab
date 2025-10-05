from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Post, Comment, Tag

# Prefer taggit's TagWidget if available (optional dependency)
try:
    from taggit.forms import TagWidget as TaggitTagWidget  # type: ignore
except Exception:
    TaggitTagWidget = None


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
    tags = forms.CharField(
        required=False,
        help_text="Enter comma-separated tags. New tags will be created.",
        widget=(TaggitTagWidget() if TaggitTagWidget is not None else forms.TextInput(attrs={"placeholder": "tag1, tag2, tag3"})),
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
        """
        tag_string = self.cleaned_data.get("tags", "")
        post = super().save(commit=False)

        if author is not None and hasattr(post, "author"):
            post.author = author

        if commit:
            post.save()
            self._save_tags(post, tag_string)
        else:
            # store tag string to use later when save_m2m() is called
            self._pending_tag_string = tag_string

        return post

    def save_m2m(self):
        """
        Handle tags after instance is saved (when commit=False).
        """
        super().save_m2m()
        if hasattr(self, "_pending_tag_string"):
            self._save_tags(self.instance, self._pending_tag_string)

    def _save_tags(self, post, tag_string):
        """Helper to parse a comma-separated string into Tag objects and assign them.

        Uses a case-insensitive lookup to find existing tags; creates missing ones.
        """
        if tag_string:
            tag_names = [t.strip() for t in tag_string.split(",") if t.strip()]
            tag_objs = []
            for name in tag_names:
                # try case-insensitive match first
                existing = Tag.objects.filter(name__iexact=name).first()
                if existing:
                    tag_objs.append(existing)
                else:
                    tag_objs.append(Tag.objects.create(name=name))
            post.tags.set(tag_objs)
        else:
            post.tags.clear()


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["content"]
        widgets = {
            "content": forms.Textarea(
                attrs={"rows": 3, "placeholder": "Wanna add a comment?..."}
            ),
        }
