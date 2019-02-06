** bekazone templates platform usage explainment
-- version: 1.0.1
-- python_vertion: 3.5.0
-- django_version: 1.11.5

must be install:
django 1.11.5, pillow, pymysql, six

verification the path and a empty file
users/migrations/__init__.py
create databaes:
1, config  etc/bekazone/config.conf->[mysql]->name/user/password/host/port
2, create database
3, initial
python manage.py makemigrations
python manage.py migrate

start up server and set admin user
python manage.py runserver localhost:8888 ->
/users/system_init/
default groups: admin & normal

logger setting
etc/bekazone/config.conf
[logger]
...

log_path=var/logs
log_file=access.log

log_name=root
format='%%(asctime)s %%(levelname)s %%(message)s'
#screen_format='%%(asctime)s %%(levelname)s %%(message)s'
#file_format='%%(asctime)s %%(levelname)s %%(message)s'
date_fmt=
screen_level=DEBUG
file_level=DEBUG

"log_path" indicate the log path
"log_file" indicate the log file name
"format" indicate the log output format
"date_fmt" indicate date format in the log output format
"screen_level" & "file_level" separate the output method to set level

level: debug, info, warning, error, critical

the project named bekazone, is based django environment
operative template platform, have a lot of base code snippets

folder structure:
--app
    - cadmin
    - users
--code snipets
    - bekazone
    - common
--html
    - static
    - templates
--config
    - etc
    - var

url_file:
    bekazone/urls.py
    cadmin/urls.py
    users/urls/web_urls.py
url_list:
    - / index
    - /users/login/  users:login
    - /users/logout/  users:logout
    - /users/system_init/  users:system_init
    - /users/change-password/  users:change-password
    - /users/setting/  users:setting
    - /users/head_pic_upload/  users:head_pic_upload
    - /users/head_pic/  users:head_pic
    - /users/account-reg/  users:account-reg
    - /users/account-list/  users:account-list
    - /users/group-create/  users:group-create
    - /users/group-list/  users:group-list

    - /cadmin/  cadmin:index
    - /cadmin/<app>/  cadmin:table_model_list
    - /cadmin/<app>/<table>/  cadmin:table_list
    - /cadmin/<app>/<table>/add/  cadmin:table_add
    - /cadmin/<app>/<table>/<id>/change/  cadmin:table_change
    - /cadmin/<app>/<table>/<id>/delete/  cadmin:table_delete
    - /cadmin/get-action/  cadmin:get_action
    - /cadmin/batch-update/  cadmin:batch_update
    

the project have two app: users and cadmin

"users" app is charged with platform's user system
"cadmin" app is database management system

only is_superadmin is True, can't change its group



other:
bekazone is slave of django configure files
etc have configure files of the platform's


