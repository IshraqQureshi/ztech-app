from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.views.decorators.csrf import csrf_exempt
import time
import busio
from digitalio import DigitalInOut, Direction
import adafruit_fingerprint
import serial
from apps.appcontrol.employees.models import Employees
from apps.appcontrol.visitors.models import Visitors
from apps.appcontrol.attendance.models import Attendace
from datetime import datetime, date, timedelta
import cv2

def index(request):
    data = {
        'app_name': settings.APP_NAME,
        'page_name': 'Face Recognition and Bio-Metric Authentication System',
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
    print('Test', employees)
        
    
    currentTime = (datetime.now() + timedelta(hours=5))
    currentDate = date.today()
    employee_id = employees['id']
    employee_faceId = employees['face_id']
    employee_image = employees['image_dir']
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
        'employee_image': employee_image,
        'employee_faceId': employee_faceId,
        'punch_in': currentTime.strftime('%H:%M %S'),
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
    faceDetect = cv2.CascadeClassifier(settings.BASE_DIR+'/ml/haarcascade_frontalface_default.xml')

    cam = cv2.VideoCapture(0)
    # creating recognizer
    rec = cv2.face.LBPHFaceRecognizer_create()
    # loading the training data
    rec.read(settings.BASE_DIR+'/ml/frontend-recognizer/trainingData.yml')
    getId = 0
    font = cv2.FONT_HERSHEY_SIMPLEX
    userId = 0
    visitor = True

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
                visitor = False


            # Printing that number below the face
            # @Prams cam image, id, location,font style, color, stroke

        cv2.imshow("Face",img)        
        if(cv2.waitKey(1) == ord('q')):
            break
        elif(userId != 0):    
            cam.release()
            cv2.destroyAllWindows()                    
            return JsonResponse({'status': True, 'visitor_id': userId})    
        elif(visitor):
            cam.release()
            cv2.destroyAllWindows()
            return save_face()
        

    cam.release()
    cv2.destroyAllWindows()
    return JsonResponse({'status': False})
    
def save_face():

    visitor_count = Visitors.objects.latest('id')
    userId = visitor_count.id + 1  
    
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
            cv2.imwrite(settings.BASE_DIR+'/ml/frontend-dataset/user.'+str(id)+'.'+str(sampleNum)+'.jpg', gray[y:y+h,x:x+w])
            cv2.rectangle(img,(x,y),(x+w,y+h), (0,255,0), 2)
            cv2.waitKey(250)
        cv2.imshow("Face",img)
        cv2.waitKey(1)
        if(sampleNum>35):
            break
    cam.release()
    cv2.destroyAllWindows()    

    response = {'face_id': userId, 'status': True, 'save': True}
    return JsonResponse(response)

@csrf_exempt
def captue_finger(request):
    
    uart = serial.Serial("/dev/ttyUSB0", baudrate=57600, timeout=1)

    finger = adafruit_fingerprint.Adafruit_Fingerprint(uart)

    """Get a finger print image, template it, and see if it matches!"""
    
    print("Waiting for image...")

    while finger.get_image() != adafruit_fingerprint.OK:
        pass
    print("Templating...")

    if finger.image_2_tz(1) != adafruit_fingerprint.OK:
        print('Finger Not Found')        
        return save_fingerprint()
    print("Searching...")

    if finger.finger_search() != adafruit_fingerprint.OK:
        print('Finger Not Found')        
        return save_fingerprint()
    
    visitor = Visitors.objects.filter(fingerprint_1=finger.finger_id).values().first()
    print('Test', visitor)

    response = {
        'visitor': visitor,
        'status' : True,        
    }
    
    return JsonResponse(response)

def save_fingerprint():    
    
    for i in range(1, 127):                
        checkfingerprint = Visitors.objects.filter(fingerprint_1=i).values()
        if checkfingerprint.exists() == False:
            fingerprint_id = i
            break
            
    enroll_finger(fingerprint_id)

    response = {'fingerprint_id': fingerprint_id, 'save': True, 'status': True}
    return JsonResponse(response)

def enroll_finger(location):
    
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

def store_visitor(request):    

    save_visitor = Visitors()
        
    save_visitor.first_name = request.GET.get('first_name')
    save_visitor.last_name = request.GET.get('last_name')
    save_visitor.email = request.GET.get('email')
    save_visitor.nic_number = request.GET.get('nic_number')
    save_visitor.phone_number = request.GET.get('phone_number')
    save_visitor.address = request.GET.get('address')
    save_visitor.purpose = request.GET.get('purpose')
    save_visitor.want_to = request.GET.get('want_to')
    save_visitor.fingerprint_1 = request.GET.get('fingerprint_1')
    save_visitor.fingerprint_2 = request.GET.get('fingerprint_1')
    save_visitor.face_id = request.GET.get('face_id')    

    # print(request.GET)
    # save_visitor.save()            

    
    email_subject = 'Visitor Notification'
    html_message = render_to_string('email/frontend/visitor_notification.html', 
    {                
        'full_name': request.GET.get('first_name') + ' ' + request.GET.get('last_name'),
        'purpose': request.GET.get('purpose')
    })
    plain_message = strip_tags(html_message) 
    from_email = settings.ADMIN_EMAIL
    to = 'ishraq@yopmail.com'

    # send_mail(email_subject, plain_message, from_email, [to], html_message=html_message)

    data = {
        'app_name': settings.APP_NAME,
        'page_name': 'Face Recognition and Bio-Metric Authentication System',
        'template_folder': 'frontend/thankyou',
        'template_file': 'view.html',        
    }

    return render(request, data['template_folder'] + '/' + data['template_file'], data)

