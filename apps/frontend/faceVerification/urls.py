from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="start_app"),
    path('face_recognition/', views.face, name="face_recognition"),
    path('mark_attendance/', views.mark_attendance, name="mark_attendance"),
]
