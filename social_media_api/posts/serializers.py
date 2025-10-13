from rest_framework import serializers
from .models import Post, Comment
from accounts.models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    """Minimal user serializer for displaying author info in Post/Comment."""
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'profile_picture']

class CommentSerializer(serializers.ModelSerializer):
    """Serializer for Comment model."""
    author = UserSerializer(read_only=True)
    post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all())

    class Meta:
        model = Comment
        fields = ['id', 'post', 'author', 'content', 'created_at', 'updated_at']
        read_only_fields = ['id', 'author', 'created_at', 'updated_at']

    def create(self, validated_data):
        """Attach the logged-in user as the comment author."""
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            validated_data['author'] = request.user
        return super().create(validated_data)
    
    def validate_content(self, value):
        """Ensure comments aren’t empty or too short."""
        if len(value.strip()) < 5:
            raise serializers.ValidationError("Comment must be at least 5 characters long.")
        return value
    

class PostSerializer(serializers.ModelSerializer):
    """Serializer for Post model with nested comments."""
    author = UserSerializer(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'author', 'title', 'content', 'created_at', 'updated_at', 'comments']
        read_only_fields = ['id', 'author', 'created_at', 'updated_at', 'comments']

    def create(self, validated_data):
        """Attach the logged-in user as the post author."""
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            validated_data['author'] = request.user
        return super().create(validated_data)
    
    def validate_title(self, value):
        """Ensure titles aren’t empty or too short."""
        if len(value.strip()) < 5:
            raise serializers.ValidationError("Title must be at least 5 characters long.")
        return value

    def validate_content(self, value):
        """Ensure posts aren't empty or too short."""
        if len(value.strip()) < 10:
            raise serializers.ValidationError("Content must be at least 10 characters long.")
        return value