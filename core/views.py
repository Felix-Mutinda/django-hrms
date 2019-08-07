from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.http import HttpResponse

from .forms import EmployerSignupForm

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
    
    return render(request, 'core/employer_signup.html', {'form': form})

# the employer dashboard
def employer_dashboard(request):
    return render(request, 'core/employer_dashboard.html')