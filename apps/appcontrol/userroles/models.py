from django.db import models

class UserRoles(models.Model):
    role_name = models.CharField('role_name', max_length=100)

