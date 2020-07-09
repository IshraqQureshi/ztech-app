from django.urls import path
from . import views

urlpatterns = [
    path('manage', views.index, name='manage_user_roles'),    
]
