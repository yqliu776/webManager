from datetime import datetime
from extensions import db


class MemberModel(db.Model):
    """
    会员 数据表 模型
    属性：id, card_number, phone_number, membership_level, account_points,
          member_name, gender, account_balance, recharge_record
    """
    __tablename__ = 'member'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    card_number = db.Column(db.String(4), unique=True, nullable=False)  # 假设会员卡号长度固定为4位
    phone_number = db.Column(db.String(11), unique=True, nullable=False)
    membership_level = db.Column(db.Integer, default=0)
    account_points = db.Column(db.Integer, default=0)
    member_name = db.Column(db.String(200), nullable=False)
    gender = db.Column(db.Integer, default=-1)  # 默认值为-1
    account_balance = db.Column(db.Integer, default=0)
    cumulative_points = db.Column(db.Integer, default=0)
    recharge_record = db.Column(db.Text)  # 时间+金额的字符串记录

    def __init__(self, card_number, phone_number, member_name, gender, membership_level=0):
        """
        初始化会员实例
        :param card_number: 会员卡号
        :param phone_number: 手机号码
        :param member_name: 会员姓名
        :param gender: 性别
        :param membership_level: 会员等级，默认为0
        """
        self.card_number = card_number.zfill(4)  # 确保卡号是4位数字，前面补零
        self.phone_number = phone_number
        self.member_name = member_name
        self.gender = gender
        self.membership_level = membership_level

    def to_dict(self):
        """
        将会员信息转换为字典格式，方便转换成前端需要的格式
        """
        return {
            'id': self.id,
            'card_number': self.card_number,
            'phone_number': self.phone_number,
            'membership_level': self.membership_level,
            'account_points': self.account_points,
            'member_name': self.member_name,
            'gender': self.gender,
            'account_balance': self.account_balance,
            'cumulative_points': self.cumulative_points,
            'recharge_record': self.recharge_record
        }

    def __repr__(self):
        return '<Member %s>' % self.card_number

    def add_recharge_record(self, amount):
        """
        添加会员充值记录
        :param amount: 充值金额
        """
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        record = f"{timestamp}+{amount};"
        if self.recharge_record:
            self.recharge_record += record
        else:
            self.recharge_record = record



