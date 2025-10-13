from django.urls import path,include
from .views import RegisterView, LoginView,UserViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('', include(router.urls)),
     # Additional explicit routes for follow/unfollow (optional if using @action)
    path('follow/<int:pk>/', UserViewSet.as_view({'post': 'follow'}), name='follow-user'),
    path('unfollow/<int:pk>/', UserViewSet.as_view({'post': 'unfollow'}), name='unfollow-user'),
]
