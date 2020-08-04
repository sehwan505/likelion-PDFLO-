from django.shortcuts import render, redirect, render_to_response, get_object_or_404
from MECboard.models import Board, Comment, Profile
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
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score

UPLOAD_DIR = "C:/Users/sehwa/PycharmProjects/MEC/MECboard/media/images"
login_failure = False


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
                                          | Q(title__contains=search) | Q(content__contains=search), Q(is_finished=False)).count()
    elif search_option == "writer":
        boardCount = Board.objects.filter(Q(writer__contains=search), Q(is_finished=False)).count()
    elif search_option == "title":
        boardCount = Board.objects.filter(Q(title__contains=search), Q(is_finished=False)).count()
    elif search_option == "content":
        boardCount = Board.objects.filter(Q(content__contains=search), Q(is_finished=False)).count()

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
                                         | Q(title__contains=search) | Q(content__contains=search), Q(is_finished=False)).order_by("-idx")[
                    start:end]
    elif search_option == "writer":
        boardList = Board.objects.filter(Q(writer__contains=search), Q(is_finished=False)).order_by("-idx")[start:end]
    elif search_option == "title":
        boardList = Board.objects.filter(Q(title__contains=search), Q(is_finished=False)).order_by("-idx")[start:end]
    elif search_option == "content":
        boardList = Board.objects.filter(Q(content__contains=search), Q(is_finished=False)).order_by("-idx")[start:end]

    links = []
    for i in range(start_page, end_page + 1):
        page = (i - 1) * page_size
        links.append("<a href='?start=" + str(page) + "'>" + str(i) + "</a>")

    user = request.user

    # if not request.user.is_authenticated:
    #     username = request.user
    #     is_authenticated = request.user.is_authenticated
    # else:
    #     username = request.user.username
    #     is_authenticated = request.user.is_authenticated

    return render_to_response("list.html",
                              {"boardList": boardList, "boardCount": boardCount,
                               "search_option": search_option, "search": search,
                               "range": range(start_page - 1, end_page),
                               "start_page": start_page, "end_page": end_page,
                               "page_list_size": page_list_size, "total_page": total_page,
                               "prev_list": prev_list, "next_list": next_list,
                               "links": links, "user" : user})

@login_required
def write(request):
    return render_to_response("write.html", {"user": request.user})

@csrf_exempt
@login_required
def insert(request):
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

        dto = Board(writer=request.POST["writer"],
                    title=request.POST["title"],
                    content=request.POST["content"],
                    filename=fname, filesize=fsize,
                    image_thumbnail=request.FILES["thumbnail"])
        dto.save()
    else:
        dto = Board(writer=request.POST["writer"],
                    title=request.POST["title"],
                    content=request.POST["content"],
                    filename=fname, filesize=fsize)
        dto.save()

    id = str(dto.idx)
    return HttpResponseRedirect("detail?idx=" + id)


def download(request):
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
    if search_option == "written":
        commentList = Comment.objects.filter(board_idx=id).order_by("idx")
    elif search_option == "rating":
        commentList = Comment.objects.filter(board_idx=id).order_by("-rating")

    if(request.user.is_anonymous):
        profile = Profile.objects.get(id=1)
    else:
        profile = Profile.objects.get(user=request.user)

    user = request.user
    return render_to_response("detail.html",
                              {"dto": dto, "filesize": filesize, "commentList": commentList,
                               "search_option": search_option, "profile": profile, "user": user})


@csrf_exempt
def update_page(request):
    id = request.POST['idx']
    dto = Board.objects.get(idx=id)
    filesize = "%.2f" % (dto.filesize / 1024)
    username = request.user
    return render_to_response("update_page.html", {"username": username, "dto": dto, "filesize": filesize})


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


@csrf_exempt
def reply_insert(request):
    id = request.POST["idx"]
    vote = request.POST["vote"]
    dto_board = Board.objects.get(idx=id)
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
        dto = Comment(board_idx=id, writer=request.POST["writer"], writer_id=request.POST["writer_id"],
                      content=request.POST["content"], vote=request.POST["vote"], filename=fname, filesize=fsize,
                      image=request.FILES["file"], evidence=request.POST["evidence"])
    else:
        dto = Comment(board_idx=id, writer=request.POST["writer"],writer_id=request.POST["writer_id"],
                      content=request.POST["content"], vote=request.POST["vote"], filename=fname, filesize=fsize,
                      evidence=request.POST["evidence"])
    dto.save()

    if vote == '1' or vote == '2':
        dto_board.rate_up()
    else:
        dto_board.rate_down()
    dto_board.rating = dto_board.ratings_up - dto_board.ratings_down
    dto_board.save()

    return HttpResponseRedirect("detail?idx=" + id)


