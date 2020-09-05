from django.shortcuts import render
from .models import Review
from login.models import Account
from writing.models import Blog

# Create your views here.

def review(request):   
     
    return render (request, 'review.html')
    




