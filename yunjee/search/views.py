from django.shortcuts import render
from writing.models import Blog
from django.db.models import Q
from login.models import Account

def searchResult(request):
    blogs = None
    query = None
    if request.GET['q']:
        query = request.GET.get('q')
        blogs = Blog.objects.all().filter(Q(title__contains=query) | Q(content__contains=query) |
        Q(one_line__contains=query) | Q(content_list__contains=query))
    if request.user.is_authenticated:
        now_login = Account.objects.get(user=request.user)
        return render(request, 'search.html', {'query':query, 'blogs':blogs, 'account':now_login})
    else:
        return render(request, 'search.html', {'query': query, 'blogs': blogs})
