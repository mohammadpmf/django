from django.urls import path
from . import views


urlpatterns = [
    path('', views.PostListView.as_view(), name='posts_list'),
    path('detail/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
    path('create/', views.PostCreateView.as_view(), name='post_create'),
    path('update/<int:pk>/', views.PostUpdateView.as_view(), name='post_update'),
    path('delete/<int:pk>/', views.PostDeleteView.as_view(), name='post_delete'),
    path('read_more/', views.ReadMoreView.as_view(), name='read_more'),
]
