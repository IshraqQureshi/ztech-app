from django.db import models

class Users(models.Model):
    first_name = models.CharField('first_name', max_length=199)
    last_name = models.CharField('last_name', max_length=199)
    email = models.CharField('email', max_length=199)
    phone_num = models.CharField('phone_num', max_length=20)
    user_name = models.CharField('user_name', max_length= 100)
    password = models.CharField('password', max_length= 100)
    user_images_dir = models.CharField('user_images_dir', max_length=200)
    finger_print_id = models.CharField('finger_print_id', max_length=100)
    status = models.BooleanField('status')
    forget_password_token = models.CharField('forget_password_token', max_length=256)
    user_role_id = models.IntegerField('user_role_id')