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


from faas import app
from process import pipeline, FMT_STR

import os
from flask import request, redirect, send_from_directory, after_this_request, render_template
from werkzeug.utils import secure_filename

import tempfile
import shutil

from distutils.util import strtobool
from datetime import datetime


# Definitions
TMPPATH = '/tmp'
OUTFILE='faas.pdf'

ALLOWED_EXTENSIONS = set(['pdf'])

app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024 # 1 MB


def parse_form(form):
    form = form.to_dict()
    if 'dashed' in form:
        form['dashed'] = bool(strtobool(form['dashed']))
    if 'debug' in form:
        form['debug'] = bool(strtobool(form['debug']))
    if 'variation' in form:
        form['variation'] = int(form['variation'])
    if 'start' in form:
        datetime.strptime(form['start'], FMT_STR)
    if 'end' in form:
        datetime.strptime(form['end'], FMT_STR)

    return form


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['POST'])
def upload_file():
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

		filename = secure_filename(file.filename)
		infile = os.path.join(tmppath, filename)
		outfile = os.path.join(tmppath, OUTFILE)
		file.save(os.path.join(tmppath, filename))

		srcpath = os.path.dirname(os.path.realpath(__file__))

                # Ready to accept new arguments
                options = parse_form(request.form)
                pipeline(infile, outfile, **options)

		@after_this_request
		def cleanup(response):
			shutil.rmtree(tmppath)
			return response

		return send_from_directory(tmppath, OUTFILE, as_attachment=True)


@app.route('/', methods=['GET'])
def web_interface():
    return render_template('index.html')

