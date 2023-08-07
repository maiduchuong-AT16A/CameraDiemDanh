from django.contrib import admin
from .models import DataCam
# Register your models here.
class Data_Admin(admin.ModelAdmin):
    list_display = ('Id','name')
    search_fields = ['name']
    list_filter = ('Id','name')
admin.site.register(DataCam,Data_Admin)
