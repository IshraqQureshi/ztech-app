# Generated by Django 3.0.8 on 2020-11-27 11:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0002_employees_face_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employees',
            name='face_id',
            field=models.IntegerField(default=0, verbose_name='face_id'),
        ),
    ]
