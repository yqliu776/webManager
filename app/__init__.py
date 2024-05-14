from app.blueprints import main_bp, admin_bp, debug_bp
from flask_migrate import Migrate
from app.api import Admins, Admin
from flask_restful import Api
from extensions import db
from flask import Flask
import config


def create_app():
    app = Flask(__name__,
                template_folder='templates',
                static_folder='static')
    app.config.from_object(config)
    app.register_blueprint(main_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(debug_bp)
    Api(app).add_resource(Admins, '/api/admins')
    Api(app).add_resource(Admin, '/api/admin/<int:admin_id>')

    db.init_app(app)
    with app.app_context():
        db.create_all()

    migrate = Migrate(app, db, directory='app/migrations')
    return app
