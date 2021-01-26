from django.shortcuts import render, redirect, reverse, HttpResponse
import json
import datetime
from blog_backend.models import MessageList, BlogKind, Tag, BlogList
from common.utils import JsonResponse
from common.utils import PageBranch
from cadmin.utils import get_search_obj
import random
from users.auth import login_required
import os
import mimetypes
import re
from django.utils.encoding import force_text
from django.utils.encoding import DjangoUnicodeDecodeError
from bekazone.settings import BASE_DIR


# Create your views here.
@login_required(login_url_name='users:login')
def edit_blog(request):
    """
    contribute the editor mode
    """
    #return render(request, "blog_backend/edit_blog.html")
    edit_type = request.GET.get("edit_type")
    if edit_type == "message":
        return redirect(reverse("blog_backend:message"))
    elif edit_type == "upload_md":
        return redirect(reverse("blog_backend:upload_markdown"))
    elif edit_type == "md_blog":
        return redirect(reverse("blog_backend:md_edit_blog"))
    else:
        return render(request, "blog_backend/blog_type_sel.html")

@login_required(login_url_name='users:login')
def message(request):
    """
    message mode editor
    """
    if request.method == "GET":
        msg_id = request.GET.get("id")
        if msg_id:
            ml_obj = MessageList.objects.filter(id=msg_id)
        return render(request, "blog_backend/message.html", locals())
    else:
        typ = request.POST.get("typ")
        if typ == "get_content":
            msg_id = request.POST.get("msg_id")
            ml_obj = MessageList.objects.get(id=msg_id)
            jrs = JsonResponse()
            jrs.set_success(0, ml_obj.content)
            return HttpResponse(jrs.set_json_pack())
        else:
            content = request.POST.get("content")
            jrs = JsonResponse()
            users_dict = request.session.get("user")
            userid = users_dict["id"]
            id = request.POST.get("msg_id")
            if id:
                ml_obj = MessageList.objects.get(id=id)
                ml_obj.content = content
                ml_obj.creator_id = userid
                adjustment_date = datetime.datetime.now()
                ml_obj.adjustment_date = adjustment_date
                ml_obj.save()
            else:
                create_date = datetime.datetime.now()
                ml_obj = MessageList()
                ml_obj.content = content
                ml_obj.creator_id = userid
                ml_obj.create_date = create_date
                ml_obj.save()
            jrs.set_success(0, "ok")
        
            jrs.url = "/backend/blog-backend/message-list/";

            return HttpResponse(jrs.set_json_pack())

@login_required(login_url_name='users:login')
def normal_edit_blog(request):
    """
    normal editor(trash)
    """
    if request.method == "GET":
        blog_id = request.GET.get("id")
        if blog_id:

            try:
                bl_obj = BlogList.objects.get(id=blog_id)
            except:
                return redirect("/backend/blog-backend/display-blog-list/")
        bk_obj_list = BlogKind.objects.all()
        tg_obj_list = Tag.objects.all()

        return render(request, "blog_backend/normal_edit_blog.html", locals())
    else:
        typ = request.POST.get("typ")
        
        title = request.POST.get("blog_title")
        content = request.POST.get("content")
        kind_id = request.POST.get("kind_id")
        tag_list = request.POST.get("tag")
        tag_list = tag_list.split(",")
        userid = request.session.get("user")["id"]
        
        if typ == "create":
            bk = BlogList()
            bk.title = title
            bk.blog_content = content
            bk.blog_kind_id = kind_id
            bk.creator_id = userid
            bk.create_date = datetime.datetime.now()
            bk.save()
        else:
            blog_id = request.GET.get("id")
            bk = BlogList.objects.filter(id=blog_id).first()
            if bk:
                bk.title = title
                bk.blog_content = content
                bk.blog_kind_id = kind_id
                bk.creator_id = userid
                bk.create_date = datetime.datetime.now()
                bk.save()
                
            else:
                bk = BlogList()
                bk.title = title
                bk.blog_content = content
                bk.blog_kind_id = kind_id
                bk.creator_id = userid
                bk.adjustment_date = datetime.datetime.now()
                bk.save()

        
        bk.tag.clear()
        for tag in tag_list:
            if tag:
                obj = Tag.objects.get(id=tag)
                bk.tag.add(obj)
        jrs = JsonResponse()
        jrs.set_success(0, "ok")
        jrs.url = "/backend/blog-backend/display-blog-list/";
        return HttpResponse(jrs.set_json_pack())

