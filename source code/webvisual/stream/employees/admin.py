from django.contrib import admin
from .models import Employees
# Register your models here.
class Employees_Admin(admin.ModelAdmin):
    list_display = ('employees_id','department_id','name','age')
    search_fields = ['name']
    list_filter = ('employees_id','department_id','name','age')
admin.site.register(Employees,Employees_Admin)