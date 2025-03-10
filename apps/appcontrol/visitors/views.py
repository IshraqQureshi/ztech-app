from django.shortcuts import render, redirect
from django.conf import settings
from . import models
from . import form
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import cv2
import numpy as np
import os

def index(request):
    if request.session.get('user') is None:
        return redirect('/appcontrol/')
    
    user_data = request.session.get('user')    
    
    data = {
        'app_name': settings.APP_NAME,
        'page_name': 'Manage Visitors',
        'template_folder': 'appcontrol/visitors',
        'template_file': 'manage.html',
        'admin_name': user_data['first_name'] + ' ' + user_data['last_name'],
        'admin_image': user_data['user_images_dir'],
    }

    data['visitors'] = models.Visitors.objects.values()
            
    return render(request, data['template_folder'] + '/' + data['template_file'], data)

def add (request):
    if request.session.get('user') is None:
        return redirect('/appcontrol/')
    
    user_data = request.session.get('user')    
    
    data = {
        'app_name': settings.APP_NAME,
        'page_name': 'Add Visitor',
        'template_folder': 'appcontrol/visitors',
        'template_file': 'edit.html',
        'admin_name': user_data['first_name'] + ' ' + user_data['last_name'],
        'admin_image': user_data['user_images_dir'],
    }    

    if request.POST:
        visitor_data = form.VisitorForm(request.POST)        

        data['errors'] = visitor_data.validate()

        if data['errors']:
            data['visitor_data'] = request.POST            

        else:
            # email_subject = 'Welcome on Board!!'
            # html_message = render_to_string('email/appcontrol/employee_welcome.html', 
            # {                               
            #     'full_name': request.POST.get('first_name') + ' ' + request.POST.get('last_name')
            # })
            # plain_message = strip_tags(html_message) 
            # from_email = settings.ADMIN_EMAIL
            # to = request.POST.get('email')
            
            save(request)

            # send_mail(email_subject, plain_message, from_email, [to], html_message=html_message)
            data['success'] = 'Visitor Added Successfully'

    return render(request, data['template_folder'] + '/' + data['template_file'], data)

def edit(request, visitor_id):
    if request.session.get('user') is None:
        return redirect('/appcontrol/')
    
    user_data = request.session.get('user')    

    visitor = models.Visitors.objects.filter(id=visitor_id).values()    
    
    data = {
        'app_name': settings.APP_NAME,
        'page_name': 'Edit Visitor',
        'template_folder': 'appcontrol/visitor',
        'template_file': 'edit.html',
        'admin_name': user_data['first_name'] + ' ' + user_data['last_name'],
        'admin_image': user_data['user_images_dir'],
        'errors': {},
        'visitor_data': visitor[0],        
        'success': None,
    }

    data['form'] = form.VisitorForm(None)

    if request.POST:
        
        visitor_data = form.VisitorForm(request.POST)        

        data['errors'] = visitor_data.validate(edit=True)

        if data['errors']:
            pass
        else:            
            
            save(request, visitor_id==visitor_id)                            

            data['success'] = 'Visitor Update Successfully'            

    return render(request, data['template_folder'] + '/' + data['template_file'], data)

def save(request, visitor_id= None, visitor_image= None):
    
    save_visitor = models.Visitors()

    if visitor_id is not None:
        save_visitor = models.Visitors.objects.get(id=visitor_id)
    
    save_visitor.first_name = request.POST.get('first_name')
    save_visitor.last_name = request.POST.get('last_name')
    save_visitor.email = request.POST.get('email')
    save_visitor.nic_number = request.POST.get('nic_number')
    save_visitor.phone_number = request.POST.get('phone_number')
    save_visitor.address = request.POST.get('address')
    save_visitor.purpose = request.POST.get('purpose')
    save_visitor.want_to = request.POST.get('want_to')

    # print(request.POST)
    save_visitor.save()            

def delete(request, visitor_id): 
    
    visitor_data = models.Visitors.objects.filter(id=visitor_id)

    visitor_data.delete()

    return redirect('/appcontrol/visitors/manage')

@csrf_exempt
def ajax_face(request):
    return JsonResponse({'status': True})

def train_ml(request):
    return redirect('/')
