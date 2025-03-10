from django.shortcuts import render, redirect
from django.conf import settings
from . import models
from . import form
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.files.storage import FileSystemStorage
import cv2
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from keras_facenet import FaceNet
import joblib

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
    user_id = int(request.POST['user_id'])

    try:
        user = models.Employees.objects.get(id=user_id)
    except models.Employees.DoesNotExist:
        return JsonResponse({'status': False, 'error': 'User not found'})

    face_cascade = cv2.CascadeClassifier(settings.BASE_DIR + '/ml/haarcascade_frontalface_employee.xml')
    cam = cv2.VideoCapture(0)

    if not cam.isOpened():
        return JsonResponse({'status': False, 'error': 'Camera not accessible'})

    embedder = FaceNet()
    detected_embedding = None

    frame_count = 0

    while True:
        ret, frame = cam.read()
        if not ret:
            continue

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

        if len(faces) > 0:
            x, y, w, h = faces[0]
            face = frame[y:y+h, x:x+w]
            face_resized = cv2.resize(face, (160, 160))

            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(frame, "Registering Face...", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

            cv2.imshow("Registering Face - Look at the camera", frame)

            frame_count += 1

            if frame_count >= 30:
                detected_embedding = embedder.embeddings(np.expand_dims(face_resized, axis=0))[0]
                break

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    cam.release()
    cv2.destroyAllWindows()

    if detected_embedding is not None:
        user.embedding = detected_embedding.tobytes()
        user.save()

        return JsonResponse({'status': True, 'message': 'Face registered successfully'})

    return JsonResponse({'status': False, 'message': 'No face detected'})




@csrf_exempt
def train_ml(request):
    employees = models.Employees.objects.exclude(embedding=None).values('id', 'embedding')

    if employees.count() < 1:
        return JsonResponse({'status': False, 'error': 'Not enough face embeddings for training'})

    X = []
    y = []

    for employee in employees:
        embedding = np.frombuffer(employee['embedding'], dtype=np.float32)
        X.append(embedding)
        y.append(employee['id'])

    X = np.array(X)
    y = np.array(y)

    n_neighbors = min(1, len(y))
    knn = KNeighborsClassifier(n_neighbors=n_neighbors, metric='euclidean')
    knn.fit(X, y)

    model_path = settings.BASE_DIR + '/ml/employee_recognition_model.pkl'
    joblib.dump(knn, model_path)

    return JsonResponse({'status': True, 'message': 'Model trained successfully with {} samples'.format(len(y))})
