from django.forms import ModelForm
from django import forms
from . import models
import re

class EmployeeForm(): 
    def __init__(self, form_data):
        
        if form_data is not None:
            
            self.error = {}
            self.first_name = form_data.get('first_name')
            self.last_name = form_data.get('last_name')
            self.email = form_data.get('email')
            self.nic_number = form_data.get('nic_number')
            self.phone_number = form_data.get('phone_number')
            self.address = form_data.get('address')
            self.designation = form_data.get('designation')
            self.department_id = form_data.get('department_id')
            self.image_dir = form_data.get('image_dir')
            self.fingerprint_1 = form_data.get('fingerprint_1')
            self.fingerprint_2 = form_data.get('fingerprint_2')
            self.face_id = form_data.get('face_id')
            self.status = form_data.get('designation')
            
    def validate(self, edit= False):
                
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
            
        if self.nic_number == '':
            self.error['nic_number'] = 'NIC Number is requird'

        elif self.numberValidation(self.nic_number):
            self.error['nic_number'] = 'Only numbers are required'

        if self.phone_number == '':
            self.error['phone_number'] = 'Phone Number is requird'

        elif self.numberValidation(self.phone_number):
            self.error['phone_number'] = 'Only numbers are required'

        if self.address == '':
            self.error['address'] = 'Address is requird'

        if self.designation == '':
            self.error['designation'] = 'Designation is requird'

        if self.department_id == '':
            self.error['department_id'] = 'Department is requird'                
        
        if self.image_dir == '' and edit == False:
            self.error['image_dir'] = 'Employee Images is required'

        if self.fingerprint_1 == '':
            self.error['fingerprint_1'] = 'Fingerprint is required'        
        
        if self.face_id == '':
            self.error['face_id'] = 'Face is required'        

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
        

    def uniqueUserEmail(self, value):

        check_user = models.Employees.objects.filter(email=value).values()        

        if check_user.exists():
            return True
        
        return False    