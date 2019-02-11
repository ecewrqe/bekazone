

import json
import os

from django.shortcuts import render, redirect, reverse, HttpResponse
from users.auth import authenticate, auth_login, auth_logout, login_required
from users import forms

from common.utils import JsonResponse

from common.utils import img_cut, img_changesize
from common.utils import PageBranch
from common.utils import LoggerCollection

from users.models import User, Group
from users.password_hasher import MD5PasswordHasher

from cadmin.utils import get_filter_obj, get_order_obj, get_search_obj


def logout(request):
    auth_logout(request)
    return redirect(reverse('users:login'))


def login(request):
    """
    sign in view
    :param request:
    :return:
    """
    user_count = User.objects.count()
    if user_count == 0:
        return redirect(reverse("users:system_init"))
    if request.session.get("users"):
        return redirect(reverse("index"))

    if request.method == "POST":
        jrs = JsonResponse()

        username = request.POST.get('username')
        password = request.POST.get('password')
        rem_me = request.POST.get('rem_me')
        rem_me = True if rem_me == 'true' else False

        form = forms.UserLoginForm(data=request.POST)
        if form.is_valid():
            user = authenticate(username=username, password=password)
            if user:
                auth_login(request, user)
                jrs.set_success(0, "login success")
                if request.session.get("prepath"):
                    jrs.url = request.session["prepath"]
                else:
                    jrs.url = "/"

                print(jrs.url)

                lc = LoggerCollection()
                lc.log_output("info", "account:%s, login success" % username)
                if request.session.get("prepath"):
                    del request.session["prepath"]

            else:
                jrs.set_error(300, {"username": ["username or password is error", ]})
        else:
            jrs.set_error(300, form.errors)

        return HttpResponse(jrs.set_json_pack())
    else:


        form = forms.UserLoginForm()
        return render(request, 'users/login.html', context=locals())


def system_init(request):
    """
    while the system initial, the first apply user
    """
    user_count = User.objects.count()
    if user_count == 1:
        return redirect(reverse("users:login"))

    if request.method == 'GET':
        Group.objects.get_or_create(groupname="admin")
        Group.objects.get_or_create(groupname="normal")
        form = forms.UserFirstCreateForm()
        return render(request, 'users/first_register.html', context=locals())
    else:
        jrs = JsonResponse()
        form_obj = forms.UserFirstCreateForm(initial=request.POST, data=request.POST)

        if form_obj.is_valid():
            lc = LoggerCollection()
            lc.log_output("info", "account:%s, password changed" % username)
            form_obj.save()

        if form_obj.errors:
            errors=form_obj.errors
            jrs.set_error(1, errors)
        else:
            jrs.set_success(0,'admin register success')
            jrs.url = reverse('users:login')
        return HttpResponse(jrs.set_json_pack())


@login_required(login_url_name='users:login')
def change_passwd(request):
    """
    update the new password
    """
    if request.method == 'GET':
        
        return render(request, 'users/change_passwd.html')
    else:
        jrs = JsonResponse()
        form_obj = forms.PasswdChangeForm(initial=request.POST, data=request.POST)
        user_dict = request.session['user']
        if form_obj.is_valid():
            form_obj.save(user_dict)

        if form_obj.errors:
            errors = form_obj.errors
            jrs.set_error(300, errors)
        else:
            jrs.set_success(0, 'change password success')
            jrs.url = reverse('index')
        return HttpResponse(jrs.set_json_pack())

@login_required(login_url_name="users:login")
def setting(request):
    return redirect(reverse("users:user_setting"))

@login_required(login_url_name="users:login")
def user_setting(request):
    """
    user setting page
    """
    if request.method == "GET":
        print(request.session["user"])
        id = request.session["user"]["id"]

        user = User.objects.get(id=id)
        setting_form = forms.UserSettingForm(instance=user)
        group_list = Group.objects.all()
        
        return render(request, "users/setting.html", {"setting_form": setting_form, "users": user, "group_list": group_list})

    elif request.method == "POST":
        
        jrs = JsonResponse()
        user_id = request.session["user"]["id"]
        user_obj = User.objects.get(id=user_id)
        setting_form = forms.UserSettingForm(data=request.POST, instance=user_obj)
        
        # comparinent
        if setting_form.is_valid():
            setting_form.save(request)
            

        if setting_form.errors:

            errors = setting_form.errors
            print(errors)
            jrs.set_error(300,errors)
        else:
            jrs.set_success(0, 'change setting success')
            jrs.url = reverse('index')
        return HttpResponse(jrs.set_json_pack())

@login_required(login_url_name='users:login')
def account_reg(request):
    if request.method == 'GET':
        form = forms.AccountCreateForm()

        return render(request, 'users/account_create.html', context=locals())
    else:
        jrs = JsonResponse()

        form = forms.AccountCreateForm(initial=request.POST, data=request.POST)
        if form.is_valid():
            form.save()

        if form.errors:
            errors = form.errors
            jrs.set_error(300, errors)
        else:
            jrs.set_success(0, 'account %s create success' % (form.instance.username))
            jrs.url = reverse('users:account-list')

        return HttpResponse(jrs.set_json_pack())

