from django.forms import ModelForm
from django import forms
from apps.authentication.models import Users
import re

class UserForm(): 
    def __init__(self, form_data):
        
        if form_data is not None:
            
            self.error = {}
            self.first_name = form_data.get('first_name')
            self.last_name = form_data.get('last_name')
            self.email = form_data.get('email')
            self.phone_num = form_data.get('phone_num')
            self.user_name = form_data.get('user_name')
            self.status = form_data.get('status')
            self.user_images_dir = form_data.get('file_user_image')
            
    def validate(self, edit= False):
        
        print(edit)

        if self.first_name == '':
            self.error['first_name'] = 'First Name is requird'
        
        elif self.nameValidation(self.first_name):
            self.error['first_name'] = 'Only alphabets are required'
            
        if self.last_name == '':
            self.error['last_name'] = 'Last Name is requird'
        
        elif self.nameValidation(self.last_name):
                self.error['last_name'] = 'Only alphabets are required'

        if self.email == '':
            self.error['email'] = 'Email is requird'
        
        elif self.emailVaidation(self.email):
            self.error['email'] = 'Email is not valid'
        
        elif self.uniqueUserEmail(self.email) and edit == False:
            self.error['email'] = 'Email is already taken'
            
        if self.phone_num == '':
            self.error['phone_num'] = 'Phone is requird'

        elif self.numberValidation(self.phone_num):
            self.error['phone_num'] = 'Only numbers are required'

        if self.user_name == '':
            self.error['user_name'] = 'User Name is requird'                

        elif self.uniqueUserName(self.user_name) and edit == False:
            self.error['user_name'] = 'User Name is already taken'

        if self.user_images_dir == '' and edit == False:
            self.error['user_images_dir'] = 'User Image is required'        

        return self.error

    def nameValidation(self, value):
        
        data = re.match(r"^[a-zA-Z]+$", value)        

        if data:
            return False
        
        return True
    
    def emailVaidation(self, value):

        data = re.match(r"^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$", value)

        if data:
            return False
        
        return True
    
    def numberValidation(self, value):
        
        data = re.match(r"^[0-9]+$", value)        

        if data:
            return False
        
        return True
    
    def uniqueUserName(self, value):

        check_user = Users.objects.filter(user_name=value).values()        

        if check_user.exists():
            return True
        
        return False

    def uniqueUserEmail(self, value):

        check_user = Users.objects.filter(email=value).values()        

        if check_user.exists():
            return True
        
        return False    