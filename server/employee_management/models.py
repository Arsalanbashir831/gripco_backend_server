
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self, email, password=None, **extra_fields):

        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)



class Branches(models.Model):
    branch_name = models.CharField(max_length=100)
    branch_location = models.CharField(max_length=100)
    branch_contact = models.CharField(max_length=100)
    branch_email = models.EmailField(max_length=100)
    branch_status = models.CharField(max_length=100)
    branch_created = models.DateTimeField(auto_now_add=True)
    branch_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.branch_name

class Departments(models.Model):
    department_name = models.CharField(max_length=100)
    department_status = models.CharField(max_length=100)
    department_created = models.DateTimeField(auto_now_add=True)
    department_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.department_name
    
class Designations(models.Model):
    designation_name = models.CharField(max_length=100)
    designation_status = models.CharField(max_length=100)
    designation_created = models.DateTimeField(auto_now_add=True)
    designation_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.designation_name


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=100)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    branch = models.ForeignKey(Branches, on_delete=models.CASCADE, null=True, blank=True)
    department = models.ForeignKey(Departments, on_delete=models.CASCADE, null=True, blank=True)
    designation = models.ForeignKey(Designations, on_delete=models.CASCADE, null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    salary = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    objects = CustomUserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']

    def __str__(self):
        return self.email


class ApplicationLeave(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approve', 'Approve'),
        ('rejection', 'Rejection'),
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    leave_reason = models.CharField(max_length=100)
    leave_start_date = models.DateField()
    leave_end_date = models.DateField()
    leave_status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='pending'
    )
    leave_created = models.DateTimeField(auto_now_add=True)
    leave_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.leave_reason



class DailyWorkReports(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    work_title = models.CharField(max_length=100)
    work_description = models.TextField()
    work_created = models.DateTimeField(auto_now_add=True)
    work_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.work_title