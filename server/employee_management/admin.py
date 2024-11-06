from django.contrib import admin
from .models import CustomUser, Branches, Departments, Designations , Attendance , DailyWorkReports, ApplicationLeave
# Register your models here.

admin.site.register(CustomUser)
admin.site.register(Branches)
admin.site.register(Departments)
admin.site.register(Designations)
admin.site.register(Attendance)
admin.site.register(DailyWorkReports)  
admin.site.register(ApplicationLeave)

