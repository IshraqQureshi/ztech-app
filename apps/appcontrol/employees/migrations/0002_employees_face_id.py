# Generated by Django 3.0.8 on 2020-11-27 11:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='employees',
            name='face_id',
            field=models.IntegerField(default='null', verbose_name='face_id'),
        ),
    ]