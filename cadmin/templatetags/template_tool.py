from django import template
from django.utils.safestring import mark_safe
# A site is a piece of ground that is used for a particular purpose or where a particular thing habbens
from cadmin.baseadmin import site
from common.utils import demark_safe

register = template.Library()


@register.simple_tag
def get_verbose_name(model_class):
    return model_class[0]._meta.verbose_name


@register.filter
def decode_utf8(src):
    return unicode(src)


@register.simple_tag
def get_field_verbose_name(model_class, field):
    """
    verbose_name/related_name
    :param model_class:
    :param field:
    :return:
    """
    fields = field.split("__", 1)
    field_obj = model_class._meta.get_field(fields[0])
    if len(fields) == 2:
        verbose_name = get_field_verbose_name(field_obj.related_model, fields[1])
    else:
        verbose_name = model_class._meta.get_field(field).verbose_name
    return verbose_name


def get_depth_value(obj, field):
    """
    递归读取
    aa__bb__cc
    如果有__说明是外键，往里面走
    如果找到最里面的，看是否是choice，如果是，get_该字段_display找值，如果不是，直接按照该字段找值
    a__b__c
    """
    fields = field.split("__", 1)
    if len(fields) == 2:

        obj = getattr(obj, fields[0])

        value = get_depth_value(obj, fields[1]) if obj else ""

    else:
        field_obj = obj._meta.get_field(field)
        try:
            choice = field_obj.choices
        except AttributeError:
            choice = None
        if choice:
            value = getattr(obj, "get_%s_display" % field)()

        else:
            value = getattr(obj, field)
    return value


@register.filter
def get_model_value(obj, field):

    value = get_depth_value(obj, field)

    return value


@register.simple_tag
def get_model_url(request, table_obj, field):
    """单个url的制作,目的给前端和内部都能调用"""
    url = "<td><a href='%s/change/?%s'>%s</a></td>" % (
        table_obj.id,
        "&".join(["%s=%s" % (k, v) for k, v in request.GET.items()]),
        get_model_value(table_obj, field)
    )
    return mark_safe(url)


@register.simple_tag
def get_model_item(request, table_obj, admin_class):
    """
    穿表对象和admin对象，根据field取表的每个记录，第一个字段是可链接的，不可修改
    list_editable不可用双下划线
    """
    fields = admin_class.list_display

    editfields = admin_class.list_editable

    form_obj = admin_class.model_change_form(instance=table_obj)

    ret_html = []

    ret_html.append('''<td>
    <div class="checkbox check-transparent">
                <input type="checkbox" class="magic-checkbox" id="check_%s" name="check_item" value="%s" onclick="check_component('check_item','checkall')">
                <label for="check_%s"></label>
            </div></td>
    ''' % ((table_obj.id, ) * 3))
    for field in fields:
        if fields.index(field) == 0:

            ret_html.append(get_model_url(request, table_obj, field))
        else:
            if field in editfields:
                ret_html.append("<td>%s</td>" % form_obj[field])
            else:
                get_model_value(table_obj, field)

                ret_html.append("<td>%s</td>" % (get_model_value(table_obj, field)))

    return mark_safe("".join(ret_html))


@register.simple_tag
def get_filter_options(table, field):
    """
    拿到该字段的对象，找get_choices
    如果有__ 如：group__groupname   列出所有groupname字段的数据
    :param table:
    :param field:
    :return:
    table._meta.get_field(group).model.objects.value_list('groupname')
    table._meta.get_field(group).model._meta.get_field(group).model.objects.value_list('groupname')
    """

    def get_depth_filter(table, field):
        fields = field.split("__", 1)

        field_obj = table._meta.get_field(fields[0])

        if len(fields) == 2:
            # print(field_obj.related_model)
            ret_html = get_filter_options(field_obj.related_model, fields[1])
        else:
            ret_html = []
            try:
                for choice in field_obj.get_choices():
                    chose = (choice[0], demark_safe(choice[1]))

                    ret_html.append("<option value='%s'>%s</option>" % chose)
            except AttributeError:  # 没有拿到choice说明是普通字段
                choice_list = [('', '---------'), ]
                choice_list.extend(field_obj.model.objects.all().values_list(field, field))
                for choice in choice_list:
                    ret_html.append("<option value='%s'>%s</option>" % choice)
                pass
        return ret_html

    ret_html = get_depth_filter(table, field)

    '''
    默认：模板引擎向下转义一层，浏览器向上转义一层，等到的是原来的字符串
    mark_safe: 如果模板引擎没有向下转换，但浏览器向上转换，会被翻译成html语言
    所以直接return回去的字符串或者在模板内(两个大括号或{%%}之间的)会原样输出，
    但是被mark_safe修饰过就能被浏览器翻译成html语言

    默认机制的好处是：
    如果黑客在可输入框中输入html语句，提交后存到数据库，再次拿到时不会被翻译成html语句，html代码就无法植入
    如果不这么做，那么他想要插入什么语句就是什么语句，会被植入任何广告等等
    '''

    return mark_safe("".join(ret_html))


