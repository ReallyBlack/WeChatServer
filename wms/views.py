from flask import Blueprint
from flask import render_template

views_bp = Blueprint('wms', __name__)


@views_bp.route('/')
def index():
    context = { "user": 'zhouxu'}
    return render_template('index.html', context=context)