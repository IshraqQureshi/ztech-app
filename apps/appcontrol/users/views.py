from django.shortcuts import render, redirect
from django.conf import settings
from apps.authentication.models import Users
from .forms import UserForm

def index(request):
    if request.session.get('user') is None:
        return redirect('/appcontrol/')
    
    user_data = request.session.get('user')
    
    data = {
        'app_name': settings.APP_NAME,
        'page_name': 'Manage User Roles',
        'template_folder': 'appcontrol/users',
        'template_file': 'manage.html',
        'admin_name': user_data['first_name'] + ' ' + user_data['last_name']
    }

    data['users'] = Users.objects.filter(status=1).values()    
            
    return render(request, data['template_folder'] + '/' + data['template_file'], data)

def add(request):
    if request.session.get('user') is None:
        return redirect('/appcontrol/')
    
    user_data = request.session.get('user')
    
    data = {
        'app_name': settings.APP_NAME,
        'page_name': 'Manage User Roles',
        'template_folder': 'appcontrol/users',
        'template_file': 'add.html',
        'admin_name': user_data['first_name'] + ' ' + user_data['last_name']
    }

    data['form'] = UserForm(None)

    if request.POST:
        
        user_data = UserForm(request.POST)        

    return render(request, data['template_folder'] + '/' + data['template_file'], data)