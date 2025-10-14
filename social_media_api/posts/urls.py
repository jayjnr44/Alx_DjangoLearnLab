from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, CommentViewSet
from . import views

router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='post')
router.register(r'comments', CommentViewSet, basename='comment')


urlpatterns = [
    path('', include(router.urls)),
    # Explicit route for feed (optional since it's defined with @action)
    path('feed/', PostViewSet.as_view({'get': 'feed'}), name='user-feed'),
       # Like and Unlike routes
    path('posts/<int:pk>/like/', views.PostViewSet.as_view({'post: like'}), name='like-post'),
    path('posts/<int:pk>/unlike/', views.PostViewSet.as_view({'post: unlike'}), name='unlike-post'),]
