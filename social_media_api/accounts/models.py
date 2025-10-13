from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class CustomUser(AbstractUser):
    bio = models.TextField(blank=True),    
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True),
    followers =models.ManyToManyField('self', symmetrical=False, related_name='following', blank=True)

    def __str__(self):
        return self.username
    
    def follow(self, user):
        """Follow another user"""
        if user != self:
            self.following.add(user)
    
    def unfollow(self, user):
        """Unfollow another user"""
        if user != self:
            self.following.remove(user)
    
    def is_following(self, user):
        """Check if following another user"""
        return self.following.filter(id=user.id).exists()
    
    def is_followed_by(self, user):
        """Check if followed by another user"""
        return self.followers.filter(id=user.id).exists()