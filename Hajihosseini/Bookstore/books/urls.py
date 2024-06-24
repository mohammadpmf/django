from django.urls import path

from .views import BookListView, BookDetailView, BookCreateView, BookDeleteView, BookUpdateView, book_detail_view, BookMyFavorites1, BookMyFavorites2

urlpatterns = [
    path('', BookListView.as_view(), name='books'),
    path('my_favorites/', BookMyFavorites2.as_view(), name='my_favorites'),
    path('<int:pk>/', BookDetailView.as_view(), name='book_detail'),
    # path('<int:pk>/', book_detail_view, name='book_detail'),
    path('create/', BookCreateView.as_view(), name='book_create'),
    path('update/<int:pk>/', BookUpdateView.as_view(), name='book_update'),
    path('delete/<int:pk>/', BookDeleteView.as_view(), name='book_delete'),
]
