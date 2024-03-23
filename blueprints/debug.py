from flask import Blueprint, url_for, render_template

bp = Blueprint('debug', __name__, url_prefix='/debug')


@bp.route('/')
def debug():
    print(url_for('main.index'))
    print(url_for('user.login'))
    print(url_for('admin.login'))
    print(url_for('admin.index'))
    return render_template('debug/debug.html')
