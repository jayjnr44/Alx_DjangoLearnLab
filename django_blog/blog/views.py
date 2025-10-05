from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserCreationForm, PostForm, RegisterForm, CommentForm
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import login
from .models import Post, Comment
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.db.models import Q


def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = CustomUserCreationForm()
    return render(request, "blog/register.html", {"form": form})


# Profile update form
class ProfileUpdateForm(forms.ModelForm):
    bio = forms.CharField(required=False, widget=forms.Textarea)
    profile_picture = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ["email"]


@login_required
def profile(request):
    user = request.user
    # Initial data for bio and profile_picture (if using extended user model)
    initial = {
        "bio": getattr(user, "bio", ""),
        "profile_picture": getattr(user, "profile_picture", None),
    }
    if request.method == "POST":
        form = ProfileUpdateForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            # Save bio and profile_picture if present
            bio = form.cleaned_data.get("bio")
            profile_picture = form.cleaned_data.get("profile_picture")
            if hasattr(user, "bio"):
                user.bio = bio
            if hasattr(user, "profile_picture") and profile_picture:
                user.profile_picture = profile_picture
            user.save()
            messages.success(request, "Profile updated successfully.")
            return redirect("profile")
    else:
        form = ProfileUpdateForm(instance=user, initial=initial)
    return render(request, "blog/profile.html", {"form": form, "user": user})


class PostListView(ListView):
    model = Post
    template_name = "blog/post_list.html"  # blog/templates/blog/post_list.html
    context_object_name = "posts"
    paginate_by = 10

    def get_queryset(self):
        """Allow searching posts by title, content, or tag name using ?q=..."""
        qs = super().get_queryset().prefetch_related("Tag")
        q = self.request.GET.get("q")
        if q:
            # search title, content, and related Tag name (case-insensitive)
            qs = qs.filter(
                Q(title__icontains=q)
                | Q(content__icontains=q)
                | Q(Tag__name__icontains=q)
            ).distinct()
        return qs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['q'] = self.request.GET.get('q', '')
        # Heading helps templates display whether this is a search or normal listing
        context['heading'] = 'Search results' if self.request.GET.get('q') else 'Posts'
        return context


class TagPostListView(PostListView):
    """List posts filtered by a tag name passed in the URL as `tag_name`."""

    def get_queryset(self):
        qs = super().get_queryset()
        tag_name = self.kwargs.get('tag_name')
        if tag_name:
            qs = qs.filter(Tag__name__iexact=tag_name).distinct()
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['heading'] = f"Posts tagged '{self.kwargs.get('tag_name')}'"
        context['tag_name'] = self.kwargs.get('tag_name')
        return context


class SearchResultsView(PostListView):
    """Explicit view for search results; delegates to PostListView filtering via ?q="""
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['heading'] = f"Search results for \"{self.request.GET.get('q','')}\""
        return context


class PostDetailView(DetailView):
    model = Post
    template_name = "blog/post_detail.html"
    context_object_name = "post"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # include comments and an empty form for posting new comments
        context["comments"] = self.object.comments.all()
        context["comment_form"] = CommentForm()
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = "blog/post_form.html"

    def form_valid(self, form):
        # set author to logged-in user
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = "blog/post_form.html"

    def test_func(self):
        post = self.get_object()
        return post.author == self.request.user


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = "blog/post_confirm_delete.html"
    success_url = reverse_lazy("post-list")

    def test_func(self):
        post = self.get_object()
        return post.author == self.request.user


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = "blog/comment_form.html"

    def form_valid(self, form):
        # assign the logged in user and the post (post id passed in url)
        form.instance.author = self.request.user
        post_pk = self.kwargs.get("post_pk")
        form.instance.post = get_object_or_404(Post, pk=post_pk)
        return super().form_valid(form)


class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = "blog/comment_form.html"

    def test_func(self):
        comment = self.get_object()
        return comment.author == self.request.user


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = "blog/comment_confirm_delete.html"

    def get_success_url(self):
        # redirect back to the post detail page after deletion
        return reverse_lazy("post-detail", kwargs={"pk": self.object.post.pk})

    def test_func(self):
        comment = self.get_object()
        return comment.author == self.request.user
