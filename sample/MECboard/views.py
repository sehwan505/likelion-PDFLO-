from django.shortcuts import render, redirect,get_object_or_404
from MECboard.models import Board, Profile
import os
import math
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.utils.http import urlquote
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Q
from MECboard.forms import UserForm, LoginForm, ProfileForm
from django.contrib.auth.models import User
from django.contrib.auth import (authenticate, login as django_login, logout as django_logout, )

UPLOAD_DIR = "C:/Users/sehwa/likelion1/media/media/images/"
login_failure = False
#render_to_response 를 render로 다 바꿔야 함

@csrf_exempt
def list(request):
    try:
        search_option = request.POST["search_option"]
    except:
        search_option = "writer"
    try:
        search = request.POST["search"]
    except:
        search = ""

    if search_option == "all":
        boardCount = Board.objects.filter(Q(writer__contains=search)
                                          | Q(title__contains=search) | Q(content__contains=search)).count()
    elif search_option == "writer":
        boardCount = Board.objects.filter(Q(writer__contains=search)).count()
    elif search_option == "title":
        boardCount = Board.objects.filter(Q(title__contains=search)).count()
    elif search_option == "content":
        boardCount = Board.objects.filter(Q(content__contains=search)).count()

    try:
        start = int(request.GET["start"])
    except:
        start = 0
    page_size = 10
    page_list_size = 10
    end = start + page_size
    total_page = math.ceil(boardCount / page_size)
    current_page = math.ceil((start + 1) / page_size)
    start_page = math.floor((current_page - 1) / page_list_size) \
                 * page_list_size + 1
    end_page = start_page + page_list_size - 1

    if total_page < end_page:
        end_page = total_page
    if start_page >= page_list_size:
        prev_list = (start_page - 2) * page_size
    else:
        prev_list = 0
    if total_page > end_page:
        next_list = end_page * page_size
    else:
        next_list = 0

    if search_option == "all":
        boardList = Board.objects.filter(Q(writer__contains=search)
                                         | Q(title__contains=search) | Q(content__contains=search)).order_by("-idx")[
                    start:end]
    elif search_option == "writer":
        boardList = Board.objects.filter(Q(writer__contains=search)).order_by("-idx")[start:end]
    elif search_option == "title":
        boardList = Board.objects.filter(Q(title__contains=search)).order_by("-idx")[start:end]
    elif search_option == "content":
        boardList = Board.objects.filter(Q(content__contains=search)).order_by("-idx")[start:end]

    links = []
    for i in range(start_page, end_page + 1):
        page = (i - 1) * page_size
        links.append("<a href='?start=" + str(page) + "'>" + str(i) + "</a>")

    user = request.user
    if user.is_authenticated:
        profile = Profile.objects.get(user=user)
    else:
        profile = 0
    # if not request.user.is_authenticated:
    #     username = request.user
    #     is_authenticated = request.user.is_authenticated
    # else:
    #     username = request.user.username
    #     is_authenticated = request.user.is_authenticated

    return render(request,"list.html",
                              {"boardList": boardList, "boardCount": boardCount,
                               "search_option": search_option, "search": search,
                               "range": range(start_page - 1, end_page),
                               "start_page": start_page, "end_page": end_page,
                               "page_list_size": page_list_size, "total_page": total_page,
                               "prev_list": prev_list, "next_list": next_list,
                               "links": links, "user" : user, "profile":profile})

@login_required
def write(request):
    writer = Profile.objects.get(user=request.user).nickname
    return render(request,"write.html", {"writer": writer})

@csrf_exempt
@login_required
def insert(request): #글쓰기에서 다양한 정보 받아오고 올리기
    fname = ""
    fsize = 0

    if "file" in request.FILES:
        file = request.FILES["file"]
        print(file)
        fname = file._name
        print(UPLOAD_DIR + fname)
        with open("%s%s" % (UPLOAD_DIR, fname), "wb") as fp:
            for chunk in file.chunks():
                fp.write(chunk)

        fsize = os.path.getsize(UPLOAD_DIR + fname)

    if "thumbnail" in request.FILES:
        file = request.FILES["thumbnail"]
        print(file)
        thumbnail_name = file._name
        print(UPLOAD_DIR + thumbnail_name)
        with open("%s%s" % (UPLOAD_DIR, thumbnail_name), "wb") as fp:
            for chunk in file.chunks():
                fp.write(chunk)

        writer = Profile.objects.get(user=request.user).nickname

        dto = Board(writer=writer,
                    title=request.POST["title"],
                    content=request.POST["content"],
                    filename=fname, filesize=fsize,
                    image_thumbnail=request.FILES["thumbnail"])
        dto.save()
    else:
        writer = Profile.objects.get(user=request.user).nickname
        dto = Board(writer=writer,
                    title=request.POST["title"],
                    content=request.POST["content"],
                    filename=fname, filesize=fsize)
        dto.save()

    id = str(dto.idx)
    return HttpResponseRedirect("detail?idx=" + id)


def download(request): #다운로드 부분
    id = request.GET["idx"]
    dto = Board.objects.get(idx=id)
    path = UPLOAD_DIR + dto.filename
    filename = os.path.basename(path)
    filename = urlquote(filename)
    with open(path, "rb") as file:
        response = HttpResponse(file.read(),
                                content_type="application/octet-stream")
        response["Content-Disposition"] = \
            "attachment;filename*=UTF-8''{0}".format(filename)
        dto.down_up()
        dto.save()
    return response


