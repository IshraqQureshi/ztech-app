from django.shortcuts import render, redirect
from django.conf import settings
from . import models
from . import form
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import time
import busio
from digitalio import DigitalInOut, Direction
import adafruit_fingerprint
import serial

def index(request):
    if request.session.get('user') is None:
        return redirect('/appcontrol/')
    
    user_data = request.session.get('user')    
    
    data = {
        'app_name': settings.APP_NAME,
        'page_name': 'Manage Employees',
        'template_folder': 'appcontrol/employees',
        'template_file': 'manage.html',
        'admin_name': user_data['first_name'] + ' ' + user_data['last_name'],
        'admin_image': user_data['user_images_dir'],
    }

    data['employees'] = models.Employees.objects.filter(status=1).values()
            
    return render(request, data['template_folder'] + '/' + data['template_file'], data)

def add (request):
    if request.session.get('user') is None:
        return redirect('/appcontrol/')
    
    user_data = request.session.get('user')    
    
    data = {
        'app_name': settings.APP_NAME,
        'page_name': 'Add Employees',
        'template_folder': 'appcontrol/employees',
        'template_file': 'edit.html',
        'admin_name': user_data['first_name'] + ' ' + user_data['last_name'],
        'admin_image': user_data['user_images_dir'],
    }    

    if request.POST:
        employee_data = form.EmployeeForm(request.POST)        

        data['errors'] = employee_data.validate()

        if data['errors']:
            data['employee_data'] = request.POST            

        else:
            email_subject = 'Welcome on Board!!'
            html_message = render_to_string('email/appcontrol/employee_welcome.html', 
            {                               
                'full_name': request.POST.get('first_name') + ' ' + request.POST.get('last_name')
            })
            plain_message = strip_tags(html_message) 
            from_email = settings.ADMIN_EMAIL
            to = request.POST.get('email')
            
            save(request)

            send_mail(email_subject, plain_message, from_email, [to], html_message=html_message)
            data['success'] = 'Employee Added Successfully'

    return render(request, data['template_folder'] + '/' + data['template_file'], data)

def edit(request, employee_id):
    if request.session.get('user') is None:
        return redirect('/appcontrol/')
    
    user_data = request.session.get('user')    

    employee = models.Employees.objects.filter(id=employee_id).values()    
    
    data = {
        'app_name': settings.APP_NAME,
        'page_name': 'Edit User',
        'template_folder': 'appcontrol/employees',
        'template_file': 'edit.html',
        'admin_name': user_data['first_name'] + ' ' + user_data['last_name'],
        'admin_image': user_data['user_images_dir'],
        'errors': {},
        'employee_data': employee[0],        
        'success': None,
    }

    data['form'] = form.EmployeeForm(None)

    if request.POST:
        
        employee_data = form.EmployeeForm(request.POST)        

        data['errors'] = employee_data.validate(edit=True)

        if data['errors']:
            pass
        else:            
            
            save(request, employee_id==employee_id)                            

            data['success'] = 'Employee Update Successfully'            

    return render(request, data['template_folder'] + '/' + data['template_file'], data)

def save(request, employee_id= None, employee_image= None):
    
    save_employee = models.Employees()

    if employee_id is not None:
        save_employee = models.Employees.objects.get(id=employee_id)
    
    save_employee.first_name = request.POST.get('first_name')
    save_employee.last_name = request.POST.get('last_name')
    save_employee.email = request.POST.get('email')
    save_employee.nic_number = request.POST.get('nic_number')
    save_employee.phone_number = request.POST.get('phone_number')
    save_employee.address = request.POST.get('address')
    save_employee.designation = request.POST.get('designation')
    save_employee.department_id = request.POST.get('department_id')
    save_employee.fingerprint_1 = request.POST.get('fingerprint_1')
    save_employee.fingerprint_2 = request.POST.get('fingerprint_1')
    save_employee.status = request.POST.get('status')    

    # print(request.POST)
    save_employee.save()            

def delete(request, employee_id): 
    
    employee_data = models.Employees.objects.filter(id=employee_id)

    employee_data.delete()

    return redirect('/appcontrol/employees/manage')

@csrf_exempt
def ajax_fingerprint(request):    
    
    
    for i in range(1, 127):                
        checkfingerprint = models.Employees.objects.filter(fingerprint_1=i).values()
        if checkfingerprint.exists() == False:
            fingerprint_id = i
            break
            
    enroll_finger(request, fingerprint_id)

    response = {'fingerprint_id': fingerprint_id}
    return JsonResponse(response)

def enroll_finger(request, location):
    
    uart = serial.Serial("/dev/ttyUSB0", baudrate=57600, timeout=1)
    finger = adafruit_fingerprint.Adafruit_Fingerprint(uart)

    
    print("Place finger on sensor...", end="", flush=True)    

    while True:
        i = finger.get_image()
        if i == adafruit_fingerprint.OK:
            print("Image taken")
            break
        if i == adafruit_fingerprint.NOFINGER:
            print(".", end="", flush=True)
        elif i == adafruit_fingerprint.IMAGEFAIL:
            print("Imaging error")
            return False
        else:
            print("Other error")
            return False

    print("Templating...", end="", flush=True)
    i = finger.image_2_tz(1)
    if i == adafruit_fingerprint.OK:
        print("Templated")
    else:
        if i == adafruit_fingerprint.IMAGEMESS:
            print("Image too messy")
        elif i == adafruit_fingerprint.FEATUREFAIL:
            print("Could not identify features")
        elif i == adafruit_fingerprint.INVALIDIMAGE:
            print("Image invalid")
        else:
            print("Other error")
        return False

    
    print("Remove finger")
    time.sleep(1)
    while i != adafruit_fingerprint.NOFINGER:
        i = finger.get_image()

    print("Creating model...", end="", flush=True)
    i = finger.create_model()
    print(adafruit_fingerprint.OK)
    if i == adafruit_fingerprint.OK:
        print("Created")
    else:
        if i == adafruit_fingerprint.ENROLLMISMATCH:
            print("Prints did not match")
        else:
            print("Other error")
            return False

    print("Storing model #%d..." % location, end="", flush=True)
    i = finger.store_model(location)
    if i == adafruit_fingerprint.OK:
        print("Stored")
    else:
        if i == adafruit_fingerprint.BADLOCATION:
            print("Bad storage location")
        elif i == adafruit_fingerprint.FLASHERR:
            print("Flash storage error")
        else:
            print("Other error")
        return False

    return True
