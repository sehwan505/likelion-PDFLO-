from django.shortcuts import render
from writing.models import Blog
from django.db.models import Q

def searchResult(request):
    blogs = None
    query = None
    if 'q' in request.GET:
        query = request.GET.get('q')
        blogs = Blog.objects.all().filter(Q(title__contains=query) | Q(content__contains=query) |
        Q(one_line__contains=query) | Q(content_list__contains=query))

    return render(request, 'search.html', {'query':query, 'blogs':blogs})