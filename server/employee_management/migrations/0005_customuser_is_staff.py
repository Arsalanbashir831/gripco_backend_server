# Generated by Django 5.1.2 on 2024-11-05 00:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee_management', '0004_alter_customuser_is_superuser'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='is_staff',
            field=models.BooleanField(default=False),
        ),
    ]
