from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from apps.appcontrol.employees.models import Employees
from apps.appcontrol.attendance.models import Attendace
from datetime import datetime, date, timedelta
import os
import cv2
import numpy as np
from keras_facenet import FaceNet
import joblib

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
    embedder = FaceNet()
    model_path = os.path.join(settings.BASE_DIR, 'ml/employee_recognition_model.pkl')

    if not os.path.exists(model_path):
        return JsonResponse({'status': False, 'error': 'Model not trained yet'})

    knn = joblib.load(model_path)

    if knn.n_samples_fit_ < knn.n_neighbors:
        return JsonResponse({'status': False, 'error': 'Model has too few samples to make a prediction'})

    faceDetect = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    cam = cv2.VideoCapture(0)

    if not cam.isOpened():
        return JsonResponse({'status': False, 'error': 'Camera not accessible'})

    font = cv2.FONT_HERSHEY_SIMPLEX

    while True:
        ret, img = cam.read()
        if not ret:
            continue

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = faceDetect.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

        employee = None
        for (x, y, w, h) in faces:
            face_region = img[y:y + h, x:x + w]
            face_resized = cv2.resize(face_region, (160, 160))

            embedding = embedder.embeddings(np.expand_dims(face_resized, axis=0))[0]

            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

            distances = knn.kneighbors([embedding], n_neighbors=1)
            predicted_id = knn.predict([embedding])[0]

            if distances[0][0] <= 0.7:
                employee = Employees.objects.get(id=predicted_id)

                cv2.putText(img, f"{employee.first_name} {employee.last_name}", (x, y - 25), font, 0.5, (0, 255, 0), 2)
                cv2.putText(img, f"{employee.employee_id}", (x, y - 10), font, 0.5, (0, 255, 0), 2)
            else:
                cv2.putText(img, "Unknown", (x, y - 10), font, 0.8, (0, 0, 255), 2)

        cv2.imshow("Real-Time Face Recognition", img)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        # elif employee is not None:
        #     cam.release()
        #     cv2.destroyAllWindows()
        #     return JsonResponse({'status': True, 'employee': model_to_dict(employee), 'punch_time': datetime.now().strftime('%H:%M:%S'), 'date': datetime.now().strftime('%Y-%m-%d')})

    cam.release()
    cv2.destroyAllWindows()
    
    return JsonResponse({'status': False, 'message': 'No face detected'})



@csrf_exempt
def mark_attendance(request):    
    id = request.POST.get('id')

    if not id:
        return JsonResponse({'status': False, 'error': 'Employee ID is required'})

    try:
        id = int(id)
    except ValueError:
        return JsonResponse({'status': False, 'error': 'Invalid Employee ID'})

    latest_record = Attendace.objects.filter(id=id).order_by('-punch_in').first()

    if latest_record and not latest_record.punch_out == None:
        latest_record.punch_out = datetime.now().strftime('%H:%M:%S')
        latest_record.save()
        status = "Punched Out"
    else:
        Attendace.objects.create(
            employee_id=id,
            punch_in=datetime.now().strftime('%H:%M:%S'),
            punch_out=None,
            date=date.today()
        )
        status = "Punched In"

    return JsonResponse({'status': True, 'message': f'{status} successfully', 'id': id})