@login_required(login_url_name='users:login')
def md_edit_blog(request):
    """
    markdown mode editor

    """
    
    if request.method == "GET":
        blog_id = request.GET.get("id")
        if blog_id:

            try:
                bl_obj = BlogList.objects.get(id=blog_id)
            except:
                return redirect("/backend/blog-backend/display-blog-list/")
        bk_obj_list = BlogKind.objects.all()
        tg_obj_list = Tag.objects.all()
        return render(request, "blog_backend/md_edit_blog.html", locals())
    else:
        typ = request.POST.get("typ")
        
        title = request.POST.get("blog_title")
        content = request.POST.get("content")
        kind_id = request.POST.get("kind_id")
        tag_list = request.POST.get("tag")
        tag_list = tag_list.split(",")
        userid = request.session.get("user")["id"]
        if typ == "create":
            bk = BlogList()
            bk.title = title
            bk.blog_content = content
            bk.blog_kind_id = kind_id
            bk.creator_id = userid
            bk.create_date = datetime.datetime.now()
            bk.save()
        else:
            blog_id = request.GET.get("id")
            bk = BlogList.objects.filter(id=blog_id).first()
            if bk:
                bk.title = title
                bk.blog_content = content
                bk.blog_kind_id = kind_id
                bk.creator_id = userid
                bk.create_date = datetime.datetime.now()
                bk.save()
                
            else:
                bk = BlogList()
                bk.title = title
                bk.blog_content = content
                bk.blog_kind_id = kind_id
                bk.creator_id = userid
                bk.adjustment_date = datetime.datetime.now()
                bk.save()

        md_file_name = bk.title
        path = "var/data/blog_files"
        path = os.path.join(BASE_DIR, path)

        tempo_path = os.path.join(path, md_file_name)
        history_file = "%s-%s.md"%(tempo_path, datetime.datetime.now().strftime("%Y-%m-%d"))
        if os.path.exists("%s.md" % tempo_path) and not os.path.exists(history_file):
            os.rename("%s.md" % tempo_path, history_file)
        
        tempo_path = os.path.normpath(tempo_path)
        with open("%s.md" % tempo_path, "wb") as fp:
            fp.write(bytes(bk.blog_content, "utf8"))

        bk.tag.clear()
        for tag in tag_list:
            if tag:
                obj = Tag.objects.get(id=tag)
                bk.tag.add(obj)
        jrs = JsonResponse()
        jrs.set_success(0, "ok")
        jrs.id = bk.id
        jrs.url = "/backend/blog-backend/display-blog-list/"
        return HttpResponse(jrs.set_json_pack())

@login_required(login_url_name='users:login')
def display_blog_list(request):
    """
    blog list
    """
    if request.method == "GET":
        bl_obj_list = BlogList.objects.all().order_by("-adjustment_date", "-create_date")

        bk_obj_list = BlogKind.objects.all()
        tag_list = Tag.objects.all()
        tag_sim_list = []
        count = 0
        is_back = False
        for tag in tag_list:
            color_map = ["primary", "success", "warning", "danger"]
            random.shuffle(color_map)
            count = random.randrange(0, len(color_map))
            tag_sim_list.append([tag.name, color_map[count]])
            count += 1

        
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
        if search_handle != "None":
            bl_obj_list, search_handle = get_search_obj(request, bl_obj_list, search_fields)
        else:
            search_handle = ""
        current_page = int(request.GET.get("_p") or "1")
        row_in_page = 7

        pb = PageBranch(current_page, row_in_page, data_list=bl_obj_list)
        pb.get_pglist3()
        bl_obj_list = pb.get_data_list()
        
        return render(request, "blog_backend/display_blog_list.html", locals())

@login_required(login_url_name='users:login')
def message_list(request):
    if request.method == "GET":
        message_obj_list = MessageList.objects.all().order_by("-id")
        
        message_list = []
        for message in message_obj_list:
            message_list.append({
                "msg_id": message.id,
                "content": message.content,
                "username": message.creator.username,
                "create_date":message.create_date.strftime("%Y-%m-%d %H:%M:%S"),
                "adjustment_date":message.adjustment_date.strftime("%Y-%m-%d %H:%M:%S") if message.adjustment_date else None,
                "head_pic_url": message.creator.head_pic_url
            })
            pass
        return render(request, "blog_backend/message_list.html", locals())
    else:
        msg_id = request.POST.get("msg_id")
        MessageList.objects.filter(id=msg_id).delete()
        jrs = JsonResponse()
        jrs.set_success(0, "ok")
        
        jrs.url = "/backend/blog-backend/message-list/";

        return HttpResponse(jrs.set_json_pack())

