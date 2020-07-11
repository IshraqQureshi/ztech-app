from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('appcontrol/', include('apps.authentication.urls')),
    path('appcontrol/dashboard', include('apps.appcontrol.dashboard.urls')),
    path('appcontrol/users/', include('apps.appcontrol.users.urls')),
    path('appcontrol/user-roles/', include('apps.appcontrol.userroles.urls')),
]
