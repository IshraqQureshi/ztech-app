from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import time
import busio
from digitalio import DigitalInOut, Direction
import adafruit_fingerprint
import serial
from apps.appcontrol.employees.models import Employees
from apps.appcontrol.attendance.models import Attendace
from datetime import datetime, date


def index(request):
    data = {
        'app_name': settings.APP_NAME,
        'page_name': 'Manage Users',
        'template_folder': 'frontend/home',
        'template_file': 'view.html',        
    }

    return render(request, data['template_folder'] + '/' + data['template_file'], data)


@csrf_exempt
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
        response = {'error': 'Verification Failed'}
        return JsonResponse(response)
    print("Searching...")

    if finger.finger_search() != adafruit_fingerprint.OK:
        print('Finger Not Found')
        response = {'error': 'Verification Failed'}
        return JsonResponse(response)
    
    employees = Employees.objects.filter(fingerprint_1=finger.finger_id).values().first()
        
    
    currentTime = datetime.now()
    currentDate = date.today()
    employee_id = employees['id']
    employee_name = employees['first_name'] + ' ' + employees['last_name']

    save_attendance = Attendace()
    punch_in = True
    save_attendance.punch_in = currentTime
    # print(Attendace.objects.filter(employee_id=employee_id).count())
    # if( Attendace.objects.filter(employee_id=employee_id).count() ):
    #     save_attendance = Attendace.objects.get(employee_id=employee_id)
    #     save_attendance.punch_in = save_attendance['punch_in']
    #     punch_in = False

    save_attendance.employee_id = employee_id
    save_attendance.punch_out = currentTime
    save_attendance.date = currentDate

    save_attendance.save()

    response = {
        'employee_name': employee_name,
        'punch_in': currentTime.strftime('%H:%M %p'),
        'date': currentDate.strftime("%B %d, %Y"),
        'punch_type': punch_in
    }
    
    return JsonResponse(response)