from blueprints import admin_bp, debug_bp
from flask_restful import Api
from api_models import Admins, Admin


def bp_register(app):
    """
    注册蓝图
    :param app:
    :return:
    """
    app.register_blueprint(admin_bp)
    app.register_blueprint(debug_bp)


def api_register(app):
    """
    创建API
    """
    api = Api(app)
    api.add_resource(Admins, '/api/admins')
    api.add_resource(Admin, '/api/admins/<int:admin_id>')
