from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.urls import reverse
from login.models import Account
from .models import Blog
from blog.models import Blog
# Create your views here.

def home(request):
    blogs = Blog.objects
    if request.user.is_authenticated:
        now_login = Account.objects.get(user=request.user)
        
        return render(request, 'blog/home.html', {'blogs': blogs, 'user' : now_login})

    else :
        return render(request, 'blog/home.html', {'blogs': blogs})


def detail(request, blog_id):
    blog_detail = get_object_or_404(Blog, pk=blog_id)
    account = Account.objects.get(user=request.user)
    return render(request, 'blog/detail.html', {'blog': blog_detail, 'account': account})

def new(request):
    return render(request, 'blog/new.html')

def create(request):
    blog = Blog()
    blog.title = request.GET['title']
    blog.body = request.GET['body']
    blog.pub_date = timezone.datetime.now()
    blog.save()
    return redirect('/blog/' + str(blog.id))

def delete(request):
    del_id = request.GET['blogNum']
    blog = Blog.objects.get(id = del_id)
    blog.delete()
    return redirect('http://127.0.0.1:8000/')

def go_insert(request):
    ins_id = request.GET['blogNum']
    blog = Blog.objects.get(id = ins_id)

    return render(request, 'blog/go_insert.html',{'blog':blog})

def insert(request):
    del_id = request.GET['blogNum']
    blog = Blog.objects.get(id = del_id)
    blog.delete()

    ins_blog = Blog()
    ins_blog.title = request.GET['title']
    ins_blog.body = request.GET['body']
    ins_blog.pub_date = timezone.datetime.now()
    ins_blog.save()
    return redirect('/blog/' + str(ins_blog.id))

# 좋아요 받기

def blog_like(request, blog_id):
    blog = get_object_or_404(Blog, id = blog_id)
    user = request.user
    account = Account.objects.get(user=user)
    check_like_blog= account.like_blog.filter(id=blog_id)

    if check_like_blog.exists():
        account.like_blog.remove(blog)
        blog.like_num -= 1
        blog.save()
    else:
        account.like_blog.add(blog)
        blog.like_num += 1
        blog.save()

    return redirect('detail', blog_id)

# 좋아요 순으로 내림차순 정렬

def recommend(request):
    blogs = Blog.objects.all().order_by('-like_num', '-pub_date')
    return render(request, 'blog/recommend.html', {'blogs':blogs})
