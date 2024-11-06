# employee_management/migrations/XXXX_auto_default_values.py
from django.db import migrations

def create_initial_data(apps, schema_editor):
    # Get the models
    Department = apps.get_model('employee_management', 'Departments')
    Designation = apps.get_model('employee_management', 'Designations')
    Branch = apps.get_model('employee_management', 'Branches')

    # Create default Departments
    Department.objects.create(department_name="Sales", department_status="Active")
    Department.objects.create(department_name="Laboratory", department_status="Active")

    # Create default Designations
    Designation.objects.create(designation_name="Worker", designation_status="Active")
    Designation.objects.create(designation_name="Manager", designation_status="Active")

    # Create default Branch
    Branch.objects.create(branch_name="Saudia Branch", branch_location="Saudi Arabia", 
                          branch_contact="000-0000", branch_email="saudia@branch.com", branch_status="Active")

class Migration(migrations.Migration):
    dependencies = [
        # Replace 'XXXX_previous_migration' with the last migration file in employee_management
        ('employee_management', '0006_branches_departments_designations_and_more'),
    ]

    operations = [
        migrations.RunPython(create_initial_data),
    ]
