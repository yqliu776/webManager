from app.blueprints import main_bp, admin_bp, debug_bp
from logging.handlers import RotatingFileHandler
from app.api import Products, Product
from app.api import Members, Member
from flask_migrate import Migrate
from app.api import Admins, Admin
from app.api import Orders, Order
from flask_restful import Api
from flask_cors import CORS
from extensions import db
from config import config
from flask import Flask
import logging
import os


def create_app():
    flask_app = Flask(__name__,
                      template_folder='templates',
                      static_folder='static')
    config_name = 'development'
    flask_app.config.from_object(config[config_name])

    # 配置日志文件路径
    if not os.path.exists('app/logs'):
        os.makedirs('app/logs')

    # 配置日志
    log_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    log_file = 'app/logs/app.log'
    file_handler = RotatingFileHandler(log_file, maxBytes=1024 * 1024 * 10, backupCount=5)
    file_handler.setFormatter(log_formatter)
    file_handler.setLevel(logging.INFO)

    # 获取Flask的logger并添加handler
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    logger.addHandler(file_handler)

    logger.info('App starting...')

    # 启用跨域请求
    CORS(flask_app)

    # 注册蓝图
    flask_app.register_blueprint(main_bp)
    flask_app.register_blueprint(admin_bp)
    flask_app.register_blueprint(debug_bp)

    # 注册API
    flask_api = Api(flask_app)
    flask_api.add_resource(Admins, '/api/admins')
    flask_api.add_resource(Admin, '/api/admin/<int:admin_id>')
    flask_api.add_resource(Members, '/api/members')
    flask_api.add_resource(Member, '/api/members/<int:member_id>')
    flask_api.add_resource(Products, '/api/products')
    flask_api.add_resource(Product, '/api/product/<int:product_id>')
    flask_api.add_resource(Orders, '/api/orders')
    flask_api.add_resource(Order, '/api/order/<int:order_id>')

    # 初始化数据库
    db.init_app(flask_app)
    with flask_app.app_context():
        # 只在开发环境中使用 create_all
        if config_name == 'development':
            db.create_all()

    migrate = Migrate(flask_app, db, directory='app/migrations')

    return flask_app