@csrf_exempt
@login_required
def reply_rating(request):
    cid = request.GET["cid"]
    id = request.GET["idx"]
    cdto = Comment.objects.get(idx=cid)
    dto = Board.objects.get(idx=id)

    post = get_object_or_404(Comment, idx=cid)
    user = request.user
    profile = Profile.objects.get(user=user)
    check_like_post = profile.user_likelist.filter(idx=post.idx)

    if check_like_post.exists():
        profile.user_likelist.remove(post)
        cdto.rating -= 1
        cdto.save()
        if (cdto.evidence == True):
            evidence = Comment.objects.get(evidence=True, idx=cid)
            if evidence.rating == 1:
                if evidence.vote == 1:
                    dto.win_score -= 2;
                elif evidence.vote == 2:
                    dto.win_score -= 1
                elif evidence.vote == 3:
                    dto.win_score += 1
                elif evidence.vote == 4:
                    dto.win_score += 2
            dto.save()

    else:
        profile.user_likelist.add(post)
        cdto.rating += 1
        cdto.save()
        if (cdto.evidence == True):
            evidence = Comment.objects.get(evidence=True, idx=cid)
            if evidence.rating == 1:
                if evidence.vote == 1:
                    dto.win_score += 2;
                elif evidence.vote == 2:
                    dto.win_score += 1
                elif evidence.vote == 3:
                    dto.win_score -= 1
                elif evidence.vote == 4:
                    dto.win_score -= 2
            dto.save()

    if dto.win_score > 3:
        print("찬성 승리")
        dto.is_finished = True
        dto.save()
    elif dto.win_score < -3:
        print("반대 승리")
        dto.is_finished = True
        dto.save()
    # 예전꺼
    # if rate == '1':
    #     cdto.rate_up()
    # else:
    #     cdto.rate_down()
    # cdto.rating = cdto.ratings_up - cdto.ratings_down
    # cdto.save()

    return HttpResponseRedirect("detail?idx=" + id)


@csrf_exempt
def reply_update(request):
    cid = request.POST["cid"]
    id = request.POST["idx"]
    dto_src = Comment.objects.get(idx=cid)
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
    dto_new = Comment(idx=cid, board_idx=id, writer=request.POST["writer"], content=request.POST["content"], writer_Id=request.POST["writer_id"],
                      rating=request.POST["rating"], ratings_up=request.POST["ratings_up"],
                      ratings_down=request.POST["ratings_down"],
                      filename=fname, filesize=fsize, vote=request.POST["vote"], )
    dto_new.save()
    return HttpResponseRedirect("detail?idx=" + id)


@csrf_exempt
def reply_delete(request):
    cid = request.GET["cid"]
    id = request.GET["idx"]
    dto = Board.objects.get(idx=id)
    cdto = Comment.objects.get(idx=cid)
    if cdto.vote == 1:
        dto.ratings_up -= 1
        dto.rating -= 1
    else:
        dto.ratings_down -= 1
        dto.rating += 1
    dto.save()
    cdto.delete()
    return HttpResponseRedirect("detail?idx=" + id)


@csrf_exempt
def reply_update_page(request):
    id = request.GET['cid']
    dto = Comment.objects.get(idx=id)
    filesize = "%.2f" % (dto.filesize / 1024)

    return render_to_response("reply_update_page.html", { "dto": dto, "filesize": filesize})


@csrf_exempt
def evidence_insert(request):
    id = request.GET["idx"]
    user = request.user
    dto = Board.objects.get(idx=id)
    dto.hit_up()
    dto.save()

    filesize = "%.2f" % (dto.filesize / 1024)

    try:
        search_option = request.POST["array_option"]
    except:
        search_option = "written"
    if search_option == "written":
        commentList = Comment.objects.filter(board_idx=id).order_by("idx")
    elif search_option == "rating":
        commentList = Comment.objects.filter(board_idx=id).order_by("-rating")

    if(request.user.is_anonymous):
        profile = Profile.objects.get(id=1)
    else:
        profile = Profile.objects.get(user=request.user)

    return render_to_response("evidence_insert.html",
                              {"dto": dto, "filesize": filesize, "commentList": commentList,
                               "user": user,
                               "search_option": search_option, "profile": profile})


