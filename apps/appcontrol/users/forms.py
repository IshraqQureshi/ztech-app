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
            
    def validate(self):
        
        if self.first_name == '':
            self.error['first_name'] = 'First Name is requird'                        
            
        if self.last_name == '':
            self.error['last_name'] = 'Last Name is requird'

        if self.email == '':
            self.error['email'] = 'Email is requird'
            
        if self.phone_num == '':
            self.error['phone_num'] = 'Phone is requird'

        if self.user_name == '':
            self.error['user_name'] = 'User Name is requird'

        if self.nameValidation(self.first_name):
                self.error['first_name'] = 'Only alphabets are required'

        if self.nameValidation(self.last_name):
                self.error['last_name'] = 'Only alphabets are required'
            
        return self.error

    def nameValidation(self, name):
        
        prog = re.match(r"^[a-zA-Z]+$", name)        

        if prog:
            return False
        
        return True