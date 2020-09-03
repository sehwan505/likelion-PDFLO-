from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib import auth
from .models import Account

#중복
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
#import json
#from django.http import HttpResponse, JsonResponse
#from django.views import View


# Create your views here.

def signup(request):
    if request.method == 'POST':
        #user_id = request.POST.get('id')
        pw1 = request.POST.get('password1')
        pw2 = request.POST.get('password2')
        email = request.POST.get('email')
        nickname = request.POST.get('nickname')

        #if user_id =="" or nickname =="" or email =="" or pw1 == "" or pw2 == "":
        if nickname =="" or email =="" or pw1 == "" or pw2 == "":
            messages.info(request, "모든 항목을 채워주세요")
            return redirect('signup')

        if not pw1 == pw2:
            messages.info(request, "비밀번호가 일치하지 않습니다. 다시 입력해주세요.")
            return redirect('signup')


        #이메일 중복 확인
        if Account.objects.filter(email=email):
            messages.info(request, "이미 가입한 이메일입니다.")
            return redirect('signup')
        elif ObjectDoesNotExist:
             #user = User.objects.create_user(username = user_id, password = pw1)
             user = User.objects.create_user(username = email, password = pw1)
             user.save()
             account = Account(user=user, email=email, nickname=nickname)
             account.save()
             return redirect('login')
    return render(request, 'signup.html')        
        
        
        
#        try:
#            user = Account.objects.filter(email=email)
#            messages.info(request, "이미 가입한 이메일입니다.")
#            return redirect('signup')
#        except ObjectDoesNotExist:
#            user = User.objects.create_user(username = user_id, password = pw1)
#            user.save()
#            account = Account(user=user, email=email, nickname=nickname)
#            account.save()
#            return redirect('login')



        #if Account.objects.get(email=email):
        #    messages.error(request, "이미 가입된 이메일입니다.")
        #    return redirect('signup')
        #else:
        #    user = User.objects.create_user(username = user_id, password = pw1)
        #    user.save()
        #    account = Account(user=user, email=email, nickname=nickname)
        #    account.save()
        #    return redirect('login')
#---------------------------------------------------------------------------------------------#
       # if Account.objects.filter(email = 'email').exists():
       #     messages.info(request, "이미 가입한 이메일입니다.")
       #     return redirect('signup')
#----------------------------------------------------------------------------------------------#            
        #user = User.objects.create_user(username = user_id, password = pw1)
        #user.save()
        #account = Account(user=user, email=email, nickname=nickname)
        #account.save()
        #return redirect('login')
    #else:
        #return render(request, 'signup.html')
    


def login(request):
    if request.method == "POST":
        #username = request.POST['id']
        email = request.POST["email"]
        password = request.POST["password"]

        #user = auth.authenticate(request, username=username, password=password)
        user = auth.authenticate(request, username=email, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('home')
        else:
            messages.info(request, "비밀번호가 일치하지 않거나, 가입하지 않은 계정입니다.")
            return redirect('login')
    else:
        return render(request, 'login.html')
    return render(request, 'login.html')

def logout(request):
    auth.logout(request)
    return redirect('home')


