#--coding:utf8--

from __future__ import absolute_import
from __future__ import unicode_literals

from users.auth import login_required
from django.shortcuts import render
from bekazone.utils import page_not_found
import datetime

@login_required(login_url_name='users:login')
def index(request):
    now_date = datetime.date.today().strftime("%Y年%m月%d日".encode("utf8"))
    now_time = datetime.datetime.now().strftime("%H:%M:%S".encode("utf8"))
    return render(request, 'index.html', locals())


