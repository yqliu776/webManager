from app.blueprints import main_bp, admin_bp, debug_bp
from flask_migrate import Migrate
from app.api import Admins, Admin
from app.api import Members, Member
from flask_restful import Api
from extensions import db
from flask import Flask
import config


def create_app():
    flask_app = Flask(__name__,
                      template_folder='templates',
                      static_folder='static')
    flask_app.config.from_object(config)

    # 注册蓝图
    flask_app.register_blueprint(main_bp)
    flask_app.register_blueprint(admin_bp)
    flask_app.register_blueprint(debug_bp)

    flask_api = Api(flask_app)
    flask_api.add_resource(Admins, '/api/admins')
    flask_api.add_resource(Admin, '/api/admin/<int:admin_id>')
    flask_api.add_resource(Members, '/api/members')
    flask_api.add_resource(Member, '/api/members/<int:member_id>')

    # 初始化数据库
    db.init_app(flask_app)
    with flask_app.app_context():
        db.create_all()

    migrate = Migrate(flask_app, db, directory='flask_app/migrations')

    return flask_app


app = create_app()
