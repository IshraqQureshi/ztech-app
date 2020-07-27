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
            self.phone_num = form_data.get('phone_num')            
            self.password = form_data.get('password')            
            self.confirm_password = form_data.get('confirm_password')
            self.user_images_dir = form_data.get('file_user_image')
            
    def validate(self, edit= False):
                
        if self.first_name == '':
            self.error['first_name'] = 'First Name is requird'
        
        elif self.nameValidation(self.first_name):
            self.error['first_name'] = 'Only alphabets are required'
            
        if self.last_name == '':
            self.error['last_name'] = 'Last Name is requird'
        
        elif self.nameValidation(self.last_name):
                self.error['last_name'] = 'Only alphabets are required'
            
        if self.phone_num == '':
            self.error['phone_num'] = 'Phone is requird'

        elif self.numberValidation(self.phone_num):
            self.error['phone_num'] = 'Only numbers are required'

        if self.user_images_dir == '' and edit == False:
            self.error['user_images_dir'] = 'User Image is required'        

        if len(self.password) <= 5 and len(self.password) >= 1:
            self.error['password'] = 'Password must be atleast 6 characters '

        if self.confirm_password != self.password and self.password != '':
            self.error['confirm_password'] = 'Password does not match'        

        return self.error

    def nameValidation(self, value):
        
        data = re.match(r"^[a-zA-Z]+$", value)        

        if data:
            return False
        
        return True
    
    def numberValidation(self, value):
        
        data = re.match(r"^[0-9]+$", value)        

        if data:
            return False
        
        return True