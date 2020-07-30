from django.urls import path, include
from . import views

urlpatterns = [
    path('manage', views.index, name='manage_employee'),
    # path('add', views.add, name='add_employee'),
    # path('edit/<int:employee_id>', views.edit, name='edit_employee'),
    # path('delete/<int:employee_id>', views.delete, name='delete_employee')    
]