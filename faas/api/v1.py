from flask import Blueprint, make_response, request

mod = Blueprint(r'faas_v1', __name__, url_prefix='/v1')


@mod.route('/', methods=['POST'])
def upload_folha():
    if 'file' in request.files:
        response = make_response('', 200)
    else:
        response = make_response('', 400)
    return response

