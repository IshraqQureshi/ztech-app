from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="start_app"),
    path('face_recognition/', views.face, name="face_recognition"),
    path('face_capture/', views.capture, name="face_capture"),
    path('save_visitor/', views.store_visitor, name="store_visitor"),
    path('mark_attendance/', views.mark_attendance, name="mark_attendance"),
]
