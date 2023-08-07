from django.contrib import admin
from .models import Department
# Register your models here.
class Department_Admin(admin.ModelAdmin):
    list_display = ('department_id','name')
    search_fields = ['name']
    list_filter = ('department_id','name')
admin.site.register(Department,Department_Admin)
