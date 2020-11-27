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
from apps.appcontrol.visitors.models import Visitors
from apps.appcontrol.attendance.models import Attendace
from datetime import datetime, date
import cv2

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
        'employee_id': employee_id,
        'employee_name': employee_name,
        'punch_in': currentTime.strftime('%H:%M %p'),
        'date': currentDate.strftime("%B %d, %Y"),
        'punch_type': punch_in
    }
    
    return JsonResponse(response)

@csrf_exempt
def face(request):
    faceDetect = cv2.CascadeClassifier(settings.BASE_DIR+'/ml/haarcascade_frontalface_default.xml')

    cam = cv2.VideoCapture(0)
    # creating recognizer
    rec = cv2.face.LBPHFaceRecognizer_create()
    # loading the training data
    rec.read(settings.BASE_DIR+'/ml/recognizer/trainingData.yml')
    getId = 0
    font = cv2.FONT_HERSHEY_SIMPLEX
    userId = 0
    while(True):
        ret, img = cam.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = faceDetect.detectMultiScale(gray, 1.3, 5)
        for(x,y,w,h) in faces:
            cv2.rectangle(img,(x,y),(x+w,y+h), (0,255,0), 2)

            getId,conf = rec.predict(gray[y:y+h, x:x+w]) #This will predict the id of the face

            #print conf;
            if conf<35:
                userId = getId
                cv2.putText(img, "Detected",(x,y+h), font, 2, (0,255,0),2)
            else:
                cv2.putText(img, "Unknown",(x,y+h), font, 2, (0,0,255),2)

            # Printing that number below the face
            # @Prams cam image, id, location,font style, color, stroke

        cv2.imshow("Face",img)        
        if(cv2.waitKey(1) == ord('q')):
            break
        elif(userId != 0):    
            cam.release()
            cv2.destroyAllWindows()                    
            return JsonResponse({'status': True, 'employee_id': userId})    
    cam.release()
    cv2.destroyAllWindows()
    return JsonResponse({'status': False})

@csrf_exempt
def capture(request):
    visitor_count = {}
    try:
        visitor_count = Visitors.objects.latest('id')
        userId = visitor_count.id + 1        
    except:
        visitor_count = 0
        userId = visitor_count + 1
    finally:
        visitor_count = 0
        userId = visitor_count + 1
    
    faceDetect = cv2.CascadeClassifier(settings.BASE_DIR+'/ml/haarcascade_frontalface_default.xml')
    cam = cv2.VideoCapture(0)

    id = userId

    sampleNum = 0

    while(True):
        ret, img = cam.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = faceDetect.detectMultiScale(gray, 1.3, 5)
        for(x,y,w,h) in faces:
            sampleNum = sampleNum+1
            cv2.imwrite(settings.BASE_DIR+'/ml/dataset/user.'+str(id)+'.'+str(sampleNum)+'.jpg', gray[y:y+h,x:x+w])
            cv2.rectangle(img,(x,y),(x+w,y+h), (0,255,0), 2)
            cv2.waitKey(250)
        cv2.imshow("Face",img)
        cv2.waitKey(1)
        if(sampleNum>35):
            break
    cam.release()
    cv2.destroyAllWindows()    

    response = {'face_id': userId}
    return JsonResponse(response)
    