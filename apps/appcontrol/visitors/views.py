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
    
    save_visitor.first_name = request.POST.get('first_name')
    save_visitor.last_name = request.POST.get('last_name')
    save_visitor.email = request.POST.get('email')
    save_visitor.nic_number = request.POST.get('nic_number')
    save_visitor.phone_number = request.POST.get('phone_number')
    save_visitor.address = request.POST.get('address')
    save_visitor.purpose = request.POST.get('purpose')
    save_visitor.want_to = request.POST.get('want_to')
    save_visitor.face_id = request.POST.get('face_id')    

    # print(request.POST)
    save_visitor.save()            

def delete(request, visitor_id): 
    
    visitor_data = models.Visitors.objects.filter(id=visitor_id)

    visitor_data.delete()

    return redirect('/appcontrol/visitors/manage')

@csrf_exempt
def ajax_face(request):
    face_id = int(request.POST['face_id'])

    if face_id == 0:
        if models.Visitors.objects.exists():
            visitor_count = models.Visitors.objects.latest('id')
            user_id = visitor_count.id + 1
        else:
            user_id = 1
    else:
        user_id = face_id

    face_cascade = cv2.CascadeClassifier(settings.BASE_DIR + '/ml/haarcascade_frontalface_visitors.xml')

    cam = cv2.VideoCapture(0)

    if not cam.isOpened():
        return JsonResponse({'status': False, 'error': 'Camera not accessible'})

    sample_num = 0
    dataset_path = os.path.join(settings.BASE_DIR, 'ml', 'frontend-dataset')

    os.makedirs(dataset_path, exist_ok=True)

    while True:
        ret, frame = cam.read()
        if not ret:
            print("Failed to capture image")
            continue

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

        for (x, y, w, h) in faces:
            face = gray[y:y+h, x:x+w]
            face_resized = cv2.resize(face, (150, 150)) 

            file_name = f"visitor.{user_id}.{sample_num}.jpg"
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

    dataset_path = settings.BASE_DIR + '/ml/frontend-dataset'

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

    recognizer.save(settings.BASE_DIR + '/ml/frontend-recognizer/trainingData.yml')

    cv2.destroyAllWindows()
    return redirect('/')