@register.simple_tag
def make_url(path_info, filter_dict, action):
    '''
    对已有的url和get进行重构
    :param path_info:
    :return:
    '''
    param_dict = {}
    for k, v in filter_dict.items():
        param_dict[k] = "%s=%s" % (k, v)

    url = "%s%s?%s" % (path_info, action, "&".join(param_dict.values()))
    return url


@register.simple_tag
def make_delete_url(path_info, filter_dict):
    path_info = path_info.rsplit("/", 2)[0]
    url = make_url(path_info, filter_dict, "/delete/")
    return url


@register.simple_tag
def merge_url(path_info, filter_dict, page_value):
    """拼凑成url,给页码"""
    param_dict = {}
    for k,v in filter_dict.items():
        param_dict[k] = "%s=%s" % (k, v)

    param_dict["_page"] = "%s=%s" % ("_page", page_value)

    url = "%s?%s" % (path_info, "&".join(param_dict.values()))
    return url


def get_url_dict(p_dict):
    """此函数生成字典，形式是k:k=v"""
    param_dict = {}

    for k, v in p_dict.items():
        param_dict[k] = "%s=%s" % (k, v)
    return param_dict


@register.simple_tag
def get_order_url(request, field):
    """
    生成排序的url,
    排序看_o，如果_o没有，直接加_o:field，如果有_o:field,field，
    还要比对一下，如果该feild不在里边，直接添加，如果在里边，判断正负
    field传过来是字段名，不存在正负，肯定是正的，在列表中，如果存在该字段，无论正负都应该删除
    """
    url_dict = {}
    for k, v in request.GET.items():
        url_dict[k] = v
    if url_dict.get("_o"):
        flag = check_order_field(request.GET, field)
        order_list=url_dict["_o"].split(",")
        # field可能是-xx,xx
        if flag == "+":
            order_list.remove(field)
            field = "-%s" % field

        if  flag == "-":
            order_list.remove("-%s" % field)
            field = field

        order_list.append(field)
        order_list = set(order_list)
        url_dict["_o"] = ",".join(order_list)
    else:
        url_dict["_o"] = field

    url_dict = get_url_dict(url_dict)

    return "&".join(url_dict.values())


@register.simple_tag
def check_order_field(source,field):
    """根据GET中的_o和field,判断是否在里面"""
    source=source.get("_o")
    if source:
        order_list=source.split(",")
        if field in order_list:
            return "+"    # 肯定有正的该字段存在
        elif "-%s" % field in order_list:
            return "-"  # 肯定有负的该字段存在

        else:
            return None  # 说明该字段不存在


@register.simple_tag
def get_m2m_selected_fields(form_obj, field_name):
    # form_obj是这个记录的form的对象,form_obj.instance是这个form_obj对应的表  如Account表
    # print(field_name)
    # if field_name != "id":
    #     if hasattr(form_obj.instance,field_name):
    # print(bool(form_obj.instance),dir(form_obj.instance))
    # m2m_obj=getattr(form_obj.instance,field_name)   #m2m这个记录的字段对象，是多对多字段。直接all(拿到该记录的所有多对多)
    # 如果有句柄，说明是更新，没有，，去_meta拿model，。。。空

    # print("ddddd",form_obj.instance._meta.get_field("name"))   # model_obj
    if form_obj.instance.id:   # id没有，说明不是model对象
        m2m_obj = getattr(form_obj.instance,field_name)
        # form_obj[field_name].field.widget.attrs['class']=''
        # def create_option(self, name, value, label, selected, index, subindex=None, attrs=None):

        return m2m_obj.all()  # m2m字段直接all找到对应表的所有
    else:
        return []


