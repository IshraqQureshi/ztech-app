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
from django.core.files.storage import FileSystemStorage
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

            employee_image = request.FILES['employee_images_dir']
        
            employee_images_dir = 'media/users/' + request.POST.get('first_name')
            fileSystem = FileSystemStorage(location=employee_images_dir)
            filename = fileSystem.save(employee_image.name, employee_image)
            uploaded_file_url = employee_images_dir + '/' + filename
            
            save(request, employee_image=uploaded_file_url)

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
    save_employee.face_id = request.POST.get('face_id')
    save_employee.status = request.POST.get('status')    

    if employee_image is not None:
        save_employee.image_dir = employee_image

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

@csrf_exempt
def ajax_face(request):
    
    face_id = request.POST['face_id']
    
    if int(face_id) == 0:
        employee_count = models.Employees.objects.latest('id')
        userId = employee_count.id + 1        
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

def train_ml(request):
    import os
    from PIL import Image

    #Creating a recognizer to train
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    #Path of the samples
    path = settings.BASE_DIR+'/ml/dataset'

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
    recognizer.save(settings.BASE_DIR+'/ml/recognizer/trainingData.yml')
    cv2.destroyAllWindows()

    return redirect('/')