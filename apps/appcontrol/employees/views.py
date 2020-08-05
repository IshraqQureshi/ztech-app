from django.shortcuts import render, redirect
from django.conf import settings
from . import models
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
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
            
    return render(request, data['template_folder'] + '/' + data['template_file'], data)

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
