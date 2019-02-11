from django.shortcuts import render, redirect, reverse, HttpResponse
import json
import datetime
from blog_backend.models import MessageList, BlogKind, Tag, BlogList
from common.utils import JsonResponse
import random
from users.auth import login_required


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
    elif edit_type == "normal_blog":
        return redirect(reverse("blog_backend:normal_edit_blog"))
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
            print(msg_id)
            ml_obj = MessageList.objects.filter(id=msg_id)
        return render(request, "blog_backend/message.html", locals())
    else:
        typ = request.POST.get("typ")
        if typ == "get_content":
            print(typ)
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
        
            jrs.url = "/blog-backend/message-list/";

            return HttpResponse(jrs.set_json_pack())

@login_required(login_url_name='users:login')
def normal_edit_blog(request):
    """
    normal editor
    """
    if request.method == "GET":
        blog_id = request.GET.get("id")
        if blog_id:
            try:
                bl_obj = BlogList.objects.get(id=blog_id)
            except:
                return redirect("/blog-backend/display-blog-list/")
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
            print("repair")
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
        jrs.url = "/blog-backend/display-blog-list/";
        return HttpResponse(jrs.set_json_pack())

@login_required(login_url_name='users:login')
def md_edit_blog(request):
    """
    markdown mode editor
    """
    if request.method == "GET":
        return render(request, "blog_backend/md_edit_blog.html")

@login_required(login_url_name='users:login')
def display_blog_list(request):
    """
    blog list
    """
    if request.method == "GET":
        bl_obj_list = BlogList.objects.all()

        bk_obj_list = BlogKind.objects.all()
        tag_list = Tag.objects.all()
        tag_sim_list = []
        count = 0
        for tag in tag_list:
            color_map = ["primary", "success", "warning", "danger"]
            random.shuffle(color_map)
            tag_sim_list.append([tag.name, color_map[count]])
            count += 1
        
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
        
        jrs.url = "/blog-backend/message-list/";

        return HttpResponse(jrs.set_json_pack())

@login_required(login_url_name='users:login')
def kind_list(request):
    name = request.POST.get("name").strip()
    alias = request.POST.get('alias').strip()
    introdution = request.POST.get("introdution").strip()
    if not alias:
        alias = name
    jrs = JsonResponse()
    try:
        bk = BlogKind()
        bk.name = name
        bk.alias = alias
        bk.introdution = introdution
        bk.create_date = datetime.datetime.now()
        bk.save()
        jrs.set_success(0, "ok")
        jrs.url = "/blog-backend/display-blog-list/"
        jrs.id = bk.id
        jrs.name = bk.name
    except:
        jrs.set_error(300, "create failure")
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
            print("none")
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
    jrs.url = "/blog-backend/kind-delete/"
    return HttpResponse(jrs.set_json_pack())

@login_required(login_url_name='users:login')
def tag_list(request):
    name = request.POST.get("name")
    tg = Tag()
    tg.name = name
    tg.save()
    jrs = JsonResponse()
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
    print("blog delete")
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
        print(blog_id)
        bl_obj = BlogList.objects.filter(id=blog_id).first()
        if bl_obj:
            jrs.set_success(0, "ok")
            jrs.title = bl_obj.title
            jrs.content = bl_obj.blog_content
            jrs.kind_id = bl_obj.blog_kind_id
            jrs.tag_id_list = [str(tag.id) for tag in bl_obj.tag.all()]
            print(jrs.tag_id_list)
            if jrs.tag_id_list:
                jrs.tag_id_list = ",".join(jrs.tag_id_list)
            return HttpResponse(jrs.set_json_pack())
            
    jrs.set_error(300, "error")
    return HttpResponse(jrs.set_json_pack())

def blog_view(request):
    """
    display blog view
    """
    blog_id = request.GET.get("id")
    bl_obj = BlogList.objects.get(id=blog_id)
    return render(request, "blog_view.html", locals())
