
from django.conf.urls import url
from users.views import web_views

urlpatterns = [
    url('^login/$', web_views.login, name='login'),
    url('^logout/$', web_views.logout, name='logout'),
    url('^system_init/$', web_views.system_init, name='system_init'),
    url('^change-passwd/$', web_views.change_passwd, name='change-passwd'),
    url('^setting/user_setting/$', web_views.user_setting, name='user_setting'),

    url('^setting/$', web_views.setting, name='setting'),
    url('^head_pic_upload/$', web_views.head_pic_upload, name='head_pic_upload'),
    url('^head_pic/$', web_views.get_head_pic, name='head_pic'),
    url('^account-reg/$', web_views.account_reg, name='account-reg'),
    url('^account-list/$', web_views.account_list, name='account-list'),
    url('^group-create/$', web_views.group_create, name='group-create'),
    url('^group-list/$', web_views.group_list, name='group-list'),
]