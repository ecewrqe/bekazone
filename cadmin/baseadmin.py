from cadmin.baseform import create_dynamic_modelform


def create_admin():
    # dynamically generate class object
    def batch_delete(self, request, query_set):
        query_set.delete()

    batch_delete.short_description = "批量删除"

    baseadmin = type('BaseAdmin'.encode("utf8"), (object,), {
        "list_display": (),
        "list_filter": (),
        "search_fields": (),
        "model_change_form": None,
        "order_fields": (),

        "model_add_form": None,
        "filter_horizontal": (),
        "list_per_page": 10,
        "actions": ['batch_delete', ],
        "list_editable": (),
        "readonly_field_for_change": (),

    })

    baseadmin.batch_delete = batch_delete
    return baseadmin


'''
1，注册的时候拿到表，自动创建，放入
'''
class AdminSite(object):
    def __init__(self):
        self.app_dict = {}

    def register(self, model_class, admin_class=None, **options):
        """
        主页上所有内容都是在register中生成的：
        {'app01':[model01,model02],'app02':[xxx]}
        site.register(model),
        拿到model对象和admin对象
        :param model_class:
        :param admin_class:
        :param options:
        :return:
        """

        baseadmin = create_admin()

        if not admin_class:
            admin_class = baseadmin

        form_class = create_dynamic_modelform(model_class)

        admin_class.model_add_form = form_class if not admin_class.model_add_form else admin_class.model_add_form
        admin_class.model_change_form = form_class if not admin_class.model_change_form else admin_class.model_change_form

        # 每次注册创建一个表单基类，放到admin_class中

        # if not admin_class:
        #     adm=BaseAdmin(model_or_iterable)
        # else:
        #     adm=admin_class(model_or_iterable)

        app_label = model_class._meta.app_label
        if app_label not in self.app_dict:
            self.app_dict[app_label] = {}
        model_name = model_class._meta.model_name

        self.app_dict[app_label][model_name] = [model_class, admin_class, ]


site = AdminSite()




