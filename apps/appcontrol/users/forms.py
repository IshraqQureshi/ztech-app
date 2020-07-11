from django.forms import ModelForm
from django import forms
from apps.authentication.models import Users

class UserForm(ModelForm):
    class Meta:
        model = Users

        fields = ['first_name', 'last_name', 'email', 'phone_num', 'user_name', 'status']
    
    def clean(self):

        super(UserForm, self).clean()

        first_name = self.cleaned_data.get('first_name')
        last_name = self.cleaned_data.get('last_name')
        email = self.cleaned_data.get('email')
        phone_num = self.cleaned_data.get('phone_num')
        user_name = self.cleaned_data.get('user_name')

        custom_errors = {}

        print(first_name)
        
        if len(first_name) < 5:
            custom_errors['first_name'] = 'Minimum 5 characters are required'
        
        
        print(custom_errors)
        return custom_errors