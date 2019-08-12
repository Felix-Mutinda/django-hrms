from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.http import HttpResponse

from .forms import *

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


# employer profile
def employer_profile(request):
    user = request.user
    form = EmployerProfileForm(request.POST or None, instance=user, initial = {
        'company_name': user.employer.company,
        'number_of_employees': user.employer.number_of_employees
    })
    
    if request.method == 'POST':
        if form.is_valid():
            user = form.save()
            
        # rebind form due to employer profile
        form = EmployerProfileForm(request.POST, instance = user, initial = {
            'company_name': user.employer.company,
            'number_of_employees': user.employer.number_of_employees
        })
        
    return render(request, 'core/employer/profile.html', {'form': form})

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
    
# displays all assets associated with  the current user,
# a form to add a  new asset and another form to assign an asset.
def employer_assets(request):
    user = request.user
    employer_assets = Asset.objects.filter(employer=user.employer)
    all_assigned_assets = AssignedAsset.objects.all() # not effective
    
    assets = [] # build a list of tuples, (asset, employee_assigned_to or None)
    l = [a.asset for a in all_assigned_assets]
    for asset in employer_assets:
        try:
            i = l.index(asset) # if asset is assigned, get it index in l
            assets.append((asset, all_assigned_assets[i].employee))
        except ValueError:
            assets.append((asset, None))
    
    new_asset_form  = AssetCreationForm()
    asset_assign_form = AssignAssetForm()
    
    return render(request, 'core/employer/assets.html', {
        'assets': assets,
        'new_asset_form': new_asset_form,
        'asset_assign_form': asset_assign_form
    })
    

# displays a real time notifications page for the current user,
# the notifications are delivered using pusher/channels
def employer_notifications(request):
    
    return render(request, 'core/employer/notifications.html')


# add employee 
def employee_add(request):
    if request.method == 'POST':
        form = EmployeeCreationForm(request.POST)
        if form.is_valid():
            employee = form.save()
            
            # current user becomes the employer of employee
            Employee.objects.create(
                user = employee,
                employer = request.user.employer
            )
            
            # unbind form for adding another user
            form = EmployeeCreationForm()
            
            # return redirect('core:employer_dashboard')
    else:
        form = EmployeeCreationForm()
            
    return render(request, 'core/employer/employee_add.html', {'form': form})


# add company asset
def asset_add(request):
    if request.method == 'POST':
        form = AssetCreationForm(request.POST)
        if form.is_valid():
            # set the owner/employer before save
            form.set_employer(request.user.employer)
            form.save()
            
            # unbind form for adding another asset
            form = AssetCreationForm()
    else: # GET
        form = AssetCreationForm()

    return render(request, 'core/employer/asset_add.html', {'new_asset_form': form})

# display employee assigned asset 
def employee_assigned_assets(request):
    assigned_assets = AssignedAsset.objects.filter(employee=request.user.employee)
    assets = [a.asset for a in assigned_assets]
    
    return render(request, 'core/employee/assigned_assets.html', {'assets': assets})


# employee profile 
def employee_profile(request):
    form = EmployeeProfileForm(request.POST or None, instance=request.user)
    
    if request.method == 'POST':
        if form.is_valid():
            user = form.save()
            
    return render(request, 'core/employee/profile.html', {'form': form})


# assign an asset to an employee
def asset_assign(request):
    if request.method == 'POST':
        form = AssignAssetForm(request.POST)
        if form.is_valid():
            asset_id = form.cleaned_data.get('asset_id')
            employee_email = form.cleaned_data.get('employee_email')
            
            AssignedAsset.objects.create(
                asset = Asset.objects.get(asset=asset_id),
                employee = User.objects.get(email=employee_email).employee
            )
            
            # unbind form
            form = AssignAssetForm()
    else:
        form = AssignAssetForm()
        
    return render(request, 'core/employer/asset_assign.html', {'asset_assign_form': form})

# reclaim an assigned asset 
def asset_reclaim(request):
    pass







