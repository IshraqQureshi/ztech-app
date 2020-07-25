from django.shortcuts import redirect
from apps.authentication.models import Users
from apps.appcontrol.userroles.models import UserRoles

class UserRoleAuthentication:
    def __init__(self, get_response):
        self.get_response = get_response        

    def __call__(self, request, args_id= False):
        
        response = self.get_response(request)
        user = request.session.get('user')

        user_role_id = user['user_role_id']
        request_url = request.path

        authenticate_urls = self.authenticate_url(user_role_id)
        print(args_id)
        print(authenticate_urls)

        if request_url in authenticate_urls:
            return response
        
        else:
            print('fails')
            return redirect('appcontrol/dashboard')

    def process_view(self, request, view_func, view_args, view_kwargs):
        self.user_id = view_kwargs.get('user_id')

    def authenticate_url(self, role_id):

        if role_id == 1:

            urls = [
                '/appcontrol/',
                '/appcontrol/dashboard',
                '/appcontrol/users/manage',
                '/appcontrol/users/add',                
                '/appcontrol/users/edit/'+str(self.user_id),
                '/appcontrol/users/delete/'+str(self.user_id),                
                '/appcontrol/user-roles/',
            ]

        elif role_id == 2:
            
            urls = [
                '/appcontrol/',
                '/appcontrol/dashboard',                
            ]

        elif role_id == 3:
            
            urls = [
                '/appcontrol/',
                '/appcontrol/dashboard',             
            ]
        
        elif role_id == 4:

            urls = [
                '/appcontrol/',
                '/appcontrol/dashboard',                
            ]

        elif role_id == 5:

            urls = [
                '/appcontrol/',
                '/appcontrol/dashboard',                
            ]
        
        elif role_id == 6:

            urls = [
                '/appcontrol/',
                '/appcontrol/dashboard',                
            ]

        return urls

    
    

    