@login_required(login_url_name='users:login')
def account_list(request):
    if request.method == "GET":
        model_class = User

        model_class_objs, filter_dict = get_filter_obj(request, model_class)
        model_class_objs, search_keyword = get_search_obj(request, model_class_objs, ("username",))

        model_class_objs = get_order_obj(request, model_class_objs)

        current_page = int(request.GET.get("_p") or "1")
        row_in_page = 7

        pb = PageBranch(current_page, row_in_page, data_list=model_class_objs)
        pb.get_pglist3()
        model_class_objs = pb.get_data_list()
        return render(request, 'users/account_list.html', locals())
    else:
        check_list = request.POST.get("check_list")

        check_list = json.loads(check_list)
        ul = ""

        for check in check_list:
            us01 = User.objects.get(id=check)
            ul += us01.username+","
            user_obj = User.objects.filter(id=check).delete()
            

        jrs = JsonResponse()
        jrs.set_success(0, 'user:%s delete' % (ul))
        jrs.url = "/users/account-list/"
        return HttpResponse(jrs.set_json_pack())

    

@login_required(login_url_name='users:login')
def head_pic_upload(request):
    '''
    /head-pic/?filename=a2993902752ec4ea5ce301efaf38cdba.jpg&size=128
    :param request:
    :return:
    '''
    if request.method == "POST":
        pic_upload = request.FILES.get("pic_upload")
        username = request.session['user']['username']
        custom_pic_dir = "static/custom_files/head_pics/%s" % username
        try:
            os.makedirs(custom_pic_dir)
        except OSError:
            pass
        pic_init = os.path.splitext(pic_upload.name)[1].strip(".")
        pic_name = MD5PasswordHasher.encoding(pic_upload.name)
        custom_pic_path = "%s/%s.%s" % (custom_pic_dir, pic_name, pic_init)

        with open(custom_pic_path, "wb") as f:
            for chunk in pic_upload.chunks():
                f.write(chunk)


        return HttpResponse("%s.%s" % (pic_name, pic_init))
    else:
        filename = request.GET.get("filename")
        username = request.session['user']['username']
        custom_pic_dir = "static/custom_files/head_pics/%s" % username
        custom_pic_path = "%s/%s" % (custom_pic_dir, filename)
        img = img_cut(custom_pic_path)
        for i in (256, 128, 64):
            stream = img_changesize(img, (i, i))
            custom_pic_path_temp = "%s/%s-%s" % (custom_pic_dir, filename, i)
            with open(custom_pic_path_temp, "wb") as fp:
                fp.write(stream.getvalue())
        jrs = JsonResponse()
        jrs.set_success(200, "")
        jrs.url = "/%s/%s-%s" % (custom_pic_dir, filename, 256)
        return HttpResponse(jrs.set_json_pack())

@login_required(login_url_name='users:login')
def get_head_pic(request):
    """
    the current function to cut a picture
    """
    size = int(request.GET.get("size"))
    filename = request.GET.get("filename")
    username = request.session['user']['username']
    custom_pic_dir = "static/custom_files/head_pics/%s" % username
    custom_pic_path = "%s/%s" % (custom_pic_dir, filename)

    img = img_cut(custom_pic_path)
    stream = img_changesize(img, (size, size))
    hrsp = HttpResponse(stream.getvalue())
    hrsp["Content-Type"] = "image/jpeg"
    return hrsp

@login_required(login_url_name='users:login')
def group_create(request):
    if request.method == "GET":
        form = forms.GroupCreateForm()
        return render(request, 'users/group_create.html', locals())

    else:
        form = forms.GroupCreateForm(data=request.POST)
        if form.is_valid():
            form.save()
        jrs = JsonResponse()
        if form.errors:
            jrs.set_error(300,form.errors)
        else:
            jrs.set_success(0,'group %s create success'%form.cleaned_data['groupname'])
            jrs.url = reverse('users:group-list')

        return HttpResponse(jrs.set_json_pack())

@login_required(login_url_name='users:login')
def group_list(request):
    if request.method == "GET":
        group_objs = Group.objects.all()
        group_list = []
        for group in group_objs:
            group_ucount = User.objects.filter(group_id=group.id).count()
            group_list.append({
                "group_id": group.id,
                "groupname": group.groupname,
                "group_ucount": group_ucount
                })
        print(group_list)
        return render(request, 'users/group_list.html', locals())
    else:
        check_list = request.POST.get("check_list")
        check_list = json.loads(check_list)

        for check in check_list:
            print(check)
            g_obj = Group.objects.get(id=check)
            Group.objects.filter(id=check).delete()

        jrs = JsonResponse()
        jrs.set_success(0,"delete success")
        jrs.url = "/users/group-list/"
        return HttpResponse(jrs.set_json_pack())


