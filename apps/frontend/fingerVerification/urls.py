from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="start_app"),
    path('finger_print_verification/', views.finger, name="finger_verification"),    
    
]
