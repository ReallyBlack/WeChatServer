from flask import Blueprint
from flask import render_template, request

views_bp = Blueprint('wms', __name__)


@views_bp.route('/')
def index():
    if request.headers.get('token', None) is None:
    context = { ss"user": 'zhouxu'}
    return render_template('index.html', context=context)