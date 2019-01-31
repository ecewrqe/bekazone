import re

from django.db.models import Q
from django.db.models.sql.query import FieldError
from django.db.models import QuerySet


def search_fieldobj(model_class, field):
    '''
    '''
    fields = field.split("__", 1)
    field_obj = model_class._meta.get_field(fields[0])
    if len(fields) == 2:
        field_obj = search_fieldobj(field_obj.related_model, fields[1])

    return field_obj


def get_filter_obj(request, model_class):
    """
    filter a table's row
    """
    filter_dict = {}
    q1 = Q()
    q1.connector = "AND"
    model_objs = QuerySet()
    try:
        for k, v in request.GET.items():

            if k in ["_p", "_s", "_o", "_f"]:
                continue

            if v:
                filter_dict[k] = v
                q1.children.append((k, v))
        model_objs = model_class.objects.filter(q1)
    except FieldError:
        pass
    return model_objs, filter_dict


def get_search_obj(request, model_objs, search_field):
    search_keyword = keyword = request.GET.get("_s")
    if keyword:
        q_search = Q()
        q_search.connector = "OR"
        for field in search_field:
            field_obj = search_fieldobj(model_objs.model, field)
            print("----", field_obj)
            type_flag = re.search(r"IntegerField|ForeignKey",
                                  field_obj.get_internal_type.__str__())
            if type_flag:
                try:
                    keyword = int(keyword)
                    q_search.children.append((field, keyword))
                except ValueError as e:  # int转换失败
                    pass
            else:
                q_search.children.append(("%s__icontains" % field, keyword))
        # 如果该字段是Integer,或Forignkey，转换成数字，如果不能转换，放弃该字段
        print(q_search)
        model_objs = model_objs.filter(q_search)
    return model_objs, search_keyword


def get_order_obj(request, model_objs):
    '''
    专门负责排序,_o,返回排完序的列表
    :param request:
    :return:
    '''
    search_field = request.GET.get("_o")
    if search_field:
        search_field.split(",")
        model_objs = model_objs.order_by(*search_field.split(","))
    else:  # 没有，按id倒叙排
        model_objs = model_objs.order_by("-id")
    return model_objs
