
from django.db import models
from django.utils.translation import gettext_lazy as _

class User(models.Model):

    username = models.CharField(verbose_name='username', max_length=128, unique=True)
    password = models.CharField(verbose_name='password', max_length=128)
    email = models.EmailField(verbose_name='email', max_length=128)
    group = models.ForeignKey('Group', related_name='u_group', null=True, blank=True, on_delete=models.DO_NOTHING)
    phone = models.CharField(verbose_name='phonenumber', max_length=128, null=True, blank=True)
    is_superadmin = models.BooleanField(verbose_name='is_superadmin', default=False)

    head_pic_url = models.CharField(verbose_name="headicon", max_length=512, null=True, blank=True)
    person_name = models.CharField(verbose_name="surname", max_length=32, null=True, blank=True)
    birth_date = models.DateTimeField(verbose_name="birth", null=True, blank=True)
    card_id = models.CharField(verbose_name="identified card", max_length=32, null=True, blank=True)

    introduce = models.TextField(verbose_name="introduce", max_length=200, null=True, blank=True)

    instaff_date = models.DateTimeField(verbose_name="instaff date", auto_now=True)

    def __str__(self):
        return "<User: %s>" % (self.username)

class Group(models.Model):
    groupname = models.CharField(verbose_name="groupname", max_length=128, unique=True)
    introduce = models.TextField(verbose_name="introduce", max_length=200, null=True, blank=True)
    def __str__(self):
        return "<Group: %s>" % (self.groupname)

