from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib import auth
from login.models import Account


# Create your views here.

def home(request):
    if request.user.is_authenticated:
        now_login = Account.objects.get(user=request.user)
        return render(request, 'home.html', {'user' : now_login})
    else :
        return render(request, 'home.html')
    
    return render(request, 'home.html')