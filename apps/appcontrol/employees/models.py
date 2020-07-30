from django.db import models

class Employees(models.Model):
    first_name = models.CharField('first_name', max_length=199)
    last_name = models.CharField('last_name', max_length=199)
    email = models.CharField('email', max_length=199)
    nic_number = models.CharField('nic_number', max_length=199)
    phone_number = models.CharField('phone_number', max_length=199)
    address = models.CharField('address', max_length=199)
    designation = models.CharField('designation', max_length=199)
    department_id = models.IntegerField('department_id')
    image_dir = models.CharField('image_dir', max_length=256)
    fingerprint_1 = models.IntegerField('fingerprint_1')
    fingerprint_2 = models.IntegerField('fingerprint_2')
    status = models.BooleanField('status')
