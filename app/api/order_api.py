import logging
import os
from flask import jsonify, request
from flask_restful import Resource
from extensions import db
from app.models import OrderModel

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


class Orders(Resource):
    @staticmethod
    def get():
        """
        获取所有订单数据，支持分页和搜索
        :return: JSON格式的订单列表
        """
        # 获取分页参数
        page = request.args.get('page', 1, type=int)
        limit = request.args.get('limit', 10, type=int)
        search = request.args.get('search', '')

        # 查询订单数据
        query = OrderModel.query

        if search:
            search = f"%{search}%"
            query = query.filter(
                (OrderModel.order_number.like(search)) |
                (OrderModel.user_id.like(search))
            )

        total = query.count()
        orders = query.offset((page - 1) * limit).limit(limit).all()

        # 构建响应数据
        result = {
            'total': total,
            'rows': [order.to_dict() for order in orders]
        }

        logger.info(f'Fetched page {page} of orders with limit {limit}, search: "{search}"')
        return jsonify(result)

    @staticmethod
    def post():
        """
        添加新的订单
        :return: 添加操作结果的消息
        """
        data = request.json
        new_order = OrderModel(
            order_number=data['order_number'],
            user_id=data['user_id'],
            total_price=data['total_price'],
            status=data.get('status', 'pending')
        )
        db.session.add(new_order)
        db.session.commit()
        logger.info(f'Added new order: {new_order.order_number}')
        return jsonify(message='Order added successfully.'), 201


class Order(Resource):
    @staticmethod
    def get(order_id):
        """
        获取指定ID的订单数据
        :param order_id: 订单ID
        :return: JSON格式的订单信息
        """
        order = OrderModel.query.get_or_404(order_id)
        logger.info(f'Fetched order with ID {order_id}')
        return jsonify(order.to_dict())

    @staticmethod
    def put(order_id):
        """
        更新指定ID的订单信息
        :param order_id: 订单ID
        :return: 更新操作结果的消息
        """
        order = OrderModel.query.get_or_404(order_id)
        data = request.json
        order.order_number = data.get('order_number', order.order_number)
        order.user_id = data.get('user_id', order.user_id)
        order.total_price = data.get('total_price', order.total_price)
        order.status = data.get('status', order.status)
        db.session.commit()
        logger.info(f'Updated order with ID {order_id}')
        return jsonify(message='Order updated successfully.')

    @staticmethod
    def delete(order_id):
        """
        删除指定ID的订单
        :param order_id: 订单ID
        :return: 删除操作结果的消息
        """
        order = OrderModel.query.get_or_404(order_id)
        db.session.delete(order)
        db.session.commit()
        logger.info(f'Deleted order with ID {order_id}')
        return jsonify(message='Order deleted.')
