# Djanurl

基于 Django 的短网址程序.
An English version follows.

## 需求

Django 支持的 Python3 版本

处了`pip install -r requirements.txt`, 还可能需要数据库驱动和 web 服务器

## 提示
1. 请把自定义模板放置于 `templates`;
2. 请将生产环境的配置写在 `djanurl/production.py`;
3. 需要运行 `python manage.py collectstatics`. 这需要设置 `STATIC_ROOT`;
4. 在 `production.py` 设置 `EXPLICIT_REDIRECT = True` 开启显式跳转;
5. 显式跳转模板请创建到自定义模板目录的`surl/redirect.html`, 可参考 surl 这个 app 的模板;
6. 默认开启 i18n 和 i10n, 网站语言根据浏览器/系统语言自动判断.

-------

# Djanurl

A Django based url shortener project. 

## Requirements

This project is written in Python3. It should work well with all the versions that Django supports.

In addition to `pip install -r requirements.txt`, you may also need to install database drivers and http/wsgi servers.

## Some Tips
1. You should put your own templates in the `templates` folder in the project root directory;
2. You may have your production settings set in `djanurl/production.py`
3. You might need to run `python manage.py collectstatics`. In order to do this, you should have `STATIC_ROOT` set in your settings
4. Set `EXPLICIT_REDIRECT = True` in `production.py` to enable explicit redirection
5. Template used in explicit redirection is located at `surl/redirect.html`
6. i18n and i10n is enabled by default. Language code is detected based on browser and os languages.

## 示例部署文件 Example Deployment Files

File 1: `uwsgi.ini`
````
[uwsgi]
socket=/tmp/ovz.im.sock
home=/path/to/virtualenv/
chdir=/path/to/project/
env=DJANGO_SETTINGS_MODULE=djanurl.settings
module=djanurl.wsgi:application
master=True
workers=8
pidfile=/tmp/ovz.im.pid
max-requests=5000
thunder-lock=True
vacuum=True
harakiri=120
````

File 2: `supervisord.conf`
````
....
[program:ovzim]
command = /path/to/uwsgi --ini /path/to/uwsgi.ini
stopsignal=QUIT
autostart=true
autorestart=true
stdout_logfile=/var/logs/ovz.log
redirect_stderr=true
````

File 3: nginx configuration `ovz.im.conf`

````
upstream ovzim {
    server unix:///tmp/ovz.im.sock;
}

server {
    listen 80;
    server_name www.ovz.im;
    return 302 $scheme://ovz.im$request_uri;
}

server {
    listen      80;
    server_name ovz.im;
    charset     utf-8;

    client_max_body_size 75M;

    location /static {
        root /path/to/project/;
    }

    location / {
        uwsgi_pass  ovzim;
        include     uwsgi_params;
    }
}
````