@register.simple_tag
def get_m2m_fields(model, field_name, selected):
    field_obj = model._meta.get_field(field_name)
    obj_all = field_obj.rel.to.objects.all()
    return set(obj_all) - set(selected)


@register.simple_tag
def get_description(admin, action):
    """找到每个函数，和它的short_description"""
    print(admin)
    if hasattr(admin, action):

        act_fun = getattr(admin, action)

        if hasattr(act_fun, "short_description"):
            return getattr(act_fun, "short_description")
        else:
            return action
    else:
        raise AttributeError("%s function not found" % action)



@register.simple_tag
def get_relate_depth(model_obj, depth_flag=False):
    """
    find all has related node
     被关联,rel
     find related field
     model.relatedfield.all()   拿到和该记录相关的对方的记录
     循环每一个

     对于many_to_many只是做一些提示，
    :param model_obj:
    :param depth_flag: 是否是下一层递归
    :return:
    """

    node_list = []
    if not depth_flag:
        node_list.append("<dl class='dl-horizontal'>")
    node_list.append("<dd style='margin-left:0'>")

    # if has model bond to admin then get a link,else
    if model_obj._meta.app_label in site.app_dict:
        print(model_obj._meta.model_name in site.app_dict[model_obj._meta.app_label])
        if model_obj._meta.model_name in site.app_dict[model_obj._meta.app_label]:
            node_list.append(
                ("%s:<a href='/admin/{app}/{table}/{id}/change'>%s</a>" %
                 (model_obj._meta.verbose_name,str(model_obj))).format(
                    app=model_obj._meta.app_label, table=model_obj._meta.model_name, id=model_obj.id
                )
            )
        else:
            node_list.append(
                "%s:%s" % (model_obj._meta.verbose_name, str(model_obj))
                )

    related_nodes = model_obj._meta.get_fields()

    for rel_node in related_nodes:
        if not hasattr(rel_node,"column"):  # 被关联
            rel_field = rel_node.get_accessor_name()
            sub_model_objs = getattr(model_obj, rel_field).all()
            if sub_model_objs:
                node_list.append("<dl>")
                node_list.append("<dt>many to one</dt>")

            for sub_model_obj in sub_model_objs:
                node_list.append(get_relate_depth(sub_model_obj, depth_flag=True))

            if sub_model_objs:
                node_list.append("</dl>")


        else:
            if rel_node.get_internal_type() == "ManyToManyField":
                sub_model_objs = getattr(model_obj, rel_node.column).all()
                if sub_model_objs:
                    node_list.append("<dl>")
                    node_list.append("<dt>many to many</dt>")
                for sub_model_obj in sub_model_objs:
                    node_list.append("<dd>%s</dd>" % str(sub_model_obj))

                if sub_model_objs:
                    node_list.append("</dl>")
    node_list.append("</dd>")
    if not depth_flag:
        node_list.append("</dl>")

    return "".join(node_list)


@register.simple_tag
def get_bool(s1, s2):
    print(s1, s2)
    print(type(s1), type(s2))
    return s1 == s2


@register.simple_tag
def get_read_only_readable(field, instance):
    '''
    :param field:  字段表单
    :return:
    '''
    ret_html = field

    ret_html.field.widget.attrs.update({"disabled": "disabled", "class": "hide"})

    ret_html = "<p>%s</p>%s" % (ret_html.value(), unicode(ret_html))

    field_type = instance._meta.get_field(field.name).get_internal_type()

    if field_type == "ManyToManyField":
        value = getattr(instance, field.name).all()

        # ret_html = value + "<input type='hidden' name='%s' value='%s' />" % (field, value)
        ret_html = ""

    else:
        field_obj = getattr(instance, field.name)
        if field_type == "ForeignKey":
            ret_html = demark_safe(str(field_obj)) + "<input type='hidden' name='%s' value='%s' />" % \
                                                     (field.name, instance.id)
        else:
            ret_html = demark_safe(field_obj) + "<input type='hidden' name='%s' value='%s' />" % (field.name, field_obj)

    return mark_safe(ret_html)



