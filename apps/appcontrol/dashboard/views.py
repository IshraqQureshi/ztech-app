from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf import settings

def index(request):
    
    if request.session.get('user') is None:
        return redirect('/appcontrol/')
    
    user_data = request.session.get('user')
    
    data = {
        'app_name': settings.APP_NAME,
        'page_name': 'Dashboard',
        'template_folder': 'appcontrol/dashboard',
        'template_file': 'dashboard.html',
        'admin_name': user_data['first_name'] + ' ' + user_data['last_name'],
        'admin_image': user_data['user_images_dir'],
    }
            
    return render(request, data['template_folder'] + '/' + data['template_file'], data)
