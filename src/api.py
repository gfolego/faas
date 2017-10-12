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
from flask import Flask, request, redirect, send_from_directory, after_this_request, render_template
from werkzeug.utils import secure_filename

from subprocess import call
import tempfile
import shutil

from process import pipeline

import sys
import argparse

# Definitions
HOST='0.0.0.0'
PORT=5000

TMPPATH = '/tmp'
OUTFILE='faas.pdf'
SCRIPT='faas.sh'
ALLOWED_EXTENSIONS = set(['pdf'])

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024 # 1 MB


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
                pipeline(infile, outfile)

		@after_this_request
		def cleanup(response):
			shutil.rmtree(tmppath)
			return response

		return send_from_directory(tmppath, OUTFILE, as_attachment=True)


@app.route('/', methods=['GET'])
def web_interface():
    return render_template('index.html')




def parse_args(argv):
    parser = argparse.ArgumentParser(
            formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('-H', '--host', type=str, default=HOST,
                            help='input server host')
    parser.add_argument('-P', '--port', type=int, default=PORT,
                            help='input server port')
    parser.add_argument('-d', '--debug', action='store_true',
                            help='activate debug mode')

    args = parser.parse_args(args=argv)
    return args


# Main
def main(argv):

    # Parse arguments
    args = parse_args(argv)
    if args.debug: print(args)

    app.run(host=args.host, port=args.port,
            debug=args.debug)

if __name__ == "__main__":
    main(sys.argv[1:])

