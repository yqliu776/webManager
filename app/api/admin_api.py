import logging
import os
from app.models import AdminModel
from flask import jsonify, request
from extensions import db
from flask_restful import Resource

# 配置日志记录器
logger = logging.getLogger('api')
logger.setLevel(logging.INFO)

# 创建文件处理器
if not os.path.exists('app/logs'):
    os.makedirs('app/logs')

file_handler = logging.FileHandler('app/logs/api.log')
file_handler.setLevel(logging.INFO)

# 创建日志格式器并添加到文件处理器
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


class Admins(Resource):
    @staticmethod
    def get():
        """
        获取所有管理员数据，支持分页
        :return: JSON格式的管理员列表
        """
        # 获取分页参数
        page = request.args.get('page', 1, type=int)
        limit = request.args.get('limit', 10, type=int)
        offset = (page - 1) * limit

        # 查询管理员数据
        admins_query = AdminModel.query
        total = admins_query.count()
        admins = admins_query.offset(offset).limit(limit).all()

        # 构建响应数据
        result = {
            'total': total,
            'rows': [admin.to_dict() for admin in admins]
        }

        logger.info(f'Fetched page {page} of admins with limit {limit}')
        return jsonify(result)


class Admin(Resource):
    @staticmethod
    def delete(admin_id):
        """
        删除指定ID的管理员
        :param admin_id: 管理员ID
        :return: 删除操作结果的消息
        """
        admin = AdminModel.query.get_or_404(admin_id)
        db.session.delete(admin)
        db.session.commit()
        logger.info(f'Admin with ID {admin_id} deleted.')
        return jsonify(message='Admin deleted.')
