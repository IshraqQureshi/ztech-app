from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.index, name="index"),
    
    path('appcontrol/', include('apps.authentication.urls')),
    path('appcontrol/dashboard', include('apps.appcontrol.dashboard.urls')),
    path('appcontrol/users/', include('apps.appcontrol.users.urls')),
    path('appcontrol/user-roles/', include('apps.appcontrol.userroles.urls')),  
    path('appcontrol/myprofile/', include('apps.appcontrol.user_profile.urls')),
    path('appcontrol/employees/', include('apps.appcontrol.employees.urls')),
    path('appcontrol/visitors/', include('apps.appcontrol.visitors.urls')),
    path('appcontrol/attendance/', include('apps.appcontrol.attendance.urls')),

    path('frontend/', include('apps.frontend.fingerVerification.urls')),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
