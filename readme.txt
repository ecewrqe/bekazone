** bekazone templates platform usage explainment
-- version: 1.0.1
-- python_vertion: 3.5.0
-- django_version: 1.11.5

must be install:
django 1.11.5, pillow, pymysql, six, beautifulSoup4 4.4.0

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

=================================
beka_admin
in app of cadmin

config app->_admin.py

from cadmin import baseadmin
class SimpleAdmin(baseadmin.create_admin())
    ....

baseadmin.site.register(<model>, <admin>)

config_item:
    list_display  指定展示的列数
    list_filter   指定想筛选的列数
    search_fields  选择想要搜索的列数
    order_fields  *以list_display为基础，选择那些列需要排序
    list_per_page  一页显示多少行
    list_editable  指定哪些字段需要在页面上直接修改
    
    model_change_form  指定更改一条数据的自定义表单，默认为系统指定
    model_add_form  指定添加一条数据的自定义表单，默认为系统指定
    actions  指定需要让选中的那些项执行什么函数，默认有删除

    

=================================
bekablog
/blog-backend/edit-blog/  blog_backend:edit_blog
/blog-backend/message/  blog_backend:message
/blog-backend/normal-edit-blog/  blog_backend:normal_edit_blog
/blog-backend/md-edit-blog/  blog_backend:md_edit_blog

/blog-backend/display-blog-list/  blog_backend:display_blog_list
/blog-backend/verify-kind/  blog_backend:verify_kind
/blog-backend/kind-list/  blog_backend:kind_list
/blog-backend/kind-delete/  blog_backend:kind_delete
/blog-backend/tag-list/  blog_backend:tag_list
/blog-backend/verify-tag/  blog_backend:verify_tag
/blog-backend/tag-delete/  blog_backend:tag_delete
/blog-backend/blog-title-verify/  blog_backend:blog_title_verify
/blog-backend/blog-delete/  blog_backend:blog_delete
/blog-backend/get-blog-message/  blog_backend:get_blog_message


blog: 
a piece of blog:
title, blog_content, md_content, blog_kind(group), tag, creator, ,create_date, adjustment_date

blog_kind
name, alias, introdution, create_date

tag: used to search
name

blog edit/blog list display/create blog kind/blog index
create: message?normal_blog?technology_blog?
normal_blog/technology_blog
message   normal_editor
normal_blog  title+normal_editor+group_select+tag
technology_blog  title+md_editor+group_select+tag


tinymce(used: normal_blog/message)
https://www.tiny.cloud/docs/

toolbar: formatselect, bold, italic, strikethrough, underline, forecolor, backcolor, link, alignleft, aligncenter, alignright, alignjustify, outdent, indent, removeformat, numlist, bullist

plugin tool: print, preview, fullscreen, image, media, link, codesample, table, charmap, hr, advlist, lists

list, advlist-> numlist, bullist
link -> link

unimportant plugin tool: template, pagebreak, nonbreaking, toc, insertdatetime, tinymcespellchecker, a11ychecker
never effect: autolink, directionality, fullpage, textpattern, imagetools
network is necessary:advcode, powerpaste

get content
tinyMCE.activeEditor.getContent();
tinyMCE.activeEditor.getContent({format : 'raw'});
tinyMCE.get('message').getContent();

set content
tinyMCE.activeEditor.setContent(`
<!DOCTYPE html>
<html>
<head>
</head>
<body>
<p>dddddd</p>
</body>
</html>
`, {format : 'raw'});
tinyMCE.get('my_editor').setContent(data);

editmd(used: technology_blog)
http://pandao.github.io/editor.md/examples/



1, edit_blog page select
3, new normal blog
4, new markdown blog
5, editmd control and tinymce control

6, blog table: create blog/modificate blog/recycle blog/delete blog/search blog/filter blog/order blog/ create blog kind/
7, recycle bin
8, blog kind table:
9, blog type

8, blog display page: index/message/normal blog/markdown blog/





1, blog form
2, blog managable table design
3, blog display pages design

model 模型、データベース表の模型
mode/modal 様式、方法、やり方、



