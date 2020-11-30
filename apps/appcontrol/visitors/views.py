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
import cv2
import numpy as np

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

    # print(request.POST)
    save_visitor.save()            

def delete(request, visitor_id): 
    
    visitor_data = models.Visitors.objects.filter(id=visitor_id)

    visitor_data.delete()

    return redirect('/appcontrol/visitor/manage')

@csrf_exempt
def ajax_fingerprint(request):    
    
    
    for i in range(1, 127):                
        checkfingerprint = models.Visitors.objects.filter(fingerprint_1=i).values()
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

@csrf_exempt
def ajax_face(request):
    
    face_id = request.POST['face_id']
    
    if int(face_id) == 0:
        visitor_count = models.Visitors.objects.latest('id')
        userId = visitor_count.id + 1        
    else:
        userId = face_id    

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

    response = {'face_id': userId}
    return JsonResponse(response)

def train_ml(request):
    import os
    from PIL import Image

    #Creating a recognizer to train
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    #Path of the samples
    path = settings.BASE_DIR+'/ml/frontend-dataset'

    # To get all the images, we need corresponing id
    def getImagesWithID(path):
        # create a list for the path for all the images that is available in the folder
        # from the path(dataset folder) this is listing all the directories and it is fetching the directories from each and every pictures
        # And putting them in 'f' and join method is appending the f(file name) to the path with the '/'
        imagePaths = [os.path.join(path,f) for f in os.listdir(path)] #concatinate the path with the image name
        #print imagePaths        
        # Now, we loop all the images and store that userid and the face with different image list
        faces = []
        Ids = []
        for imagePath in imagePaths:
            # First we have to open the image then we have to convert it into numpy array
            faceImg = Image.open(imagePath).convert('L') #convert it to grayscale
            # converting the PIL image to numpy array
            # @params takes image and convertion format
            faceNp = np.array(faceImg, 'uint8')
            # Now we need to get the user id, which we can get from the name of the picture
            # for this we have to slit the path() i.e dataset/user.1.7.jpg with path splitter and then get the second part only i.e. user.1.7.jpg
            # Then we split the second part with . splitter
            # Initially in string format so hance have to convert into int format            
            ID = int(os.path.split(imagePath)[-1].split('.')[1]) # -1 so that it will count from backwards and slipt the second index of the '.' Hence id
            # Images
            faces.append(faceNp)
            # Label
            Ids.append(ID)
            #print ID
            cv2.imshow("training", faceNp)
            cv2.waitKey(10)
        return np.array(Ids), np.array(faces)

    # Fetching ids and faces
    ids, faces = getImagesWithID(path)

    #Training the recognizer
    # For that we need face samples and corresponding labels
    recognizer.train(faces, ids)

    # Save the recogzier state so that we can access it later
    recognizer.save(settings.BASE_DIR+'/ml/frontend-recognizer/trainingData.yml')
    cv2.destroyAllWindows()

    return redirect('/')