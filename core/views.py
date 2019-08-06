from django.shortcuts import render

def home(request):
    '''
    handles requests to the home page.
    '''
    return render(request, 'core/home.html')