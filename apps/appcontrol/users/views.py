from django.shortcuts import render, redirect
from django.conf import settings
from apps.authentication.models import Users
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.http import HttpResponse
from .forms import UserForm
import random
import string

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
        'admin_name': user_data['first_name'] + ' ' + user_data['last_name'],
        'errors': {},
        'user_data': {},
        'success': None,
    }

    data['form'] = UserForm(None)

    if request.POST:
        
        user_data = UserForm(request.POST)        

        data['errors'] = user_data.validate()

        if data['errors']:
            data['user_data'] = request.POST
        else:

            random_key = string.ascii_lowercase
            rand_password = ''.join(random.choice(random_key) for i in range(20))

            email_subject = 'User Verification'
            html_message = render_to_string('email/appcontrol/user_registration.html', 
            {
                'password': rand_password,
                'user_name': request.POST.get('user_name'),
                'full_name': request.POST.get('first_name') + ' ' + request.POST.get('last_name')
            })
            plain_message = strip_tags(html_message) 
            from_email = settings.ADMIN_EMAIL
            to = request.POST.get('email')

            save_user = Users()
            save_user.first_name = request.POST.get('first_name')
            save_user.last_name = request.POST.get('last_name')
            save_user.email = request.POST.get('email')
            save_user.phone_num = request.POST.get('phone_num')
            save_user.user_name = request.POST.get('user_name')
            save_user.password = rand_password
            save_user.status = request.POST.get('status')

            save_user.save()            

            send_mail(email_subject, plain_message, from_email, [to], html_message=html_message)

            data['success'] = 'User Added Successfully'
    
    

    return render(request, data['template_folder'] + '/' + data['template_file'], data)

def delete(request, user_id):
    
    user_data = Users.objects.filter(id=user_id)

    user_data.delete()

    return redirect('/appcontrol/users/manage')