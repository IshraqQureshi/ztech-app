from django.db import models

class Visitors(models.Model):
    first_name = models.CharField('first_name', max_length=199)
    last_name = models.CharField('last_name', max_length=199)
    email = models.CharField('email', max_length=199)
    nic_number = models.CharField('nic_number', max_length=199)
    phone_number = models.CharField('phone_number', max_length=199)
    address = models.CharField('address', max_length=199)
    purpose = models.CharField('purpose', max_length=199)
    want_to = models.IntegerField('want_to')    
    fingerprint_1 = models.IntegerField('fingerprint_1')
    fingerprint_2 = models.IntegerField('fingerprint_2')
    face_id = models.IntegerField('face_id', default=0)
    
