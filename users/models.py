#--coding:utf8--

from __future__ import absolute_import
from __future__ import unicode_literals

from django.db import models
from django.utils.translation import gettext_lazy as _


class User(models.Model):

    '''
    用户表
    用户是唯一值
    '''

    # 用户登陆信息
    username = models.CharField(verbose_name='用户名', max_length=128, unique=True)
    password = models.CharField(verbose_name='密码', max_length=128)
    email = models.EmailField(verbose_name='邮箱', max_length=128)
    group = models.ForeignKey('Group', related_name='u_group', null=True, blank=True)
    phone = models.CharField(verbose_name='手机号', max_length=128, null=True, blank=True)

    # 用户详细信息
    head_pic_url = models.CharField(verbose_name="头像", max_length=512, null=True, blank=True)
    person_name = models.CharField(verbose_name='姓名', max_length=32, null=True, blank=True)
    birth_date = models.DateTimeField(verbose_name='出生日期', null=True, blank=True)
    card_id = models.CharField(verbose_name="身份证", max_length=32, null=True, blank=True)

    introduce = models.TextField(verbose_name="说明", max_length=200, null=True, blank=True)

    instaff_date = models.DateTimeField(verbose_name="入职日期", auto_now=True)

    def __unicode__(self):
        return "<User: %s>" % (self.username)

class Group(models.Model):
    """
    admin
    运维
    """
    groupname = models.CharField(max_length=128, unique=True)
    introduce = models.TextField(max_length=200, null=True, blank=True)

    def __unicode__(self):
        return "<Group: %s>" % (self.groupname)

