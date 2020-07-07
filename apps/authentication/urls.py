from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='login'),    
    path('logout', views.logout, name='logout'),
    path('forget_password', views.forget_password, name='forget_password'),
    path('forget_password/<str:forget_password_token>', views.post_forget_password, name='post_forget_password')
]