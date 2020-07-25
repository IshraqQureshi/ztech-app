from django.shortcuts import render, redirect
from django.conf import settings
from . import models

def index(request):
    if request.session.get('user') is None:
        return redirect('/appcontrol/')
    
    user_data = request.session.get('user')
    
    data = {
        'app_name': settings.APP_NAME,
        'page_name': 'Manage User Roles',
        'template_folder': 'appcontrol/userroles',
        'template_file': 'manage.html',
        'admin_name': user_data['first_name'] + ' ' + user_data['last_name'],
        'admin_image': user_data['user_images_dir'],
    }

    data['user_roles'] = models.UserRoles.objects.all().values()    
            
    return render(request, data['template_folder'] + '/' + data['template_file'], data)
