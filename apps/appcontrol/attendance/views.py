from django.shortcuts import render, redirect
from django.conf import settings
from . import models
import time
from apps.appcontrol.employees.models import Employees

def index(request):
    if request.session.get('user') is None:
        return redirect('/appcontrol/')
    
    user_data = request.session.get('user')    
    
    data = {
        'app_name': settings.APP_NAME,
        'page_name': 'Manage Attendance',
        'template_folder': 'appcontrol/attendance',
        'template_file': 'manage.html',
        'admin_name': user_data['first_name'] + ' ' + user_data['last_name'],
        'admin_image': user_data['user_images_dir'],
    }

    data['attendance'] = models.Attendace.objects.values()
    data['employees'] = Employees.objects.values()
            
    return render(request, data['template_folder'] + '/' + data['template_file'], data)