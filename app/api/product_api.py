import logging
import os
from flask import jsonify, request
from flask_restful import Resource
from extensions import db
from app.models import ProductModel

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


class Products(Resource):
    @staticmethod
    def get():
        """
        获取所有商品数据，支持分页和搜索
        :return: JSON格式的商品列表
        """
        # 获取分页参数
        page = request.args.get('page', 1, type=int)
        limit = request.args.get('limit', 10, type=int)
        search = request.args.get('search', '')

        # 查询商品数据
        query = ProductModel.query

        if search:
            search = f"%{search}%"
            query = query.filter(
                (ProductModel.product_code.like(search)) |
                (ProductModel.product_name.like(search))
            )

        total = query.count()
        products = query.offset((page - 1) * limit).limit(limit).all()

        # 构建响应数据
        result = {
            'total': total,
            'rows': [product.to_dict() for product in products]
        }

        logger.info(f'Fetched page {page} of products with limit {limit}, search: "{search}"')
        return jsonify(result)

    @staticmethod
    def post():
        """
        添加新的商品
        :return: 添加操作结果的消息
        """
        data = request.json
        new_product = ProductModel(
            product_code=data['product_code'],
            product_name=data['product_name'],
            product_price=data['product_price'],
            product_description=data['product_description'],
            product_image=data['product_image'],
            product_type=data['product_type'],
            product_stock=data['product_stock'],
            included_products=data.get('included_products')
        )
        db.session.add(new_product)
        db.session.commit()
        logger.info(f'Added new product: {new_product.product_name}')
        return jsonify(message='Product added successfully.'), 201


class Product(Resource):
    @staticmethod
    def get(product_id):
        """
        获取指定ID的商品数据
        :param product_id: 商品ID
        :return: JSON格式的商品信息
        """
        product = ProductModel.query.get_or_404(product_id)
        logger.info(f'Fetched product with ID {product_id}')
        return jsonify(product.to_dict())

    @staticmethod
    def put(product_id):
        """
        更新指定ID的商品信息
        :param product_id: 商品ID
        :return: 更新操作结果的消息
        """
        product = ProductModel.query.get_or_404(product_id)
        data = request.json
        product.product_code = data.get('product_code', product.product_code)
        product.product_name = data.get('product_name', product.product_name)
        product.product_price = data.get('product_price', product.product_price)
        product.product_description = data.get('product_description', product.product_description)
        product.product_image = data.get('product_image', product.product_image)
        product.product_type = data.get('product_type', product.product_type)
        product.product_stock = data.get('product_stock', product.product_stock)
        product.included_products = data.get('included_products', product.included_products)
        db.session.commit()
        logger.info(f'Updated product with ID {product_id}')
        return jsonify(message='Product updated successfully.')

    @staticmethod
    def delete(product_id):
        """
        删除指定ID的商品
        :param product_id: 商品ID
        :return: 删除操作结果的消息
        """
        product = ProductModel.query.get_or_404(product_id)
        db.session.delete(product)
        db.session.commit()
        logger.info(f'Deleted product with ID {product_id}')
        return jsonify(message='Product deleted.')