def join(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            new_user = User.objects.create_user(**form.cleaned_data)
            django_login(request, new_user)
            return redirect("/")
        else:
            return render_to_response("index.html",
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


def muchin_learning(request):
    vec = TfidfVectorizer(min_df=2, tokenizer=None, norm='l2')
    df = pd.read_sql_query("select * from rating")
    rf = RandomForestClassifier(n_estimators=50)

    df = df.dropna(subset=['rating'])
    df.index = range(0, len(df))
    reviews_data = df['gaming'].astype(str).tolist()
    reviews_rating = df['rating'].astype(str).tolist()
    train_size = int(round(len(reviews_data) * 0.8))

    x_train = np.array([''.join(data) for data in reviews_data[0:train_size]])
    y_train = np.array([''.join(data) for data in reviews_rating[0:train_size]])

    x_test = np.array([''.join(data) for data in reviews_data[train_size:]])
    y_test = np.array([''.join(data) for data in reviews_rating[train_size:]])

    x_train = vec.fit_transform(x_train)
    x_test = vec.transform(x_test)
    rf.fit(x_train, y_train)
    pred = rf.predict(x_test)


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
    user_commentList = Comment.objects.filter(writer = request.user)
    likeList = Comment.objects.all()


    posts =  Comment.objects.filter(writer=request.user.username)
    for post in posts:
        profile = Profile.objects.get(user=request.user)
        profile.user_commentlist.add(post)

    return render_to_response("profile.html",
                              {"profile": profile, "user_commentList": user_commentList, "likeList": likeList})


@csrf_exempt
def profile_update(request):
    profile = Profile.objects.get(user=request.user)
    user_commentList = Comment.objects.filter(writer=request.user)
    profile_form = ProfileForm(request.POST, request.FILES)
    if profile_form.is_valid():
        profile.nickname = profile_form.cleaned_data['nickname']
        profile.introduction = profile_form.cleaned_data['introduction']
        profile.profile_photo = profile_form.cleaned_data['profile_photo']
        profile.save()
        return redirect('/profile', {"profile": profile, "user_commentList": user_commentList})
    else:
        profile_form = ProfileForm(instance=profile)
    return render(request, 'profile_update.html', {
        'profile_form': profile_form
    })

@csrf_exempt
def finished_dic(request):
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
                                          | Q(title__contains=search) | Q(content__contains=search), Q(is_finished=True)).count()
    elif search_option == "writer":
        boardCount = Board.objects.filter(Q(writer__contains=search), Q(is_finished=True)).count()
    elif search_option == "title":
        boardCount = Board.objects.filter(Q(title__contains=search), Q(is_finished=True)).count()
    elif search_option == "content":
        boardCount = Board.objects.filter(Q(content__contains=search), Q(is_finished=True)).count()

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
                                         | Q(title__contains=search) | Q(content__contains=search), Q(is_finished=True)).order_by("-idx")[
                    start:end]
    elif search_option == "writer":
        boardList = Board.objects.filter(Q(writer__contains=search), Q(is_finished=True)).order_by("-idx")[start:end]
    elif search_option == "title":
        boardList = Board.objects.filter(Q(title__contains=search), Q(is_finished=True)).order_by("-idx")[start:end]
    elif search_option == "content":
        boardList = Board.objects.filter(Q(content__contains=search), Q(is_finished=True)).order_by("-idx")[start:end]

    links = []
    for i in range(start_page, end_page + 1):
        page = (i - 1) * page_size
        links.append("<a href='?start=" + str(page) + "'>" + str(i) + "</a>")

    return render_to_response("finished_dic.html",
                              {"boardList": boardList, "boardCount": boardCount,
                               "search_option": search_option, "search": search,
                               "range": range(start_page - 1, end_page),
                               "start_page": start_page, "end_page": end_page,
                               "page_list_size": page_list_size, "total_page": total_page,
                               "prev_list": prev_list, "next_list": next_list,
                               "links": links })

