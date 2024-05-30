from django.urls import path
from . import views


urlpatterns = [
    path('', views.post_list_view, name='posts_list'),
    path('detail/<int:pk>/', views.post_detail_view, name='post_detail'),
]
