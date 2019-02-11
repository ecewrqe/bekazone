# It is bekauser's admin
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
        return HttpResponse("welcome to tiger zoo")

    tigermark.short_description = "tiger zoo"


class GroupAdmin(baseadmin.create_admin()):
    list_display = ["groupname"]

baseadmin.site.register(models.User, UserAdmin)
baseadmin.site.register(models.Group, GroupAdmin)
