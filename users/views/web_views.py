

import json
import os

from django.shortcuts import render, redirect, reverse, HttpResponse
from users.auth import authenticate, auth_login, auth_logout, login_required
from users import forms

from common.utils import JsonResponse

from common.utils import img_cut, img_changesize
from common.utils import PageBranch

from users.models import User, Group
from users.password_hasher import MD5PasswordHasher

from cadmin.utils import get_filter_obj, get_order_obj


def logout(request):
    auth_logout(request)
    return redirect(reverse('users:login'))


def login(request):
    """
    登陆页面交互函数
    1，GET返回登陆页面
    2，POST验证登陆
    3，如果没有任何一个用户，返回首次注册页面
    4，如果有用户已经登陆直接跳转到index
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
                # 判断session是否有prepath
                jrs.set_success(200, "login success")
                jrs.url = request.session["prepath"]
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
    用户首次登陆函数
    1，GET返回页面
    2，POST验证并注册
    3，如果有1个用户就直接跳到用户登陆页面
    4，如果session里有user直接跳转到index页面

    创建第一个用户时首先创建一个admin的用户组
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
    """修改密码"""
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
            jrs.set_success(200, 'change password success')
            jrs.url = reverse('index')
        return HttpResponse(jrs.set_json_pack())


@login_required(login_url_name="users:login")
def user_setting(request):
    """用户配置"""
    if request.method == "GET":
        id = request.session["user"]["id"]

        user = User.objects.get(id=id)
        setting_form = forms.UserSettingForm(instance=user)
        return render(request, "users/setting.html", {"setting_form": setting_form, "users": user})

    elif request.method == "POST":
        jrs = JsonResponse()
        user_id = request.session["user"]["id"]
        user_obj = User.objects.get(id=user_id)
        setting_form = forms.UserSettingForm(data=request.POST, instance=user_obj)
        # 没有验证成功
        if setting_form.is_valid():

            setting_form.save(request)



        if setting_form.errors:

            errors = setting_form.errors
            jrs.set_error(300,errors)
        else:
            jrs.set_success(200, 'change setting success')
            jrs.url = reverse('index')
        return HttpResponse(jrs.set_json_pack())


@login_required(login_url_name='users:login')
def staff_reg(request):
    if request.method == 'GET':
        form = forms.StaffCreateForm()
        return render(request, 'users/staff_create.html', context=locals())
    else:
        jrs = JsonResponse()

        form = forms.StaffCreateForm(initial=request.POST, data=request.POST)
        print(form.is_valid())
        print(form.errors)
        if form.is_valid():
            form.save()

        if form.errors:
            errors = form.errors
            jrs.set_error(300, errors)
        else:
            jrs.set_success(200, 'staff %s create success' % (form.instance.username))
            jrs.url = reverse('index')

        return HttpResponse(jrs.set_json_pack())

@login_required(login_url_name='users:login')
def staff_list(request):
    model_class = User

    model_class_objs, filter_dict = get_filter_obj(request, model_class)  # 所有筛选后的记录

    model_class_objs = get_order_obj(request, model_class_objs)

    current_page = int(request.GET.get("_p") or "1")
    row_in_page = 7

    pb = PageBranch(current_page, row_in_page, data_list=model_class_objs)
    pb.get_pglist3()
    model_class_objs = pb.get_data_list()

    return render(request, 'users/staff_list.html', locals())

@login_required(login_url_name='users:login')
def head_pic_upload(request):
    '''
    头像图片处理，只做保存，只能传jpg图片
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
    '''本函数用于切割图片'''
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
            jrs.set_success(200,'group %s create success'%form.cleaned_data['groupname'])
            jrs.url = reverse('index')

        return HttpResponse(jrs.set_json_pack())

@login_required(login_url_name='users:login')
def group_list(request):
    if request.method == "GET":
        group_objs = Group.objects.all()
        return render(request, 'users/group_list.html', locals())


