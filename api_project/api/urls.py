from django.urls import path, include
from .views import BookList
from rest_framework.routers import DefaultRouter
from .views import BookViewSet, BookList

router = DefaultRouter()
router.register(r'books_all', BookViewSet, basename='book_all')


urlpatterns = [
    path('books/', BookList.as_view(), name="book_list_create"),
    
    path('', include(router.urls)),
]