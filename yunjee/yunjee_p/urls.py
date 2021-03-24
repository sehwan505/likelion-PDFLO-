"""yunjee_p URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
import writing.views
import login.views
import review.views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', writing.views.home, name = 'home'),
    path('blog/<int:blog_id>', writing.views.detail, name = 'detail'),
    path('create/<int:step>', writing.views.create, name = 'create'),
    path('delete/', writing.views.delete, name = 'delete'),
    path('signup/', login.views.signup, name='signup'),
    path('login/', login.views.login, name='login'),
    path('logout/', login.views.logout, name='logout'),
    path('accounts/', include('allauth.urls')),
    path('like/<int:blog_id>',writing.views.blog_like, name="like"),
    path('search/', include('search.urls'), name='search'),
    path('profile/',login.views.profile, name="profile"),
    path('profile_update/',login.views.profile_update),
    path('review/', review.views.review, name = 'review'),
    path('delete_review/<review_id>', review.views.delete_review, name='delete_review'),

] + static(settings. MEDIA_URL, document_root=settings.MEDIA_ROOT)