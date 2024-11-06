# Generated by Django 5.1.2 on 2024-11-05 00:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee_management', '0003_remove_customuser_is_staff_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='is_superuser',
            field=models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status'),
        ),
    ]