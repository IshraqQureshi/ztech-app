from django.urls import path, include
from . import views

urlpatterns = [
    path('manage', views.index, name='manage_users'),
    path('add', views.add, name='add_user'),
    path('edit/<int:user_id>', views.edit, name='edit_user'),
    path('delete/<int:user_id>', views.delete, name='delete_user')    
]
