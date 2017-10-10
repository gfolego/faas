import os
from flask import Blueprint, make_response, request, send_from_directory
from subprocess import call
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = '/tmp'
ALLOWED_EXTENSIONS = set(['pdf'])

mod = Blueprint(r'faas_v1', __name__, url_prefix='/v1')


@mod.route('/', methods=['POST'])
def upload_folha():
    if 'file' in request.files:
        f = request.files['file']
        if f.filename.rsplit('.', 1)[1].lower() not in ALLOWED_EXTENSIONS:
            response = make_response('', 400)
        else:
            filename = secure_filename(f.filename)
            in_file = os.path.join(UPLOAD_FOLDER, filename)
            f.save(in_file)
            out_file = os.path.join(UPLOAD_FOLDER, 'outfile.pdf')
            call(['bash', 'src/faas.sh', in_file, out_file])
            response = send_from_directory(UPLOAD_FOLDER, 'outfile.pdf')
    else:
        response = make_response('', 400)
    return response