# @login_required(login_url_name='users:login')
def kind_list(request):
    jrs = JsonResponse()
    if request.method == "POST":
        name = request.POST.get("name").strip()
        alias = request.POST.get('alias').strip()
        introdution = request.POST.get("introdution").strip()
        if not alias:
            alias = name

        try:
            bk = BlogKind()
            bk.name = name
            bk.alias = alias
            bk.introdution = introdution
            bk.create_date = datetime.datetime.now()
            bk.save()
            jrs.set_success(0, "ok")
            jrs.url = "/backend/blog-backend/display-blog-list/"
            jrs.id = bk.id
            jrs.name = bk.name
        except:
            jrs.set_error(300, "create failure")
    else: # GET
        bk_obj_list = BlogKind.objects.all()
        bk_list = []
        for bk_obj in bk_obj_list:
            bk_list.append(bk_obj.name)
        jrs.set_success(0, "ok")
        jrs.data = bk_list
    return HttpResponse(jrs.set_json_pack())

@login_required(login_url_name='users:login')
def kind_verify(request):
    field = request.POST.get("verify_field").strip()
    value = request.POST.get("value").strip()
    jrs = JsonResponse()
    if field == "name":
        if not value:
            jrs.set_error(300, "repeated")
        else:
            try:
                BlogKind.objects.get(name=value)
            except:
                jrs.set_success(0, "ok")
            else:
                jrs.set_error(300, "repeated")
    elif field == "alias":
        if value:
            try:
                BlogKind.objects.get(alias=value)
            except:
                jrs.set_success(0, "ok")
            else:
                jrs.set_error(300, "repeated")
        else:
            jrs.set_success(0, "ok")
        
    else:
        jrs.set_error(300, "repeated")
    return HttpResponse(jrs.set_json_pack())

@login_required(login_url_name='users:login')
def kind_delete(request):
    name_list = request.POST.get("name_list")
    name_list = json.loads(name_list)
    for name in name_list:
        BlogKind.objects.filter(name=name).delete()
    jrs = JsonResponse()
    jrs.set_success(0, "ok")
    jrs.url = "/backend/blog-backend/kind-delete/"
    return HttpResponse(jrs.set_json_pack())

@login_required(login_url_name='users:login')
def tag_list(request):
    jrs = JsonResponse()
    if request.method == "GET":
        tg_obj_list = Tag.objects.all()
        tg_list = []
        for tg_obj in tg_obj_list:
            tg_list.append(tg_obj.name)
        jrs.set_success(0, "ok")
        jrs.data = tg_list
    else:
        name = request.POST.get("name")
        tg = Tag()
        tg.name = name
        tg.save()

        jrs.set_success(0, "ok")
        jrs.id = tg.id
        jrs.name = tg.name
    return HttpResponse(jrs.set_json_pack())

@login_required(login_url_name='users:login')
def tag_verify(request):
    name = request.POST.get("name")
    
    tg = Tag.objects.filter(name=name)
    jrs = JsonResponse()
    if tg or not name:
        jrs.set_error(300, "error")
    else:
        jrs.set_success(0, "ok")
        
    return HttpResponse(jrs.set_json_pack())

@login_required(login_url_name='users:login')
def tag_delete(request):
    name_list = request.POST.get("name_list")
    name_list = json.loads(name_list)
    for name in name_list:
        Tag.objects.filter(name=name).delete()
    jrs = JsonResponse()
    jrs.set_success(0, "ok")
        
    return HttpResponse(jrs.set_json_pack())

@login_required(login_url_name='users:login')
def blog_title_verify(request):
    typ = request.POST.get("typ")
    value = request.POST.get("value")
    
    jrs = JsonResponse()
    if typ == "normal":
        if not value:
            jrs.set_error(300, "error")
        else:
            try:
                bl = BlogList.objects.get(title=value)
            except:
                jrs.set_success(0, "ok")
                
            else:
                jrs.set_error(300, "error")
        

    elif typ == "markdown":
        try:
            bl = BlogList.objects.get(title=value)
        except:
            jrs.set_success(0, "ok")
        else:
            jrs.set_error(300, "error")
    else:
        jrs.set_error(300, "error")
    return HttpResponse(jrs.set_json_pack())

