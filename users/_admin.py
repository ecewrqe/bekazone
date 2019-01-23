# --coding:utf8--

from __future__ import absolute_import
from __future__ import unicode_literals
from django.shortcuts import HttpResponse

# Register your models here.

from cadmin import baseadmin
from users import models


class UserAdmin(baseadmin.create_admin()):
    list_display = ["username", "email", "person_name"]
    list_filter = ("group", )
    actions = ("tigermark", )
    readonly_field_for_change = ("group", )

    def tigermark(self, request, query_set):
        return HttpResponse("欢迎来到老虎动物园")

    tigermark.short_description = "老虎动物园"


class GroupAdmin(baseadmin.create_admin()):
    list_display = ["groupname"]

baseadmin.site.register(models.User, UserAdmin)
baseadmin.site.register(models.Group, GroupAdmin)
