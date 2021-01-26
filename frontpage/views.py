import json
import os

from django.shortcuts import render, redirect, reverse, HttpResponse
from users.auth import authenticate, auth_login, auth_logout, login_required
from users.models import User
from users import forms

from common.utils import JsonResponse

from common.utils import img_cut, img_changesize
from common.utils import PageBranch
from common.utils import LoggerCollection

from blog_backend.models import MessageList, BlogKind, Tag, BlogList

from cadmin.utils import get_search_obj
def init_assert(request):
    user_count = User.objects.count()
    print(user_count)
    if user_count == 0:
        return redirect(reverse("users:system_init"))
    if request.session.get("users"):
        return None
def index(request):
    res=init_assert(request)
    if res == None:
        return redirect("/frontpage/")
    else:
        return res

def post_list(request):
    """
    blog list
    """
    res=init_assert(request)
    if res != None:
        return res
    if request.method == "GET":
        bl_obj_list = BlogList.objects.all().order_by("-adjustment_date", "-create_date")
        bk_obj_list = BlogKind.objects.all()
        tag_list = Tag.objects.all()
        tag_sim_list = []
        count = 0

        kind = request.GET.get("_k") # filter blog in kind
        if kind:
            is_back = True
            bl_obj_list = bl_obj_list.filter(blog_kind__name=kind)

        tag = request.GET.get("_t")  # filter blog in tag
        if tag:
            is_back = True
            bl_obj_list = bl_obj_list.filter(tag__name=tag)

        creator = request.GET.get("creator")
        if creator:
            is_back = True
            bl_obj_list = bl_obj_list.filter(creator__username = creator)

        search_handle = request.GET.get("_s")
        search_fields = ["title"]
        print(search_handle)
        if search_handle != "None":
            bl_obj_list, search_handle = get_search_obj(request, bl_obj_list, search_fields)
        else:
            search_handle = ""

        current_page = int(request.GET.get("_p") or "1")
        row_in_page = 7
        pb = PageBranch(current_page, row_in_page, data_list=bl_obj_list)
        pb.get_pglist3()
        bl_obj_list = pb.get_data_list()
        return render(request, 'frontpage/post_list.html', context=locals())

def post_view(request):
    res=init_assert(request)
    if res != None:
        return res
    blog_id = request.GET.get("id")
    bl_obj = BlogList.objects.get(id=blog_id)
    tag_list = bl_obj.tag.all()
    return render(request, "frontpage/post_view.html", locals())
