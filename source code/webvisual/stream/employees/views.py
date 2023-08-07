from django.shortcuts import render

# Create your views here.
def get_employees(request, id):
    return render(request, 'employees.html')