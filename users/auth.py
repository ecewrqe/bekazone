
from django.shortcuts import redirect, reverse, resolve_url, render
from django.conf import settings

from common.utils import date_to_string
from bekazone.utils import page_not_found
from users.models import User
from users.password_hasher import SaltMD5PasswordHasher
from users import permissions

import re



def authenticate(**kwargs):
    """
    登陆验证
    authenticate({"username":"example","password":"example123"})
    :param kwargs:
    :return: boolean类型，{1，验证成功;2，验证失败}
    """
    user = User.objects.filter(username=kwargs['username']).first()
    if user:
        hasher = SaltMD5PasswordHasher()
        com_res = hasher.verify(kwargs['password'], user.password)
        if com_res:
            return user
        else:
            return False
    else:
        return False

def auth_login(request, user):
    """
    登陆句柄
    一般在验证后登陆,本质是创建session
    users: Users数据库对象
    """
    user_dict = user.__dict__
    user_dict['birth_date'] = date_to_string(user_dict['birth_date'])
    user_dict['instaff_date'] = date_to_string(user_dict['instaff_date'])
    user_dict["groupname"] = user.group.groupname
    if user_dict["groupname"] == "normal":
        request.session["now_path"] = "/kaoqing/user_detail/"
    else:
        request.session["now_path"] = "/"
    del user_dict['_state']
    del user_dict['_group_cache']
    print(user_dict)
    request.session['user'] = user_dict



    request.session.set_expiry(settings.USER_SESSION_EXPIRED or 300)

def auth_logout(request):
    '''
    登出句柄，本质是删除session
    '''
    if request.session.get('user'):
        del request.session['user']

def login_required(login_url_name='login'):
    """
    1，登陆判定装饰器，判断session有没有该请求的user
    2，在没有的情况下，存储当前path到session，返回登陆页面
    """
    def required(func):
        def inner(request, *args, **kwargs):
            """
            该函数适用于非login的普通函数
            1,如果user没有的情况下，跳转到login
            2,如果数据库一个用户都没有，跳转到system_init
            3,如果以上都有就执行被装饰的函数
            """
            if not request.session.get("user"):
                login_url = reverse(login_url_name)
                prepath = request.path_info
                request.session["prepath"] = prepath
                res = redirect(login_url)
            else:
                user_dict = request.session.get('user')
                username = user_dict["username"]
                groupname = user_dict["groupname"]
                """
                如果path_info没有在permission允许的范围内返回404
                如果该url在白名单中，就通过
                如果该url在黑名单中，不通过
                用户优先组
                当该Url在用户白名单中，直接通过
                当该url不在白名单中，在黑名单中，不通过
                当该url不在用户白名单中也不在用户黑名单中，找组
                
                """
                PERMISSIONS_GROUP = permissions.PERMISSIONS_GROUP
                PERMISSIONS_PERSON = permissions.PERMISSIONS_PERSON
                path_info = request.path_info

                exec_pass = False
                if PERMISSIONS_PERSON["white"]:

                    if PERMISSIONS_PERSON["white"].get(username):
                        for name in PERMISSIONS_PERSON["white"][username]:
                            if path_info == resolve_url(name):
                                res = func(request, *args, **kwargs)
                                return res


                if PERMISSIONS_PERSON["black"] and exec_pass == False:
                    if PERMISSIONS_PERSON["black"].get(username):
                        for name in PERMISSIONS_PERSON["black"][username]:
                            if path_info == resolve_url(name):
                                """404"""
                                return page_not_found(request)


                if PERMISSIONS_GROUP["white"] and exec_pass == False:
                    if PERMISSIONS_GROUP["white"].get(groupname):
                        for name in PERMISSIONS_GROUP["white"][groupname]:
                            if path_info == resolve_url(name):
                                res = func(request, *args, **kwargs)
                                return res

                if PERMISSIONS_GROUP["black"] and exec_pass == False:
                    if PERMISSIONS_GROUP["black"].get(groupname):
                        for name in PERMISSIONS_GROUP["black"][groupname]:
                            if path_info == resolve_url(name):
                                return page_not_found(request)


                res = func(request, *args, **kwargs)
            return res
        return inner
    return required


def save_to_user(**kwargs):
    obj = User(**kwargs)
    obj.save()


