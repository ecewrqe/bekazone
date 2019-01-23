# --coding:utf8--

from __future__ import absolute_import
from __future__ import unicode_literals

import re
from django import forms
from django.forms import ValidationError
from django.utils import timezone
from . import models
from common.utils import date_to_string

from .password_hasher import SaltMD5PasswordHasher


class PasswordValidator(object):
    '''
    密码匹配
    '''
    message = ""
    max_length = 8
    letter_regex = re.compile(r'\D')

    def __call__(self, value):
        self.message = None
        if len(value) < 8:
            self.message = "the password length should outride %s"%self.max_length

        if len(self.letter_regex.findall(value)) < 3:
            self.message = "the password nonumber letter length should > 3"

        if self.message:
            raise ValidationError(self.message)


class UserLoginForm(forms.Form):
    username = forms.CharField(label='Username',
                               widget=forms.TextInput(attrs={'class': 'form-control',
                                                             'placeholder': 'Username',
                                                             })
                               )
    password = forms.CharField(label='Password', min_length=6,
                               widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                 'placeholder': 'Password'}),
                               )


class UserCreateForm(forms.ModelForm):
    """用户创建表单"""
    def mix_compare_password(self, cleaned_data):
        """
        加密，同时比较两个密码
        :param cleaned_data:
        :return:
        """
        password1 = cleaned_data['password1']
        hasher = SaltMD5PasswordHasher()
        cleaned_data['password1'] = hasher.encoding(password1)
        res = hasher.verify(cleaned_data['password2'], cleaned_data['password1'])
        return res

    def save(self, commit=True):
        """保存用户"""
        compare_ret = self.mix_compare_password(self.cleaned_data)
        self.cleaned_data['password'] = self.cleaned_data['password1']
        self.instance.password = self.cleaned_data['password']
        self.instance.group_id = self.cleaned_data["group_id"]
        self.instance.instaff_date = timezone.now()
        if compare_ret:
            super(UserCreateForm, self).save(commit)
        else:
            self.add_error('password2', 'password confirm is not equal password')


class UserFirstCreateForm(UserCreateForm):
    """用户第一次登陆用表单"""

    password1 = forms.CharField(label='密码', widget=forms.PasswordInput(attrs={
        "class": "form-control",
        "placeholder": "密码大于8位，并且字母不小于3个"
    }), validators=[PasswordValidator(), ], help_text="*", )
    password2 = forms.CharField(label='密码确认', widget=forms.PasswordInput(attrs={
        "class": "form-control",

    }), help_text="*")

    class Meta:
        fields = ["username", "email", "phone"]
        model = models.User

        help_texts = {
            "username": "*",
            "email": "*",
        }

        widgets = {
            "username": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": '用户名',
            }),
            "email": forms.EmailInput(attrs={
                "class": "form-control",
                'placeholder': 'example@gmail.com'
            }),
            "phone": forms.TextInput(attrs={
                "class": "form-control",
                'placeholder': '手机号'
            })
        }

    def save(self, commit=True):
        self.cleaned_data["group_id"] = models.Group.objects.get(groupname="admin").id

        super(UserFirstCreateForm, self).save(commit)


class PasswdChangeForm(forms.Form):
    old_passwd = forms.CharField(label='Old Password', widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'id': 'old-passwd',
    }), validators=[PasswordValidator()])
    new_passwd = forms.CharField(label='New Password', widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'id': 'new-passwd'
    }), validators=[PasswordValidator()])
    new_passwd_confirm = forms.CharField(label='New Password Confirm', widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'id': 'new-passwd-confirm',
    }), validators=[PasswordValidator()])

    def mix_passwd_compare(self, cleaned_data, user_dict):
        """
        1，比较旧密码和session中的密码
        2，加密新密码
        3，比较加密后的新密码和第二遍的新密码
        :return: 首先在cleaned_data中加入password，最终的密码，如果有errors，add_errors，
        """
        hasher = SaltMD5PasswordHasher()
        old_pass_res = hasher.verify(cleaned_data['old_passwd'], user_dict['password'])
        if old_pass_res:
            new_password = hasher.encoding(cleaned_data['new_passwd'])
            new_pass_res = hasher.verify(cleaned_data['new_passwd_confirm'], new_password)
            if new_pass_res:
                cleaned_data['password'] = new_password
            else:
                self.add_error('new_passwd_confirm','new password unfirmness')
        else:
            self.add_error('old_passwd', 'old password error')

        return cleaned_data

    def save(self, user_dict):
        """
        密码保存和验证，应该传入session的user
        :param user_dict:
        :return:
        """
        self.cleaned_data = self.mix_passwd_compare(self.cleaned_data,user_dict)
        if not self.errors:
            uid = user_dict['id']
            new_obj = models.User.objects.filter(id=uid).first()
            new_obj.password = self.cleaned_data['password']
            new_obj.save()


