from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserCreationForm
from django import forms
from django.contrib.auth.models import User


def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = CustomUserCreationForm()
    return render(request, "registration/register.html", {"form": form})


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
    return render(request, "profile.html", {"form": form, "user": user})

