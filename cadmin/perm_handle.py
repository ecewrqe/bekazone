from django.shortcuts import HttpResponse
from django.core.urlresolvers import resolve


def perm_check_content(request,app,*args,**kwargs):
    app=__import__("%s.permissions"%app)

    perm_dict=app.permissions.perm_dict

    url_obj = resolve(request.path)
    print(url_obj)
    url_name = url_obj.url_name
    matched_key=None
    matched_list = [None]
    hook_ret=True



    for perm_name, perm_item in perm_dict.items():
        perm_item_url = perm_item[0]
        perm_item_method = perm_item[1]
        perm_item_param_list = perm_item[2]
        perm_item_param_dict = perm_item[3]

        perm_item_hook=perm_item[-1] if len(perm_item) == 5 else None

        if perm_item_url == url_name:
            if perm_item_method == request.method:
                args_matched = False
                req_param = request.GET
                for item in perm_item_param_list:

                    if req_param.get(item,None):  #必须有值
                        args_matched = True
                    else:   #只要没有匹配上就是false
                        args_matched = False
                        break
                else:   #没有参数为True
                    args_matched=True

                kwargs_matched = False
                for k, v in perm_item_param_dict.items():
                    print(k,v,req_param.get(k))

                    if req_param.get(k) == v:
                        kwargs_matched = True
                        print(kwargs_matched)
                    else:
                        kwargs_matched = False
                        break
                else:
                    kwargs_matched=True


                if perm_item_hook:
                    hook_ret=perm_item_hook()

                matched_list = [args_matched, kwargs_matched, hook_ret]
                if all(matched_list):
                    matched_key=perm_name
                    break







    if all(matched_list):
        perm="%s.%s"%tuple(matched_key.split("_",1))
        if request.user.has_perm(perm):
            return True
        else:
            return False
    else:
        return False



def check_permission(func):
    '''
    1，去找权限，如果能找到，放行
    2，如果不能找到返回403

    name:[url_name,method]

    根据path，method，parameters找，如果有一个找不到，就返回403

    3,在url和method匹配到后，先list匹配，url+method具有 唯一性

    匹配上后必须在groups中有权限
    在perm_name中规定<app>_<perm>
    匹配group是当前用户去匹配，这一步是为了判断整张表是否有权限

    4,如果有钩子，用钩子的返回值来决定

    :param func:
    :return:
    '''



    def inner(request,*args,**kwargs):


        if perm_check_content(request,*args,**kwargs):

            return func(request,*args,**kwargs)
        else:
            return HttpResponse("403")
    return inner
