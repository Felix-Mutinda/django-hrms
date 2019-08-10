from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.http import HttpResponse

from .forms import EmployerSignupForm, EmployeeCreationForm

from .models import User, Employer, Employee, Asset, AssignedAsset

def home(request):
    '''
    handles requests to the home page.
    '''
    return render(request, 'core/home.html')

# handles employer signup requests
def employer_signup(request):
    if request.method == 'POST':
        form = EmployerSignupForm(request.POST)
        if form.is_valid():
            form.save() # add employer to db
            
            # authenticate and login employer
            email = form.cleaned_data.get('email')
            password1 = form.cleaned_data.get('password1')
            user = authenticate(request, email=email, password=password1)
            if user is not None:
                login(request, user)
                return redirect('core:employer_dashboard')
    else:
        form = EmployerSignupForm()
    
    return render(request, 'core/employer/signup.html', {'form': form})

# the employer dashboard
def employer_dashboard(request):
    return render(request, 'core/employer/dashboard.html')
    
# the employee dashboard
def employee_dashboard(request):
    return render(request, 'core/employee/dashboard.html')

# redirect employer to employer_dashboard and employee to employee_dashboard
def login_redirect(request):
    if request.user.is_employer:
        return redirect('core:employer_dashboard')
    return redirect('core:employee_dashboard')
    

# displays all employees associated with the current user
# and a form to add a new employee.
def employees_list(request):
    user = request.user
    
    # filter all Employees that belong to me (Employer) i.e user.employer
    employees = Employee.objects.filter(employer=user.employer)
    employees = [e.user for e in employees]
    
    emp_creation_form = EmployeeCreationForm()
    
    return render(request, 'core/employer/employees.html', {
        'employees': employees,
        'form': emp_creation_form
    })
    
# displays all assets associated with  the current user
# and a form to add a  new asset.
def employer_assets(request):
    user = request.user
    assets = Asset.objects.filter(employer=user.employer)
    
    return render(request, 'core/employer/assets.html', {'assets': assets})
    

# the current user profile
def employer_profile(request):
    
    return render(request, 'core/employer/profile.html')

# displays a real time notifications page for the current user,
# the notifications are delivered using pusher/channels
def employer_notifications(request):
    
    return render(request, 'core/employer/notifications.html')


# add employee 
def employee_add(request):
    if request.method == 'POST':
        form = EmployeeCreationForm(request.POST)
        if form.is_valid():
            form.save()
            
            # current user becomes the employer
            emp = form.add_employer(request.user.employer)
            
            return HttpResponse('<p>User added successfully</p>')
    else:
        form = EmployeeCreationForm()
            
    return render(request, 'core/employer/employee_add.html', {'form': form})












