from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.views.decorators.csrf import csrf_exempt
import time
from apps.appcontrol.employees.models import Employees
from apps.appcontrol.visitors.models import Visitors
from apps.appcontrol.attendance.models import Attendace
from datetime import datetime, date, timedelta
import cv2

def index(request):
    data = {
        'app_name': settings.APP_NAME,
        'page_name': 'Face Recognition Authentication System',
        'template_folder': 'frontend/home',
        'template_file': 'view.html',        
    }

    return render(request, data['template_folder'] + '/' + data['template_file'], data)


@csrf_exempt
def face(request):
    faceDetect = cv2.CascadeClassifier(settings.BASE_DIR + '/ml/haarcascade_frontalface_default.xml')
    cam = cv2.VideoCapture(0)
    
    if not cam.isOpened():
        return JsonResponse({'status': False, 'error': 'Camera not accessible'})

    # creating recognizer
    rec = cv2.face.LBPHFaceRecognizer_create()
    # loading the training data
    rec.read(settings.BASE_DIR + '/ml/recognizer/trainingData.yml')
    getId = 0
    font = cv2.FONT_HERSHEY_SIMPLEX
    userId = 0

    while True:
        ret, img = cam.read()
        if not ret:
            print("Failed to capture image")
            continue  # Skip processing if frame capture fails

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = faceDetect.detectMultiScale(gray, 1.3, 5)
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

            getId, conf = rec.predict(gray[y:y + h, x:x + w])  # This will predict the id of the face

            if conf < 35:
                userId = getId
                cv2.putText(img, "Detected", (x, y + h), font, 2, (0, 255, 0), 2)
            else:
                cv2.putText(img, "Unknown", (x, y + h), font, 2, (0, 0, 255), 2)

        cv2.imshow("Face", img)
        if cv2.waitKey(1) == ord('q'):
            break
        elif userId != 0:
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
    to = 'salman@yopmail.com'

    # send_mail(email_subject, plain_message, from_email, [to], html_message=html_message)

    data = {
        'app_name': settings.APP_NAME,
        'page_name': 'Face Recognition Authentication System',
        'template_folder': 'frontend/thankyou',
        'template_file': 'view.html',        
    }

    return render(request, data['template_folder'] + '/' + data['template_file'], data)

