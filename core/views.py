from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.contrib.auth.forms import SetPasswordForm

from .forms import *
from .models import User, Employer, Employee, Asset, AssignedAsset
from .tokens import account_activation_token

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
            user = form.save() # add employer to db with is_active as False
            
            # send employer a accout activation email
            current_site = get_current_site(request)
            subject = 'Activate Employer Account'
            message = render_to_string('registration/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user)
            })
            user.email_user(subject, message, from_email='3mutindafelix@gmail.com')
            
            messages.success(request, 'An accout activation link has been sent to your email: ' + user.email +
                                '. Go to your email and click the link to activate your account.')
            return redirect('core:home')
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
            messages.success(request, "Profile has been updated successfully")
            return redirect('core:employer_profile')
        
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
    

# displays all employees associated with the current user,
# a form to add a new employee and another to change the employee position
def employees_list(request):
    user = request.user
    
    # filter all Employees that belong to me (Employer) i.e user.employer
    employees = Employee.objects.filter(employer=user.employer)
    employees = [e.user for e in employees]
    
    emp_creation_form = EmployeeCreationForm()
    employee_position_edit_form = EmployeePositionChangeForm()
    
    return render(request, 'core/employer/employees.html', {
        'employees': employees,
        'employee_creation_form': emp_creation_form,
        'employee_position_edit_form': employee_position_edit_form
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
    asset_reclaim_form = ReclaimAssetForm()
    
    return render(request, 'core/employer/assets.html', {
        'assets': assets,
        'assigned_assets': l,
        'new_asset_form': new_asset_form,
        'asset_assign_form': asset_assign_form,
        'asset_reclaim_form': asset_reclaim_form
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
            employee = form.save(commit=False)
            employee.is_active = False
            employee.save()
            
            # current user becomes the employer of employee
            Employee.objects.create(
                user = employee,
                employer = request.user.employer
            )
            
            # send employee a account activation email
            current_site = get_current_site(request)
            subject = 'Activate Employee Account'
            message = render_to_string('registration/account_activation_email.html', {
                'user': employee,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(employee.pk)),
                'token': account_activation_token.make_token(employee)
            })
            employee.email_user(subject, message, from_email='3mutindafelix@gmail.com')
            
            messages.success(request, 'Employee '+employee.email+' has been added successfully and an account activation link sent to their email')
            return redirect('core:employee_add')
    else:
        form = EmployeeCreationForm()
            
    return render(request, 'core/employer/employee_add.html', {'employee_creation_form': form})

# edit employee position
def employee_position_edit(request):
    if request.method == 'POST':
        email = request.POST['email']
        employee = User.objects.get(email=email)
        form = EmployeePositionChangeForm(request.POST, instance=employee)
        if form.is_valid():
            # new_position = form.cleaned_data.get('position')
            employee = form.save()
            
            messages.success(request, 'Employee {} position changed to {}'.format(
                                employee.email,
                                employee.position
                            ))
            return redirect('core:employee_position_edit')
    else:
        form = EmployeePositionChangeForm()
    
    return render(request, 'core/employer/employee_position_edit.html', {'employee_position_edit_form': form})


# add company asset
def asset_add(request):
    if request.method == 'POST':
        form = AssetCreationForm(request.POST)
        if form.is_valid():
            # set the owner/employer before save
            form.set_employer(request.user.employer)
            asset = form.save()
            
            messages.success(request, 'Asset ' + asset.asset + ' added successfully.')
            return redirect('core:asset_add')
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
            
            messages.success(request, 'Your profile has been updated.')
            
    return render(request, 'core/employee/profile.html', {'form': form})


# assign an asset to an employee
def asset_assign(request):
    if request.method == 'POST':
        form = AssignAssetForm(request.POST)
        if form.is_valid():
            asset_id = form.cleaned_data.get('asset_id')
            employee_email = form.cleaned_data.get('employee_email')
            
            asset = AssignedAsset.objects.create(
                asset = Asset.objects.get(asset=asset_id),
                employee = User.objects.get(email=employee_email).employee
            )
            
            messages.success(request,
                'Asset ' + asset.asset.asset + ' has been assigned to '+ asset.employee.user.email)
            return redirect('core:asset_assign') # for assigning another asset
    else:
        form = AssignAssetForm()
        
    return render(request, 'core/employer/asset_assign.html', {'asset_assign_form': form})

# reclaim an assigned asset 
def asset_reclaim(request):
    if request.method == 'POST':
        form = ReclaimAssetForm(request.POST)
        if form.is_valid():
            asset_id = form.cleaned_data.get('asset_id')

            assigned_asset = AssignedAsset.objects.get(asset_id=asset_id)
            assigned_asset.delete()
            
            messages.success(request,
                'Asset ' + assigned_asset.asset.asset + ' has been re-claimed from '+ assigned_asset.employee.user.email)
            return redirect('core:asset_reclaim') # for reclaiming another asset
    else:
        form = ReclaimAssetForm()
    
    return render(request, 'core/employer/asset_reclaim.html', {'asset_reclaim_form': form})

# activate account by clicking on activation email link
def activate_account(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        
        if user.is_employer:
            messages.success(request, 'You have successfully confirmed your email. Log in to proceed.')
            return redirect('core:login')
        else:
            messages.info(request, 'Set a password for your Employee account.')
            return redirect('core:employee_set_password', uid=user.id)
    
    # invalid link
    messages.error(request, 'Account activation link is invalid or has expired. Contact system administratior for assistance')
    return redirect('core:home')

# account activation email sent
def account_activation_sent(request):
    return HttpResponse('<p>An activation link has been sent to your Email</p>')


# upon activating account, employee should set password
def employee_set_password(request, uid):
    user = get_object_or_404(User, pk=uid)
    
    if request.method == 'POST':
        form = SetPasswordForm(user, request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            
            messages.success(request, 'Welcome '+user.email+'. Your account is now operational')
            return redirect('core:login_redirect')
    else:
        form = SetPasswordForm(user)
    
    return render (request, 'core/employee/set_password.html', {'set_password_form': form, 'user': user})
