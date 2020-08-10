from django.shortcuts import render, redirect, get_object_or_404
from .models import Blog
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

def home(request):
    blogs = Blog.objects
    return render(request, 'home.html', {'blogs': blogs})

def create(request):
    if request.method == 'POST':
        blog = Blog()
        blog.title = request.POST['title']
        blog.money = request.POST['money']
        blog.one_line = request.POST['one_line']
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
    return render(request, 'detail.html', {'blog': blog_detail})

def delete(request):
    del_id = request.GET['blogNum']
    blog = Blog.objects.get(id = del_id)
    blog.delete()
    return redirect ('http://127.0.0.1:8000/')




   

    

