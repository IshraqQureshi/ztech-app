from django.shortcuts import render, redirect
from django.conf import settings
from apps.authentication.models import Users
from apps.appcontrol.userroles.models import UserRoles
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.http import HttpResponse
from .forms import UserForm
from django.core.files.storage import FileSystemStorage
import random
import string
import os

def index(request):
    if request.session.get('user') is None:
        return redirect('/appcontrol/')
    
    user_data = request.session.get('user')    
    
    data = {
        'app_name': settings.APP_NAME,
        'page_name': 'Manage User Roles',
        'template_folder': 'appcontrol/users',
        'template_file': 'manage.html',
        'admin_name': user_data['first_name'] + ' ' + user_data['last_name'],
        'admin_image': user_data['user_images_dir'],
    }

    data['users'] = Users.objects.filter(status=1).values()
    data['user_roles'] = UserRoles.objects.all().values()
            
    return render(request, data['template_folder'] + '/' + data['template_file'], data)

def add(request):
    if request.session.get('user') is None:
        return redirect('/appcontrol/')
    
    user_data = request.session.get('user')

    user_roles = UserRoles.objects.all().values()
    
    data = {
        'app_name': settings.APP_NAME,
        'page_name': 'Add User',
        'template_folder': 'appcontrol/users',
        'template_file': 'edit.html',
        'admin_name': user_data['first_name'] + ' ' + user_data['last_name'],
        'admin_image': user_data['user_images_dir'],
        'errors': {},
        'user_data': {},
        'success': None,
        'user_roles': user_roles,        
    }

    data['form'] = UserForm(None)

    if request.POST:        

        user_data = UserForm(request.POST)        

        data['errors'] = user_data.validate()

        if data['errors']:
            data['user_data'] = request.POST
            
            if 'user_images_dir' in request.FILES:
                data['user_image'] = request.FILES['user_images_dir']

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
            
            user_image = request.FILES['user_images_dir']
        
            user_image_dir = 'media/users/' + request.POST['user_name']
            fileSystem = FileSystemStorage(location=user_image_dir)
            filename = fileSystem.save(user_image.name, user_image)
            uploaded_file_url = user_image_dir + '/' + filename

            save(request, password=rand_password, user_image=uploaded_file_url)            

            send_mail(email_subject, plain_message, from_email, [to], html_message=html_message)

            data['success'] = 'User Added Successfully'
    
    

    return render(request, data['template_folder'] + '/' + data['template_file'], data)

def edit(request, user_id):
    if request.session.get('user') is None:
        return redirect('/appcontrol/')
    
    user_data = request.session.get('user')

    user_data['file_user_image'] = user_data['user_images_dir']

    user = Users.objects.filter(id=user_id).values()
    user_roles = UserRoles.objects.all().values()
    
    data = {
        'app_name': settings.APP_NAME,
        'page_name': 'Edit User',
        'template_folder': 'appcontrol/users',
        'template_file': 'edit.html',
        'admin_name': user_data['first_name'] + ' ' + user_data['last_name'],
        'admin_image': user_data['user_images_dir'],
        'errors': {},
        'user_data': user[0],
        'user_roles': user_roles,
        'success': None,
    }

    data['form'] = UserForm(None)

    if request.POST:
        
        user_data = UserForm(request.POST)        

        data['errors'] = user_data.validate(edit=True)

        if data['errors']:
            if 'user_images_dir' in request.FILES:
                data['user_image'] = request.FILES['user_images_dir']
        else:            

            uploaded_file_url = None

            if 'user_images_dir' in request.FILES:
                user_image = request.FILES['user_images_dir']
        
                user_image_dir = 'media/users/' + request.POST['user_name']
                fileSystem = FileSystemStorage(location=user_image_dir)
                filename = fileSystem.save(user_image.name, user_image)
                uploaded_file_url = user_image_dir + '/' + filename

            save(request, user_id=user_id, user_image=uploaded_file_url)                            

            data['success'] = 'User Update Successfully'            

    return render(request, data['template_folder'] + '/' + data['template_file'], data)

def save(request, user_id= None, password= None, user_image= None):
    
    save_user = Users()

    if user_id is not None:
        save_user = Users.objects.get(id=user_id)

    save_user.first_name = request.POST.get('first_name')
    save_user.last_name = request.POST.get('last_name')
    save_user.email = request.POST.get('email')
    save_user.phone_num = request.POST.get('phone_num')
    save_user.user_name = request.POST.get('user_name')
    save_user.user_role_id = request.POST.get('user_role_id')
    save_user.status = request.POST.get('status')

    if password is not None:
        save_user.password = password
    
    if user_image is not None:
        save_user.user_images_dir = user_image

    save_user.save()            

def delete(request, user_id): 
    
    user_data = Users.objects.filter(id=user_id)

    user_data.delete()

    return redirect('/appcontrol/users/manage')