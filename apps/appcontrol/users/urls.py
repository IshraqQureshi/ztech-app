from django.urls import path, include
from . import views

urlpatterns = [
    path('manage', views.index, name='manage_users'),
    path('add', views.add, name='add_user'),
]
