#!/usr/bin/python
# -*- coding: utf-8 -*-


# api.py
# Copyright 2017
#     Fábio Beranizo (fabio.beranizo@gmail.com)
#     Guilherme Folego (gfolego@gmail.com)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.



import os
from flask import Flask, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
from subprocess import call


UPLOAD_FOLDER = '/tmp'
ALLOWED_EXTENSIONS = set(['pdf'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            infile = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            outfile = os.path.join(app.config['UPLOAD_FOLDER'], 'faas.pdf')
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            dir_path = os.path.dirname(os.path.realpath(__file__))
            call(['bash', dir_path + '/faas.sh', infile, outfile])

            return send_from_directory(app.config['UPLOAD_FOLDER'], 'faas.pdf')

    return '''
    <!doctype html>
    <title>Folha as a Service (FaaS)</title>
    <h1>Folha as a Service (FaaS)</h1>
    <form method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''
