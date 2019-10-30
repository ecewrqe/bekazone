** bekazone templates platform usage explainment
-- version: 1.0.1
-- python_vertion: 3.5.0
-- django_version: 1.11.5

このブログは技術者向け、もしくはコンピューターに働いている方へ考えの機能です。便利性を考える。
技術者はたくさん癖があるので、例えば"ctrl+s"セーブ操作、そういうわけで、ctrl+sをブログのセーブ操作に変わろうと考える、例えばテーブルにはctrl+dの削除操作か慣れるので、ボタンの関心は少なくなる。

### 配置
必ずインストールしするパッケージは以下
django 1.11.5, pillow, pymysql, six

verification the path and a empty file
users/migrations/__init__.py
create databaes:
1, config  etc/bekazone/config.conf->[mysql]->name&user&password&host&port
2, create database
3, initial
python manage.py makemigrations
python manage.py migrate
========================
uwsgi,nginx
```
pip3 install uwsgi  # python3 pip3
```
bekazone_uwsgi.ini
```
[uwsgi]
socket = 127.0.0.1:3000   #  <uwsgi port>
chdir = /app/bekazone/    # project root path
#home = /usr/local/python/lib/python3.6
pythonpath = /usr/local/python/lib/python3.6  # この通り
wsgi-file = bekazone/wsgi.py   # project wsgiファイル
processes = 4
threads = 2
```

nginx.conf
```
server {
        listen       80;
        server_name  localhost;

        location / {
            include  uwsgi_params;
            uwsgi_pass  127.0.0.1:9090;              //uwsgi_port
            uwsgi_param UWSGI_SCRIPT demosite.wsgi;  // wsgi file path
            uwsgi_param UWSGI_CHDIR /demosite;       //
            index  index.html index.htm;
            client_max_body_size 35m;
        }
        location /static{
          alias /apps/bekazone/static # project_static_path
        }
    }

```

config path:
/etc/bekazone/config.conf
sections: bekazone, logger, mysql, permission
```
[mysql]
name=bekazone
user=bekazone
password=bekazone
host=localhost
port=3306
```

簡単なdjangoの起動:
```
python manage.py runserver 0.0.0.0:9000
```
nginx and uwsgiの起動は
```
# under the project path
uwsgi bekazone_uwsgi.ini
systemctl start nginx
```

備考:
bekazone is slave of django configure files
etc have configure files of the platform's

=================================
beka_admin 配置
in app of cadmin

config app->_admin.py

from cadmin import baseadmin
class SimpleAdmin(baseadmin.create_admin())
    ....

baseadmin.site.register(<model>, <admin>)
