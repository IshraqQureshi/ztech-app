from django.urls import path, include
from . import views

urlpatterns = [
    path('manage', views.index, name='manage_employee'),
    path('add', views.add, name='add_employee'),
    path('ajax_register_fingerprint/', views.ajax_fingerprint, name='register_fingerprint'),
    path('edit/<int:employee_id>', views.edit, name='edit_employee'),
    path('delete/<int:employee_id>', views.delete, name='delete_employee')    
]