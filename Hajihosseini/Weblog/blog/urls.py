from django.urls import path
from . import views


urlpatterns = [
    path('', views.post_list_view, name='posts_list'),
    path('detail/<int:pk>/', views.post_detail_view, name='post_detail'),
    path('create/', views.post_create_view, name='post_create'),
    path('update/<int:pk>/', views.post_update_view, name='post_update'),
    path('delete/<int:pk>/', views.post_delete_view, name='post_delete'),
]
