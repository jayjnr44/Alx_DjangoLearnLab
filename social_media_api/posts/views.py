from rest_framework import viewsets, permissions, filters
from rest_framework.exceptions import PermissionDenied
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q


class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Custom permission: only allow authors to edit or delete their own posts/comments.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed for any request
        if request.method in permissions.SAFE_METHODS:
            return True
        # Write permissions only for the author
        return obj.author == request.user


class PostViewSet(viewsets.ModelViewSet):
    """
    Handles CRUD for Posts.
    - List all posts
    - Retrieve single post
    - Create new post
    - Update/delete only own posts
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    # Enable search by title and content
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'content']
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']

    def perform_create(self, serializer):
        # Assign the logged-in user as author
        serializer.save(author=self.request.user)

    def get_queryset(self):
        # Default: show all posts (optional filtering by query params)
        queryset = Post.objects.all().order_by('-created_at')
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(Q(title__icontains=search) | Q(content__icontains=search))
        return queryset

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def feed(self, request):
        """Return a feed of posts from users the current user follows."""
        user = request.user
        followed_users = user.following.all()
        posts = Post.objects.filter(author__in=followed_users).order_by('-created_at')

        # Paginate the results
        page = self.paginate_queryset(posts)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CommentViewSet(viewsets.ModelViewSet):
    """
    Handles CRUD for Comments.
    - List all comments or filter by post
    - Create new comment
    - Update/delete only own comments
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['created_at']
    ordering = ['created_at']
    
    def perform_create(self, serializer):
        # Assign the logged-in user as author
        serializer.save(author=self.request.user)

    def get_queryset(self):
        # Optional: Filter comments by post ID via ?post=<post_id>
        queryset = super().get_queryset()
        post_id = self.request.query_params.get('post')
        if post_id:
            queryset = queryset.filter(post__id=post_id)
        return queryset
