from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request, 'home/index.html')

def register(request):
    return render(request, 'authentication/registerPage.html')

def connection(request):
    return render(request, 'authentication/connectionPage.html')
