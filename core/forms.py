from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction

from .models import (User, Employer, Asset, AssignedAsset)

# employer signup form
class EmployerSignupForm(UserCreationForm):
    company_name = forms.CharField()
    number_of_employees = forms.IntegerField()
    
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'phone_number', 'password1', 'password2')
    
    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_employer = True
        user.save()
        
        # create employer profile for user
        company = self.cleaned_data.get('company_name')
        no_of_emp = self.cleaned_data.get('number_of_employees')
        employer = Employer.objects.create(
            user=user,
            company=company,
            number_of_employees=no_of_emp
        )
        
        return user
        
# employee creation form.
# the employee profile which has employer_id,
# will be created in the create_employee view
# since we do not have the request object.
class EmployeeCreationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']
    
    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_employee = True
        user.save()
        
        # employee profile omitted.
        # employee = Employer.objects.create(
        #       user = user,
        #       employer = request.user
        # )
