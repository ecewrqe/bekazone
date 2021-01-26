import re
from django import forms
from django.forms import ValidationError
from django.utils import timezone
from . import models
from common.utils import date_to_string

from .password_hasher import SaltMD5PasswordHasher


class PasswordValidator(object):
    """
    to validate password
    """
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
    """
    to make a form to create user
    """
    def mix_compare_password(self, cleaned_data):
        """
        :param cleaned_data:
        :return:
        """
        password1 = cleaned_data['password1']
        hasher = SaltMD5PasswordHasher()
        cleaned_data['password1'] = hasher.encoding(password1)
        res = hasher.verify(cleaned_data['password2'], cleaned_data['password1'])
        return res

    def save(self, commit=True):
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
    """
    make a form to create initial user
    """

    password1 = forms.CharField(label="password", widget=forms.PasswordInput(attrs={
        "class": "form-control",
        "placeholder": "the password is greater than 8 digits and the letters are not less than 3"
    }), validators=[PasswordValidator(), ], help_text="*", )
    password2 = forms.CharField(label="confirm password", widget=forms.PasswordInput(attrs={
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
                "placeholder": "username",
            }),
            "email": forms.EmailInput(attrs={
                "class": "form-control",
                'placeholder': 'example@gmail.com'
            }),
            "phone": forms.TextInput(attrs={
                "class": "form-control",
                'placeholder': '000-0000-0000'
            })
        }

    def save(self, commit=True):
        self.cleaned_data["group_id"] = models.Group.objects.get(groupname="admin").id
        self.cleaned_data["is_superadmin"] = True

        super(UserFirstCreateForm, self).save(commit)


class PasswdChangeForm(forms.Form):
    old_passwd = forms.CharField(label='Old Password', widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'id': 'old-passwd',
    })) 
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
        to update personal password
        """
        hasher = SaltMD5PasswordHasher()
        old_pass_res = hasher.verify(cleaned_data['old_passwd'], user_dict['password'])
        if old_pass_res:
            new_password = hasher.encoding(cleaned_data['new_passwd'])
            new_pass_res = hasher.verify(cleaned_data['new_passwd_confirm'], new_password)
            if new_pass_res:
                cleaned_data['password'] = new_password
            else:
                self.add_error('new_passwd_confirm','error')
        else:
            self.add_error('old_passwd', 'old password error')

        return cleaned_data

    def save(self, user_dict):
        """
        :param user_dict:
        :return:
        """
        self.cleaned_data = self.mix_passwd_compare(self.cleaned_data, user_dict)
        if not self.errors:
            uid = user_dict['id']
            new_obj = models.User.objects.filter(id=uid).first()
            new_obj.password = self.cleaned_data['password']
            new_obj.save()


class UserSettingForm(forms.ModelForm):
    """
    give a form to config personal information
    """
    group_all = models.Group.objects.all()
    group_all_tuple = [(group.id, group.groupname) for group in group_all]
    
    group_id = forms.CharField(required=False, )
    class Meta:
        fields = ["username", "email", "phone", "head_pic_url", "person_name",
                  "birth_date", "card_id", "introduce"]

        model = models.User

        help_texts = {
            "username": "*",
            "email": "*",
            "phone": "*",
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
        #super(UserSettingForm, self).save(commit)
        if not self.cleaned_data["group_id"]:
            self.add_error('group_id','not empty')
            return
        user_obj = models.User.objects.get(id=self.instance.id)
        user_obj.username = self.cleaned_data["username"]
        user_obj.email = self.cleaned_data["email"]
        user_obj.phone = self.cleaned_data["phone"]
        user_obj.head_pic_url = self.cleaned_data["head_pic_url"]
        user_obj.person_name = self.cleaned_data["person_name"]
        user_obj.birth_date = self.cleaned_data["birth_date"]
        user_obj.card_id = self.cleaned_data["card_id"]
        user_obj.introduce = self.cleaned_data["introduce"]
        user_obj.group_id = self.cleaned_data["group_id"]
        user_obj.save()



        user_id = int(request.session['user']['id'])

        
        user_dict = user_obj.__dict__
        # user_dict.pop["group"]
        

        user_dict['birth_date'] = date_to_string(user_dict['birth_date'])
        user_dict['instaff_date'] = date_to_string(user_dict['instaff_date'])
        user_dict['groupname'] = user_obj.group.groupname
        if user_dict.get("_state"):
            del user_dict['_state']
        if user_dict.get("_group_cache"):
            del user_dict['_group_cache']
        request.session['user'] = user_dict


class AccountCreateForm(UserCreateForm):
    '''

    default_password: 123456
    '''

    group_all = models.Group.objects.all()
    group_all_tuple = [(group.id, group.groupname) for group in group_all]
    group = forms.ChoiceField(initial='', choices=group_all_tuple, widget=forms.Select(attrs={
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
    def save(self):
        groupname = self.instance.groupname
        g_obj = models.Group.objects.filter(groupname=groupname)
        if g_obj:
            self.add_error('groupname','is repeated')
        else:
            super(GroupCreateForm, self).save()
        

class EmployeeCreateForm(forms.Form):
    employee_num = forms.CharField(label="employee num", required=True)
    userid = forms.CharField(label="wechat id", required=True)
    name = forms.CharField(label="name", required=True)
    email = forms.CharField(label="email", required=True)
    mobile = forms.CharField(label="phone num", required=True)
