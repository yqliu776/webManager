from app.moduls import AdminModel
from flask import jsonify
from extensions import db
from flask_restful import Resource


class Admins(Resource):
    @staticmethod
    def get():
        admins = AdminModel.query.all()
        return jsonify([admin.to_dict() for admin in admins])


class Admin(Resource):
    @staticmethod
    def delete(admin_id):
        admin = AdminModel.query.get_or_404(admin_id)
        db.session.delete(admin)
        db.session.commit()
        return jsonify(message='Admin deleted.')
