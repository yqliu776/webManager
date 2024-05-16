from extensions import db


class OrderModel(db.Model):
    """
    订单 数据表 模型
    属性：id, order_number, user_id, total_price, status, created_at, updated_at
    """
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    order_number = db.Column(db.String(200), unique=True, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(50), nullable=False, default='pending')  # 状态:created, pending, completed, cancelled
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    def __init__(self, order_number, user_id, total_price, status='created'):
        """
        初始化订单对象
        :param order_number: 订单编号
        :param user_id: 用户ID
        :param total_price: 总价格
        :param status: 订单状态 (默认: pending)
        """
        self.order_number = order_number
        self.user_id = user_id
        self.total_price = total_price
        self.status = status

    def to_dict(self):
        """
        将订单对象转换为字典格式
        :return: 订单对象的字典表示
        """
        return {
            'id': self.id,
            'order_number': self.order_number,
            'user_id': self.user_id,
            'total_price': self.total_price,
            'status': self.status,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

    def __repr__(self):
        """
        订单对象的字符串表示
        :return: 订单编号的字符串表示
        """
        return '<Order %s>' % self.order_number
