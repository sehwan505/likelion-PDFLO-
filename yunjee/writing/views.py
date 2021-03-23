from django.shortcuts import render, redirect, get_object_or_404
from .models import Blog
from review.models import Review
from login.models import Account
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

def home(request):
    blogs = Blog.objects
    if request.user.is_authenticated:
        now_login = Account.objects.get(user=request.user)
        return render(request, 'mainpage.html', {'blogs': blogs,'account' : now_login})#
    else:
        return render(request, 'mainpage.html', {'blogs': blogs})

def create(request, step):
    if request.method == 'POST':
        if step == 1:
            print(request.POST)
            return render(request, 'inputpage_1.html')
        elif step == 2:
            blog = Blog()
            blog.title = request.POST['title']
            blog.money = request.POST['money']
            blog.one_line = request.POST['one_line']
            blog.page = request.POST['page']
            if request.FILES:
                blog.image = request.FILES['image']
            blog.save()
            return render(request, 'inputpage_2.html', {'blog_id' : blog.id})
        elif step == 3:
            blog = get_object_or_404(Blog, id=request.POST['id'])
            blog.seller = request.POST['seller']
            blog.seller_num = request.POST['seller_num']
            blog.seller_comment = request.POST['seller_comment']
            blog.save()
            return render(request, 'inputpage_3.html', {'blog_id' : blog.id})
        elif step == 4:
            blog = get_object_or_404(Blog, id=request.POST['id'])
            blog.pdf_subject1 = request.POST['pdf_subject1']
            blog.pdf_subject2 = request.POST['pdf_subject2']
            blog.pdf_why1 = request.POST['pdf_why1']
            blog.pdf_why2 = request.POST['pdf_why2']
            blog.pdf_spec1 = request.POST['pdf_spec1']
            blog.pdf_spec2 = request.POST['pdf_spec2']
            blog.save()
            return render(request, 'inputpage_4.html', {'blog_id' : blog.id})
        elif step == 5:
            blog = get_object_or_404(Blog, id=request.POST['id'])
            blog.seller_spec = request.POST['seller_spec']
            blog.seller_story = request.POST['seller_story']
            blog.save()
            return render(request, 'inputpage_5.html', {'blog_id' : blog.id})
        elif step == 6:
            blog = get_object_or_404(Blog, id=request.POST['id'])
            blog.content_list = request.POST['content_list']
            blog.save()
            return render(request, 'inputpage_6.html', {'blog_id' : blog.id})
        #elif step == 7:
         #   blog = get_object_or_404(Blog, id=request.POST['id'])
          #  blog.content_list = request.POST['content_list']
           # blog.save()
            blog = get_object_or_404(Blog, id=request.POST['id'])
            print(blog)
        return redirect('/')
    elif request.method == 'GET':
        return render(request, 'inputpage_1.html')

def detail(request, blog_id):
    blog = Blog()
    reviews = Review.objects.filter(blog=blog_id)
    blog_detail = get_object_or_404(Blog, pk=blog_id)
    blog.count += 1
    blog.save()
    account = Account.objects.get(user=request.user)
    return render(request, 'detail.html', {'blog': blog_detail, 'account': account, 'reviews' : reviews})

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



   

    

