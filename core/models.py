from django.db import models
from django.contrib.auth.models import AbstractUser

# use a custom auth user model to add extra fields
# for both Employer and Employee
class User(AbstractUser):
    # override username and email(unique)
    username = models.CharField(max_length=200, blank=False)
    email = models.EmailField(max_length=200, unique=True, blank=False)
    
    # denotes whether the user is Employer
    is_employer = models.BooleanField(default=False)
    
    # denotes wether the user is Employee
    is_employee = models.BooleanField(default=False)
    
    # role of the user
    position = models.CharField(max_length=200, default=None, blank=True, null=True)
    
    # phone number
    phone_number = models.CharField(max_length=15, blank=False)
    
    # date of birth
    date_of_birth = models.DateField(default=None, blank=True, null=True)
    
    # national ID
    national_id = models.CharField(max_length=15, default=None, blank=True, null=True)
    
    # KRA PIN
    kra_pin = models.CharField(max_length=50, default=None, blank=True, null=True)
    
    # mandatory fields
    REQUIRED_FIELDS = ['username',]
    
    # require the email to be the unique identifier
    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email
        
        
# profile model for fields specific to Employer
class Employer(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True
    )
    
    # company name
    company = models.CharField(max_length=200, default=None, blank=True, null=True)
    
    # number of employees associated with the employer
    number_of_employees  = models.IntegerField(default=0, blank=True, null=True)
    
    def __str__(self):
        return self.user.email + ' for company ' + self.company

# profile model for fields specific to Employee
class Employee(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True
    )
    
    # employee 'belongs' to employer
    employer = models.ForeignKey(Employer, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.user.email

# company assets, owned by the employer
class Asset(models.Model):
    asset = models.CharField(max_length=50, blank=False, primary_key=True)
    employer = models.ForeignKey(Employer, on_delete=models.CASCADE)
    description = models.CharField(max_length=200, blank=False)

# track which asset is owned by which employee
class AssignedAsset(models.Model):
    asset = models.OneToOneField(Asset, on_delete=models.CASCADE)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)






