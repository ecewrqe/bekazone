from users.auth import login_required
from django.shortcuts import render
from bekazone.utils import page_not_found
from configparser import ConfigParser
import datetime

@login_required(login_url_name='users:login')
def index(request):
    now_date = datetime.date.today().strftime("%Y/%m/%d")
    now_time = datetime.datetime.now().strftime("%H:%M:%S")
    user_dict = request.session.get('user')
    groupname = user_dict["groupname"]
    

    return render(request, 'index.html', locals())


