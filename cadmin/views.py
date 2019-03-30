import json

from django.shortcuts import render,redirect,HttpResponse
from django.conf import settings
from cadmin.baseadmin import site
from django.db.models import Q

# from cadmin.perm_handle import check_permission

from common.utils import JsonResponse

from common.utils import PageBranch
from cadmin.utils import get_filter_obj, get_order_obj, get_search_obj
from users.auth import login_required


for app in settings.INSTALLED_APPS:
    try:
        __import__("%s._admin" % app)

    except ImportError:
        pass

@login_required(login_url_name="login")
def index(request):
    """
    to collect every app
    """
    app_dict = site.app_dict
    return render(request,'admin/admin_index.html',locals())

@login_required(login_url_name="login")
def app_model(request,app):
    """
    app name to bind a model name
    """
    app_dict = site.app_dict
    model_objs = site.app_dict[app]

    return render(request, 'admin/admin_index_app.html', locals())


# @check_permission
@login_required(login_url_name="login")
def table_list(request, app, table, path="tamplate"):
    """
    to display a table
    usually table = model
    """
    request.session["old_url"] = request.path_info

    app_dict = site.app_dict # to reference such a dict
    model_class, admin_class = app_dict[app][table]

    # to filter a table's row
    model_class_objs, filter_dict = get_filter_obj(request, model_class)

    search_fields = admin_class.search_fields

    model_class_objs, search_keyword = get_search_obj(request, model_class_objs, search_fields)

    model_class_objs = get_order_obj(request, model_class_objs)

    current_page = int(request.GET.get("_p") or "1")
    row_in_page = int(admin_class.list_per_page)   # 一页显示7条


    admin_class_obj = admin_class()
    # to attach a page operator
    pb = PageBranch(current_page, row_in_page, data_list=model_class_objs)
    pb.get_pglist3()
    model_class_objs = pb.get_data_list()


    # #查找
    # app_obj=__import__(app)
    # #拿到筛选器
    # list_filter=table_item_admin.list_filter
    #
    # request_func=request.get_raw_uri

    # if path == "call":
    #     return locals()
    # else:

    return render(request, 'admin/admin_table_list.html', locals())

@login_required(login_url_name="login")
def table_change(request, app, table, id, path="template"):
    """
    give a form to change a table's record's informations
    """

    app_dict = site.app_dict
    model_class, admin_class = app_dict[app][table]

    form = admin_class.model_change_form
    model_obj = model_class.objects.get(id=id)

    
    if request.method == "GET":
        form_obj = form(instance=model_obj)
    else:
        form_obj = form(instance=model_obj, data=request.POST)
        if form_obj.is_valid():
            form_obj.save()

            # make a url to redirect
            url_path = request.path.rsplit("/",3)[0] + "/?" + "&".join(
                ["%s=%s" % (k, v) for k, v in request.GET.items()]
            )

            if path == "call":
                return url_path
            else:
                return redirect(url_path)
    app_obj = __import__(app)

    action = "change"

    return render(request, "admin/admin_table_change.html", locals())

@login_required(login_url_name="login")
def table_add(request,app,table,path="template"):
    '''
    give a form to add table
    :return:
    '''

    app_dict = site.app_dict
    app_model, table_item_admin = app_dict[app][table]


    form=table_item_admin.model_add_form

    if request.method == "GET":
        form_obj=form()
    else:
        form_obj = form(data=request.POST)
        if form_obj.is_valid():
            form_obj.save()

            url_path = request.path.rsplit("/",2)[0] + "/?" + "&".join(["%s=%s" % (k, v) for k, v in request.GET.items()])
            if path == "call":

                return url_path
            else:
                return redirect(url_path)
    app_obj = __import__(app)


    if path == "call":
        return locals()
    else:
        return render(request, "admin/admin_table_add.html", locals())

@login_required(login_url_name="login")
def table_delete(request, app_name, table, row_id, path="template"):
    app_dict = site.app_dict
    app_model, table_item_admin = app_dict[app_name][table]

    qs=app_model.objects.filter(id=row_id)
    if request.method == "POST":
        qs.delete()

        url_path=request.path.rsplit("/",3)[0]+"/?" + "&".join(["%s=%s" % (k, v) for k, v in request.GET.items()])

        if path == "call":
            return url_path
        else:
            return redirect(url_path)

    qs=qs.first()

    if path == "call":
        return locals()
    else:
        return render(request, "admin/admin_table_delete.html", locals())

action_ret = None

@login_required(login_url_name="login")
def get_action(request):
    """

    """

    global action_ret

    if request.method == "POST":
        action = request.POST.get("action")
        package = request.POST.get("package")  # 11,22,33
        table = request.POST.get("table")
        app = request.POST.get("app")

        app_dict = site.app_dict
        model_class, admin_class = app_dict[app][table]

        q1 = Q()
        q1.connector = "OR"
        package_list = package.split(',')
        for item in package_list:
            if item:
                q1.children.append(("id", item))

        if q1:
            query_set = model_class.objects.filter(q1)
        else:
            query_set = None

        admin_obj = admin_class()



        if action:
            if hasattr(admin_class, action):
                ret = getattr(admin_obj, action)(request, query_set)
                if ret:
                    
                    action_ret = ret
                    return HttpResponse("301")
                else:
                    return HttpResponse("200")
    elif request.method == "GET":
        if action_ret:
            ret = action_ret
            action_ret = redirect(request.session["old_url"] or reversed('index'))
            return ret
        else:
            return redirect(reversed('index'))

@login_required(login_url_name="login")
def batch_update(request):
    ret_dict = JsonResponse()
    if request.method == "POST":
        table = request.POST.get("table")
        app = request.POST.get("app")
        data_dict = json.loads(request.POST.get("data"))

        app_dict = site.app_dict
        model_class, admin_class = app_dict[app][table]

        print(data_dict)

        for id, data in data_dict.items():
            model_class.objects.filter(id=id).update(**data)

        ret_dict.status = 200
        return HttpResponse(json.dumps(ret_dict.__dict__))

