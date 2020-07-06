from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf import settings
from . import models

def index(request):

    if request.session.get('user') is not None:
        return redirect('/appcontrol/dashboard')

    data = {
        'app_name': settings.APP_NAME,
        'template_folder': 'authentication/login',
        'template_file': 'login.html',
        'error': None,
        'username': '',
        'password': '',
    }

    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        post_login = check_login(request, username, password)

        if post_login['status']:
            request.session['user'] = post_login['user'] 
            return redirect('/appcontrol/dashboard')
        else:
            data['error'] = 'Invalid Username or Password'
            data['username'] = username
            data['password'] = password    
    
    return render(request, data['template_folder'] + '/' + data['template_file'], data)


def check_login(request, username, password):
    username = request.POST.get('username')
    password = request.POST.get('password')

    users = models.Users.objects.all()

    login = {
        'status': False
    }

    for user in users.values():
        print(username == user['user_name'] and password == user['password'])
        if username == user['user_name'] and password == user['password']:
            login['status'] = True
            login['user'] = user
            break
        else:
            login['status'] = False
    return login