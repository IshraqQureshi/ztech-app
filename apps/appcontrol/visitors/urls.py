from django.urls import path, include
from . import views

urlpatterns = [
    path('manage', views.index, name='manage_visitor'),
    path('add', views.add, name='add_visitor'),
    path('ajax_register_fingerprint/', views.ajax_fingerprint, name='register_fingerprint'),
    path('ajax_register_face/', views.ajax_face, name='register_face'),
    path('edit/<int:visitor_id>', views.edit, name='edit_visitor'),
    path('delete/<int:visitor_id>', views.delete, name='delete_visitor'),
    path('train/', views.train_ml, name='train')
]