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
from django.core.files.storage import FileSystemStorage
import cv2
import numpy as np
import os
from PIL import Image

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

def save(request, id= None, employee_image= None):
    
    save_employee = models.Employees()

    if id is not None:
        save_employee = models.Employees.objects.get(id=id)
    
    save_employee.employee_id = request.POST.get('employee_id')
    save_employee.first_name = request.POST.get('first_name')
    save_employee.last_name = request.POST.get('last_name')
    save_employee.email = request.POST.get('email')
    save_employee.nic_number = request.POST.get('nic_number')
    save_employee.phone_number = request.POST.get('phone_number')
    save_employee.address = request.POST.get('address')
    save_employee.designation = request.POST.get('designation')
    save_employee.department_id = request.POST.get('department_id')
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
def ajax_face(request):
    face_id = int(request.POST['face_id'])

    if face_id == 0:
        if models.Employees.objects.exists():
            employee_count = models.Employees.objects.latest('id')
            user_id = employee_count.id + 1
        else:
            user_id = 1
    else:
        user_id = face_id

    face_cascade = cv2.CascadeClassifier(settings.BASE_DIR + '/ml/haarcascade_frontalface_default.xml')

    cam = cv2.VideoCapture(0)

    if not cam.isOpened():
        return JsonResponse({'status': False, 'error': 'Camera not accessible'})

    sample_num = 0
    dataset_path = os.path.join(settings.BASE_DIR, 'ml', 'dataset')

    os.makedirs(dataset_path, exist_ok=True)

    while True:
        ret, frame = cam.read()
        if not ret:
            print("Failed to capture image")
            continue

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # gray = cv2.equalizeHist(gray)  
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

        for (x, y, w, h) in faces:
            face = gray[y:y+h, x:x+w]
            face_resized = cv2.resize(face, (150, 150)) 

            file_name = f"user.{user_id}.{sample_num}.jpg"
            cv2.imwrite(os.path.join(dataset_path, file_name), face_resized)
            sample_num += 1

            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.waitKey(250)

        cv2.imshow("Capturing Faces", frame)
        if cv2.waitKey(1) & 0xFF == ord('q') or sample_num >= 35:
            break

    cam.release()
    cv2.destroyAllWindows()

    response = {'status': True, 'face_id': user_id}
    return JsonResponse(response)


def train_ml(request):
    recognizer = cv2.face.LBPHFaceRecognizer_create()

    dataset_path = settings.BASE_DIR + '/ml/dataset'

    def getImagesWithID(path):
        import glob

        imagePaths = [os.path.join(path,f) for f in os.listdir(path)] 
        faces = []
        Ids = []

        for imagePath in imagePaths:
            try:
                faceImg = Image.open(imagePath).convert('L')
                faceImg = faceImg.resize((150, 150))
                faceNp = np.array(faceImg, 'uint8')

                ID = int(os.path.split(imagePath)[-1].split('.')[1])

                faces.append(faceNp)
                Ids.append(ID)
            except Exception as e:
                print(f"Error processing file {imagePath}: {e}")

            cv2.imshow("training", faceNp)
            cv2.waitKey(10)
        return np.array(Ids), faces

    ids, faces = getImagesWithID(dataset_path)

    if len(ids) == 0 or len(faces) == 0:
        return JsonResponse({'status': False, 'error': 'No valid training data found'})

    recognizer.train(faces, ids)

    recognizer.save(settings.BASE_DIR + '/ml/recognizer/trainingData.yml')

    cv2.destroyAllWindows()
    return redirect('/')
