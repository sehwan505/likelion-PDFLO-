from django.shortcuts import render, redirect, get_object_or_404
from writing.models import Blog
from .models import Review
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
@csrf_exempt
def review(request):    
    if request.method == 'POST':
        blog = Blog.objects.get(id=request.POST['blog'])       
        review = Review (blog= blog)
        review.review_body = request.POST['review_body']
        review.review_user = request.user
        review.save()
        return redirect ('/blog/'+str(review.blog.id))
    else:
        return redirect('home')

def delete_review(request, review_id):
    review = Review.objects.get(id =review_id)
    review.delete()
    return redirect(f'/blog/{review.blog.id}')
