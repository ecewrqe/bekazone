# It is bekablog's admin
from cadmin import baseadmin
from blog_backend import models


class BlogAdmin(baseadmin.create_admin()):
    list_display = ["title", "blog_kind__name", "tag__name"]
    list_filter = ("title", "blog_kind")
    search_fields = ["title"]
    order_fields = ["title"]


class BlogKindAdmin(baseadmin.create_admin()):
    list_display = ["name", "alias"]



baseadmin.site.register(models.BlogList, BlogAdmin)
baseadmin.site.register(models.BlogKind, BlogKindAdmin)