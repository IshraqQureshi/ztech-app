from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
import time
import busio
from digitalio import DigitalInOut, Direction
import adafruit_fingerprint
import serial
from apps.appcontrol.employees.models import Employees

def index(request):
    data = {
        'app_name': settings.APP_NAME,
        'page_name': 'Manage Users',
        'template_folder': 'frontend/home',
        'template_file': 'view.html',        
    }

    return render(request, data['template_folder'] + '/' + data['template_file'], data)



def finger(request):
    
    uart = serial.Serial("/dev/ttyUSB0", baudrate=57600, timeout=1)

    finger = adafruit_fingerprint.Adafruit_Fingerprint(uart)

    """Get a finger print image, template it, and see if it matches!"""
    
    print("Waiting for image...")

    while finger.get_image() != adafruit_fingerprint.OK:
        pass
    print("Templating...")

    if finger.image_2_tz(1) != adafruit_fingerprint.OK:
        print('Finger Not Found')
        return HttpResponse('Finger Not Found')
    print("Searching...")

    if finger.finger_search() != adafruit_fingerprint.OK:
        print('Finger Not Found')
        return HttpResponse('Finger Not Found')
    
    employees = Employees.objects.filter(fingerprint_1=finger.finger_id).values('first_name')    
    return HttpResponse('Welcome '+ employees[0]['first_name'])