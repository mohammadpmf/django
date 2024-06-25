from django.urls import path
from . import views

urlpatterns = [
    path('', views.show_data, name='show_data')
]