class UserSettingForm(forms.ModelForm):
    """
    用户配置表单
    """

    class Meta:
        fields = ["username", "email", "phone", "head_pic_url", "person_name",
                  "birth_date", "card_id", "introduce"]

        model = models.User

        help_texts = {
            "username": "*",
            "email": "*",
            "phone": "*",
            "person_name": "*",
            "birth_date": "*",
            "card_id": "*",
        }

        widgets = {
            "username": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": 'Username',
            }),
            "email": forms.EmailInput(attrs={
                "class": "form-control",
                'placeholder': 'Email'
            }),
            "phone": forms.TextInput(attrs={
                "class": "form-control",
                'placeholder': 'Phone'
            }),
            "person_name": forms.TextInput(attrs={
                "class": "form-control",
                'placeholder': "Person Name",
            }),
            "birth_date": forms.TextInput(attrs={
                "class": "form-control",
                'placeholder': "yyyy-mm-dd",
                "data-date-format": "yyyy-mm-dd",
            }),
            "card_id": forms.TextInput(attrs={
                "class": "form-control",
                'placeholder': "Card Id",
            }),
            "introduce": forms.Textarea(attrs={
                "class": "form-control",
            })
        }

    def save(self, request, commit=True):
        print(self.cleaned_data)
        super(UserSettingForm, self).save(commit)
        user_id = int(request.session['users']['id'])
        print(user_id)
        user_obj = models.User.objects.get(id=user_id)
        print(user_obj)

        user_dict = user_obj.__dict__
        print(user_dict)
        # user_dict.pop["group"]
        del user_dict['_state']
        del user_dict['_group_cache']

        user_dict['birth_date'] = date_to_string(user_dict['birth_date'])
        user_dict['instaff_date'] = date_to_string(user_dict['instaff_date'])
        request.session['user'] = user_dict


class StaffCreateForm(UserCreateForm):
    '''
    创建员工/管理员：默认密码:123456,
    '''
    try:
        GROUP_CHOICES = models.User._meta.get_field('group').get_choices()

        group = forms.ChoiceField(initial='', choices=GROUP_CHOICES, widget=forms.Select(attrs={
            'style': 'width:100%',
        }))
    except Exception:
        group = forms.ChoiceField(initial='', choices=[], widget=forms.Select(attrs={
            'style': 'width:100%',
        }))

    class Meta:
        fields = ['username', 'email', 'phone']
        model = models.User

        help_texts = {
            'username': '*',
            'email': '*',
        }

        widgets = {
            "username": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": 'Username',
            }),
            "email": forms.EmailInput(attrs={
                "class": "form-control",
                'placeholder': 'Email',
            }),
            "phone": forms.TextInput(attrs={
                "class": "form-control",
            })
        }

    def save(self, commit=True):

        default_staff_password = '123456'
        self.cleaned_data['password'] = default_staff_password
        hasher = SaltMD5PasswordHasher()

        self.cleaned_data['password'] = hasher.encoding(self.cleaned_data['password'])
        self.instance.password = self.cleaned_data['password']
        self.instance.group_id = self.cleaned_data['group']
        print(self.cleaned_data['password'])
        super(UserCreateForm, self).save()


class GroupCreateForm(forms.ModelForm):
    class Meta:
        model = models.Group
        fields = ["groupname",]

        help_texts = {
            "groupname": "*",
        }

        widgets = {
            "groupname": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": 'Groupname',
            }),
        }

class EmployeeCreateForm(forms.Form):
    employee_num = forms.CharField(label="工号", required=True)
    userid = forms.CharField(label="微信号", required=True)
    name = forms.CharField(label="姓名", required=True)
    email = forms.CharField(label="邮箱", required=True)
    mobile = forms.CharField(label="手机号", required=True)
