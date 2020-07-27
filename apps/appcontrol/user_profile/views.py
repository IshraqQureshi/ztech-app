from django.shortcuts import render, redirect
from django.conf import settings
from apps.authentication.models import Users
from .forms import UserForm
from django.http import HttpResponse
from apps.appcontrol.userroles.models import UserRoles
from django.core.files.storage import FileSystemStorage

def index(request):
    if request.session.get('user') is None:
        return redirect('/appcontrol/')
    
    user_data = request.session.get('user')

    user_data['file_user_image'] = user_data['user_images_dir']

    user = Users.objects.filter(id=user_data['id']).values()
    user_roles = UserRoles.objects.all().values()
    
    data = {
        'app_name': settings.APP_NAME,
        'page_name': 'My Profile',
        'template_folder': 'appcontrol/user_profile',
        'template_file': 'edit.html',
        'admin_name': user_data['first_name'] + ' ' + user_data['last_name'],
        'admin_image': user_data['user_images_dir'],
        'errors': {},
        'user_data': user[0],
        'user_roles': user_roles,
        'success': None,
    }

    if request.POST:
        
        user_data = UserForm(request.POST)

        data['errors'] = user_data.validate(edit=True)

        if data['errors']:
            if 'user_images_dir' in request.FILES:
                data['user_image'] = request.FILES['user_images_dir']
        else:

            user_id = request.POST.get('user_id')
            password = request.POST.get('password') 
            uploaded_file_url = None

            if 'user_images_dir' in request.FILES:
                user_image = request.FILES['user_images_dir']
        
                user_image_dir = 'media/users/' + request.POST['user_name']
                fileSystem = FileSystemStorage(location=user_image_dir)
                filename = fileSystem.save(user_image.name, user_image)
                uploaded_file_url = user_image_dir + '/' + filename

            save(request, user_id=user_id, password= password, user_image=uploaded_file_url)                            

            data['success'] = 'Profile Updated Successfully'

    return render(request, data['template_folder'] + '/' + data['template_file'], data)

def save(request, user_id= None, password= None, user_image= None):
    
    save_user = Users()

    if user_id is not None:
        save_user = Users.objects.get(id=user_id)

    save_user.first_name = request.POST.get('first_name')
    save_user.last_name = request.POST.get('last_name')    
    save_user.phone_num = request.POST.get('phone_num')        

    if password is not None:
        save_user.password = password
    
    if user_image is not None:
        save_user.user_images_dir = user_image

    save_user.save()            
