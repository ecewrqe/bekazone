
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
    to verify the username and password
    authenticate({"username":"example","password":"example123"})
    :return: user object or false
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
    login function, while the verification exact, can use the current function to login, add session

    """
    user_dict = user.__dict__
    
    user_dict['birth_date'] = date_to_string(user_dict['birth_date'])
    user_dict['instaff_date'] = date_to_string(user_dict['instaff_date'])
    user_dict["groupname"] = user.group.groupname
    
    if user_dict["groupname"] == "normal":
        request.session["now_path"] = "/kaoqing/user_detail/"
    else:
        request.session["now_path"] = "/"

    if user_dict.get("_state"):
        del user_dict['_state']
    if user_dict.get("_group_cache"):
        del user_dict['_group_cache']
    print("login:user_dict===", user_dict)
    request.session['user'] = user_dict
    request.session.set_expiry(settings.USER_SESSION_EXPIRED or 300)

def auth_logout(request):
    '''
    delete the user session
    '''
    if request.session.get('user'):
        del request.session['user']

def login_required(login_url_name='login'):
    """
    
    """
    def required(func):
        def inner(request, *args, **kwargs):
            if not request.session.get("user"):
                login_url = reverse(login_url_name)
                prepath = request.path_info
                request.session["prepath"] = prepath
                res = redirect(login_url)
            else:
                user_dict = request.session.get('user')
                username = user_dict["username"]
                groupname = user_dict["groupname"]
                
                
                
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


