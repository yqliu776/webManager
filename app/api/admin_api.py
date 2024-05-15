from app.moduls import AdminModel, MemberModel
from flask import jsonify
from flask import request
from extensions import db
from flask_restful import Resource


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
        return jsonify(message='Admin deleted.')


class Members(Resource):
    @staticmethod
    def get():
        """
        获取所有会员数据，支持分页和搜索
        :return: JSON格式的会员列表
        """
        # 获取分页参数
        page = request.args.get('page', 1, type=int)
        limit = request.args.get('limit', 10, type=int)
        search = request.args.get('search', '')

        # 查询会员数据
        query = MemberModel.query

        if search:
            search = f"%{search}%"
            query = query.filter(
                (MemberModel.card_number.like(search)) |
                (MemberModel.member_name.like(search)) |
                (MemberModel.phone_number.like(search))
            )

        total = query.count()
        members = query.offset((page - 1) * limit).limit(limit).all()

        # 构建响应数据
        result = {
            'total': total,
            'rows': [member.to_dict() for member in members]
        }

        return jsonify(result)

    @staticmethod
    def post():
        """
        添加新的会员
        :return: 添加操作结果的消息
        """
        data = request.json
        new_member = MemberModel(
            card_number=data['card_number'],
            phone_number=data['phone_number'],
            member_name=data['member_name'],
            gender=data['gender'],
            membership_level=data.get('membership_level', 0)
        )
        db.session.add(new_member)
        db.session.commit()
        return jsonify(message='Member added successfully.'), 201


class Member(Resource):
    @staticmethod
    def get(member_id):
        """
        获取指定ID的会员数据
        :param member_id: 会员ID
        :return: JSON格式的会员信息
        """
        member = MemberModel.query.get_or_404(member_id)
        return jsonify(member.to_dict())

    @staticmethod
    def put(member_id):
        """
        更新指定ID的会员信息
        :param member_id: 会员ID
        :return: 更新操作结果的消息
        """
        member = MemberModel.query.get_or_404(member_id)
        data = request.json
        member.card_number = data.get('card_number', member.card_number)
        member.phone_number = data.get('phone_number', member.phone_number)
        member.member_name = data.get('member_name', member.member_name)
        member.gender = data.get('gender', member.gender)
        member.membership_level = data.get('membership_level', member.membership_level)
        member.account_points = data.get('account_points', member.account_points)
        member.account_balance = data.get('account_balance', member.account_balance)
        member.cumulative_points = data.get('cumulative_points', member.cumulative_points)
        db.session.commit()
        return jsonify(message='Member updated successfully.')

    @staticmethod
    def delete(member_id):
        """
        删除指定ID的会员
        :param member_id: 会员ID
        :return: 删除操作结果的消息
        """
        member = MemberModel.query.get_or_404(member_id)
        db.session.delete(member)
        db.session.commit()
        return jsonify(message='Member deleted.')
