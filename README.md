# FileTranStation
a web app help you to download and store file on VPS with given URL.

## Run

0. install neccesary package:

``` bash
sudo apt-get install gunicorn supervisor pip mongodb nginx-extra
pip install Pillow pymongo flask
```

1. Setup nginx:

remove default sites (in DigitalOcean+Ubuntu+Django) : `rm -rf /etc/nginx/sites-enabled/django`

`vi /etc/nginx/sites-enabled/davidlau.me`

``` bash

server
{
    listen 80;
    server_name trans.davidlau.me;
    location / {
        proxy_redirect off;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_pass http://127.0.0.1:8083;
    }
    access_log /var/log/nginx/trans.davidlau.me.log;
}

server
{
    listen 80;
    server_name file.davidlau.me;
    location / {
        proxy_redirect off;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_pass http://127.0.0.1:8082;
    }
    access_log /var/log/nginx/file.davidlau.me.log;
}

server
{
    listen 80;
    server_name image.davidlau.me;
    location / {
        proxy_redirect off;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_pass http://127.0.0.1:8081;
    }
    client_max_body_size 5m;
    access_log /var/log/nginx/image.davidlau.me.log;
}
```

2. Clone and run

``` bash
cd /home/django/
git clone https://github.com/liuslevis/FileTranStation.git
cd FileTranStation
gunicorn -b 0.0.0.0:8083 fileTranStation:app &
```
