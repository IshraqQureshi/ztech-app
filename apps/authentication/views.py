from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf import settings
from . import models
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import random
import string

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
        print(user['password'])
        if username == user['user_name'] and password == user['password']:
            login['status'] = True
            login['user'] = user
            break
        else:
            login['status'] = False
    return login

def logout(request):
    request.session['user'] = None
    return HttpResponse('Session is Removed, You Are Logout')

def forget_password(request):
    
    data = {
        'app_name': settings.APP_NAME,
        'template_folder': 'authentication/forget_password',
        'template_file': 'forget_password.html',
        'error': None,
        'sucess': None,
        'email': '',
    }

    if request.POST:
        email = request.POST.get('email')

        user_data = models.Users.objects.filter(email=email).values()
        

        if user_data.exists():
            for user in user_data:
                user_email = user['email']
                user_id = user['id']                                

            random_key = string.ascii_lowercase
            forget_password_token = ''.join(random.choice(random_key) for i in range(20))

            update_user = models.Users.objects.get(id=user_id)
            update_user.forget_password_token = forget_password_token            
            update_user.save()

            email_subject = 'Ztech Forget Password'
            html_message = render_to_string('email/appcontrol/forget_password.html', {'forget_password_token': forget_password_token})
            plain_message = strip_tags(html_message) 
            from_email = settings.ADMIN_EMAIL
            to = user_email

            send_mail(email_subject, plain_message, from_email, [to], html_message=html_message)
            
            data['sucess'] = 'Reset Link is sent to your email address'

        else:
            data['error'] = "Email doesn't exist"

    return render(request, data['template_folder'] + '/' + data['template_file'], data)

def post_forget_password(request, forget_password_token):
    
    data = {
        'app_name': settings.APP_NAME,
        'template_folder': 'authentication/reset_password',
        'template_file': 'reset_password.html',
        'error': None,
        'sucess': None,        
        'user_id': None,
    }

    if request.POST:
        password = request.POST.get('password')
        confirm_pass = request.POST.get('confirm_password')
        user_id = request.POST.get('user_id')

        if password == confirm_pass:
            update_user = models.Users.objects.get(id=user_id)
            update_user.password = password
            update_user.save()

            return redirect('/appcontrol/')

        else:
            data['error'] = "Password and Confirm Password doesn't matched"

    token_data = models.Users.objects.filter(forget_password_token=forget_password_token).values()

    if token_data.exists():
        for user_data in token_data:
            data['user_id'] = user_data['id']
    
    else:
        return redirect('/appcontrol/')

    return render(request, data['template_folder'] + '/' + data['template_file'], data)