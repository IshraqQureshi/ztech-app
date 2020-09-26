from django.db import models

class Attendace(models.Model):
    employee_id = models.CharField('employee_id', max_length=199)
    punch_in = models.TimeField('punch_in')
    punch_out = models.TimeField('punch_out')
    date = models.DateField('date')