@csrf_exempt
def detail(request):
    id = request.GET["idx"]
    dto = Board.objects.get(idx=id)
    dto.hit_up()
    dto.save()
    filesize = "%.2f" % (dto.filesize / 1024)
    try:
        search_option = request.POST["array_option"]
    except:
        search_option = "written"

    if(request.user.is_anonymous):
        profile = Profile.objects.get(id=1)
    else:
        profile = Profile.objects.get(user=request.user)

    user = request.user
    return render(request,"detail.html",
                              {"dto": dto, "filesize": filesize,
                               "search_option": search_option, "profile": profile, "user": user})


@csrf_exempt
def update_page(request):
    id = request.POST['idx']
    dto = Board.objects.get(idx=id)
    filesize = "%.2f" % (dto.filesize / 1024)
    username = request.user
    profile = Profile.objects.get(user=request.user)
    return render(request,"update_page.html", {"username": username, "dto": dto, "filesize": filesize,"profile":profile})


@csrf_exempt
def update(request):
    id = request.POST["idx"]
    dto_src = Board.objects.get(idx=id)
    fname = dto_src.filename
    fsize = dto_src.filesize
    if "file" in request.FILES:
        file = request.FILES["file"]
        fname = file._name
        fp = open("%s%s" % (UPLOAD_DIR, fname), "wb")
        for chunk in file.chunks():
            fp.write(chunk)
        fp.close()
        fsize = os.path.getsize(UPLOAD_DIR + fname)

    dto_new = Board(idx=id, writer=request.POST["writer"],
                    title=request.POST["title"], content=request.POST["content"],
                    filename=fname, filesize=fsize, hit=request.POST["hit"],
                    rating=request.POST["rating"], ratings_up=request.POST["ratings_up"],
                    ratings_down=request.POST["ratings_down"])
    dto_new.save()
    return HttpResponseRedirect("detail?idx=" + id)


@csrf_exempt
def delete(request):
    id = request.POST["idx"]
    Board.objects.get(idx=id).delete()
    return redirect("/")


def join(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            new_user = User.objects.create_user(**form.cleaned_data)
            django_login(request, new_user)
            return redirect("/")
        else:
            return render(request,"index.html",
                                      {"msg": "failed to sign up..."})
    else:
        form = UserForm()
    return render(request, "join.html", {"form": form})


def logout(request):
    django_logout(request)
    return redirect("/")


def login_check(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        name = request.POST["username"]
        pwd = request.POST["password"]
        user = authenticate(username=name, password=pwd)
        if user is not None:
            django_login(request, user)
            return redirect("/")
        else:
            return render(request, "login.html", {"form": form, "msg": "failed to login..."})
    else:
        form = LoginForm()
    return render(request, "login.html", {"form": form, "msg": "no error"})

#
# class SocialAccountAdapter(DefaultSocialAccountAdapter):
#     def save_user(self, request, sociallogin, form=None):
#
#         user = super(SocialAccountAdapter, self).save_user(request, sociallogin, form)
#
#         social_app_name = sociallogin.account.provider.upper()
#
#         if social_app_name == "FACEBOOK":
#             User.objects.get_or_create_facebook_user(user_pk=user.pk, extra_data=extra_data)
#
#         elif social_app_name == "KAKAO":
#             User.objects.get_or_create_kakao_user(user_pk=user.pk, extra_data=extra_data)
#
#         elif social_app_name == "GOOGLE":
#             User.objects.get_or_create_google_user(user_pk=user.pk, extra_data=extra_data)

def profile(request):
    profile = Profile.objects.get(user=request.user)

    return render(request,"profile.html",
                              {"profile": profile})


@csrf_exempt
def profile_update(request):
    profile = Profile.objects.get(user=request.user)
    profile_form = ProfileForm(request.POST, request.FILES)
    if profile_form.is_valid():
        profile.nickname = profile_form.cleaned_data['nickname']
        profile.introduction = profile_form.cleaned_data['introduction']
        if profile_form.cleaned_data['profile_photo'] != "media/default.jpg":
            profile.profile_photo = profile_form.cleaned_data['profile_photo']
        profile.save()
        print(profile_form.cleaned_data['profile_photo'])
        return redirect('/profile', {"profile": profile})
    else:
        profile_form = ProfileForm(instance=profile)
    return render(request, 'profile_update.html', {
        'profile_form': profile_form
    })

#pdf를 읽어오는 방법
from io import StringIO
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser

def read_pdf_PDFMINER(pdf_file_path):
    output_string = StringIO()
    with open(pdf_file_path, 'rb') as f:
        parser = PDFParser(f)
        doc = PDFDocument(parser)
        rsrcmgr = PDFResourceManager()
        device = TextConverter(rsrcmgr, output_string, laparams=LAParams())
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        for page in PDFPage.create_pages(doc):
            interpreter.process_page(page)
        print(str(output_string.getvalue()))
    return str(output_string.getvalue())


#텍스트를 pdf로 작성
from fpdf import FPDF
@csrf_exempt
def to_pdf(request):
    print("Aaa")
    content = request.POST["content"]
    title = request.POST["title"]
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=content, ln=1, align="C")
    filename = ("%spdf/%s.pdf" % (UPLOAD_DIR, title))
    pdf.output(filename,"F")

    return HttpResponseRedirect("/")


import pdfkit
def html_to_pdf(request):
    content = request.POST["content"]
    title = request.POST["title"]
    #여기에 콘텐츠를 html로 꾸미는 메소드 작성
    pdfkit.from_file("%shtml/%s" % (UPLOAD_DIR,title),"%spdf/%s" % (UPLOAD_DIR,title))

def writepdf(request):
    return render(request,"write_to_pdf.html")
