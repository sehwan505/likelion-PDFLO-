from django.shortcuts import render, redirect, get_object_or_404
from .models import Blog
from login.models import Account
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

def home(request):
    blogs = Blog.objects
    if request.user.is_authenticated:
        now_login = Account.objects.get(user=request.user)
        return render(request, 'home.html', {'blogs': blogs,'user': now_login})
    else:
        return render(request, 'home.html',{'blogs': blogs})

def create(request):
    if request.method == 'POST':
        blog = Blog()
        blog.title = request.POST['title']
        blog.money = request.POST['money']
        blog.one_line = request.POST['one_line']
        if request.FILES:
            blog.image = request.FILES['image']
        blog.seller = request.POST['seller']
        blog.content = request.POST['content']
        blog.content_list = request.POST['content_list']        
        blog.save()
        return redirect('/blog/' + str(blog.id))
    elif request.method == 'GET':
        return render(request, 'new.html')

def detail(request, blog_id):
    blog = Blog()
    blog_detail = get_object_or_404(Blog, pk=blog_id)
    blog.count += 1
    blog.save()
    account = Account.objects.get(user=request.user)
    return render(request, 'detail.html', {'blog': blog_detail, 'account': account})

def delete(request):
    del_id = request.GET['blogNum']
    blog = Blog.objects.get(id = del_id)
    blog.delete()
    return redirect('/')


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
    return render(request, 'recommend.html', {'blogs':blogs})



   

    

