from cadmin.baseform import create_dynamic_modelform


def create_admin():
    # dynamically generate class object
    def batch_delete(self, request, query_set):
        query_set.delete()

    batch_delete.short_description = "batch_delete"

    baseadmin = type('BaseAdmin', (object,), {
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
        "readonly_field_for_change": ()

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
        a model_class only have an admin_class, if not system generate it
        """
        baseadmin = create_admin()

        if not admin_class:
            admin_class = baseadmin

        form_class = create_dynamic_modelform(model_class)

        admin_class.model_add_form = form_class if not admin_class.model_add_form else admin_class.model_add_form
        admin_class.model_change_form = form_class if not admin_class.model_change_form else admin_class.model_change_form

        # every model should be belong to every app
        # admin_class bind with every model_name
        # {app_name:{model_name: [model_class, admin_class]}}
        app_label = model_class._meta.app_label
        if app_label not in self.app_dict:
            self.app_dict[app_label] = {}
        model_name = model_class._meta.model_name

        self.app_dict[app_label][model_name] = [model_class, admin_class, ]

site = AdminSite()




