from django.db import models

class Attendace(models.Model):
    employee_id = models.CharField('employee_id', max_length=199)
    punch_in = models.TimeField('punch_in', auto_now=True)
    punch_out = models.TimeField('punch_out', null=True, blank=True, default=None)
    date = models.DateField('date')