def blog_delete(request):
    blog_id_list = request.POST.get("blog_id_list")
    blog_id_list = json.loads(blog_id_list)
    for blog_id in blog_id_list:
        BlogList.objects.filter(id=blog_id).delete()
    jrs = JsonResponse()
    jrs.set_success(0, "ok")
    return HttpResponse(jrs.set_json_pack())

def get_blog_message(request):
    jrs = JsonResponse()
    blog_id = request.GET.get("id")
    
    if blog_id:
        bl_obj = BlogList.objects.filter(id=blog_id).first()
        if bl_obj:
            jrs.set_success(0, "ok")
            jrs.title = bl_obj.title
            jrs.content = bl_obj.blog_content
            jrs.kind_id = bl_obj.blog_kind_id
            jrs.tag_id_list = [str(tag.id) for tag in bl_obj.tag.all()]
            if jrs.tag_id_list:
                jrs.tag_id_list = ",".join(jrs.tag_id_list)
            return HttpResponse(jrs.set_json_pack())
            
    jrs.set_error(300, "error")
    return HttpResponse(jrs.set_json_pack())

def blog_view(request):
    """
    display blog view
    1, list->view
    2, editing->cache file->view
    """
    if request.method == "POST":
        title = request.POST.get("title")
        blog_content = request.POST.get("blog_content")
        blog_kind_id = request.POST.get("blog_kind_id")
        tag_id_list = request.post.get("tag_id_list")
        jrs = JsonResponse()
        jrs.set_error(0, "error")
        return redirect("/backend/blog-backend/blog-view/?from=cache")
    else:
        blog_id = request.GET.get("id")
        bl_obj = BlogList.objects.get(id=blog_id)
        tag_list = bl_obj.tag.all()
        return render(request, "blog_backend/blog_view.html", locals())


def verify_related(request):
    """
    verify that blog kind or blog tag is related the blog
    typ: 
    k_b kind to blog, search kind-name探した上に、逆にブロックリストへ探す、探さなければ、異常を捨てる
    t_b tag to blog
    """
    jrs = JsonResponse()
    typ = request.POST.get("typ")
    name_list = request.POST.get("name_list")

    namelist = json.loads(name_list)
    for name in namelist:
        
        if typ == "k_b":
            try:
                bk_obj = BlogKind.objects.get(name=name)
                bl_li_co = bk_obj.bloglist_set.all().count()
                if bl_li_co == 0:
                    continue
                    
                else:
                    jrs.set_success(1, "the kind's relateds is having some blogs, can't delete")
                    jrs.name = name
            except:
                jrs.set_error(300, "didn't find out the kind name")
            
        elif typ == "t_b":
            try:
                tg_obj = Tag.objects.get(name=name)
                bl_li_co = tg_obj.bloglist_set.all().count()
                if bl_li_co == 0:
                    continue
                else:
                    jrs.set_success(1, "the tag's relateds is having some blogs, can't delete")
                    jrs.name = name
            except:
                jrs.set_error(300, "didn't find out the tag name")
        else:
            jrs.set_error(300, "didn't find out the name")

        return HttpResponse(jrs.set_json_pack())

    jrs.set_success(0, "the kind's relateds is never, can delete")
    return HttpResponse(jrs.set_json_pack())

def upload_markdown(request):
    """
    upload markdown file
    """
    if request.method == "POST":
        
        jrs = JsonResponse()
        blog_file_path = "var/data/blog_files"
        markdown_file = request.FILES.get("markdown_file")
        blog_kind_id = request.POST.get("blog_kind_id")
        userid = request.session.get("user")["id"]
        title = os.path.splitext(markdown_file.name)[0]
        title_group = re.match("(.*)(-[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9])", title)
        if title_group:
            title_group = title_group.groups()
            if len(title_group) >= 2:
                title = title_group[0]
        try:
            bl = BlogList.objects.get(title=title)
        except:
            bl = BlogList()
        bl.title = title
        blog_file_fullpath = os.path.join(blog_file_path, title)
        content = markdown_file.read()
        bl.blog_content = content
        bl.blog_kind_id = blog_kind_id
        bl.creator_id = userid
        bl.create_date = datetime.datetime.now()
        try:
            bl.save()
        except DjangoUnicodeDecodeError as e:
            bl.blog_content = content.decode("gbk").encode("utf8")

            bl.save()
        with open("%s.md" % blog_file_fullpath, "wb") as fp:
            fp.write(bl.blog_content)
        return HttpResponse(jrs.set_json_pack())
    else:
        bk_obj_list = BlogKind.objects.all()
        return render(request, "blog_backend/upload_markdown.html", locals())
