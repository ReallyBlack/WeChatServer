from flask import Blueprint
from flask import render_template, request, make_response

views_bp = Blueprint('wms', __name__)


@views_bp.route('/')
def index():
    resp = make_response(render_template('index.html'))
    if request.cookies.get('token', None) is None:
        resp.set_cookie('token', 'this is a test token')
    else:
        resp.set_cookie('user', 'zhouxu')
    return resp