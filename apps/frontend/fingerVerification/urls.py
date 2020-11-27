from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="start_app"),
    path('finger_print_verification/', views.finger, name="finger_verification"),    
    path('face_recognition/', views.face, name="face_recognition"),
    path('face_capture/', views.capture, name="face_capture"),
]
