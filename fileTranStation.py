#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# Setup
# sudo pip install flask 
# install gunicorn
# cd to this location
# python main.py

# or Using gunicorn
# gunicorn -b 0.0.0.0:8083 fileTranStation:app &

# or Using supervisor, set path in supervivsord.conf

import hashlib
import datetime
import flask
import bson.binary
import bson.objectid
import bson.errors
import random
from flask import json
from cStringIO import StringIO
import os
import subprocess

app = flask.Flask(__name__)
app.debug = True

DOWNLOAD_PATH = '/home/django/FileTranStation/download'
DOWNLOAD_PATH_URL = '/FileTranStation/download'

# 日志处理
# 使用：app.logger.[debug|info|warning|error|critical]("MSG") 
import logging
from logging import FileHandler

# DEBUG及以上输出到文件
file_handler = FileHandler('./flask_debug.log')
file_handler.setLevel(logging.DEBUG)

# ERROR输出终端
file_handler_console = logging.StreamHandler() 
file_handler_console.setLevel(logging.ERROR)  
# 日志格式
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")  
file_handler.setFormatter(formatter)  
file_handler_console.setFormatter(formatter)  

app.logger.addHandler(file_handler)
app.logger.addHandler(file_handler_console)

# app.logger.critical( "FAILED to connect mongodb, check wether mongod is running!")


@app.route('/downloadFile', methods=['POST'])
def downloadURL():
    print "Start downloading task: "
    url = str(flask.request.form['intputURL'])
    print "User input URL:"+url

    # wget
    # -Q10K: in case try to download recursively, limit at 10KB size.

    resultText = subprocess.check_output(['wget', str(url), '-Q10K','-directory-prefix',DOWNLOAD_PATH,'-o', 'lastDownload.log'])
    resultURL = DOWNLOAD_PATH_URL
    return flask.render_template('index.html', resultURL=resultURL, resultText=resultText)

# page for user paste download url
@app.route('/')
def index():
    return flask.render_template('index.html')

if __name__ == '__main__':
    print 'FileTranStation is running. Hold Ctrl+C to stop.'
    app.run(port=8083)