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
from flask import Flask, request, redirect, send_from_directory, after_this_request
from werkzeug.utils import secure_filename

from subprocess import call
import tempfile
import shutil


TMPPATH = '/tmp'
OUTFILE='faas.pdf'
SCRIPT='faas.sh'
ALLOWED_EXTENSIONS = set(['pdf'])

app = Flask(__name__)


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
            tmppath = tempfile.mkdtemp()
            print(tmppath)

            filename = secure_filename(file.filename)
            infile = os.path.join(tmppath, filename)
            outfile = os.path.join(tmppath, OUTFILE)
            file.save(os.path.join(tmppath, filename))

            srcpath = os.path.dirname(os.path.realpath(__file__))
            call(['bash', os.path.join(srcpath, SCRIPT), infile, outfile])

            @after_this_request
            def cleanup(response):
                shutil.rmtree(tmppath)
                return response

            return send_from_directory(tmppath, OUTFILE)

    return '''
    <!doctype html>
    <title>Folha as a Service (FaaS)</title>
    <h1>Folha as a Service (FaaS)</h1>
    <form method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''
