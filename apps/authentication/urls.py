from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('check-login', views.check_login, name='check-login')
]