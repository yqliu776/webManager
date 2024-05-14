from extensions import db

class AdminModel(db.Model):
    """
    管理员 数据表 模型
    属性：id， adminname， password， nickname， brief， email， avatar， permission, status
    """
    __tablename__ = 'admin'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    adminname = db.Column(db.String(200))
    password = db.Column(db.String(200))
    nickname = db.Column(db.String(200))
    brief = db.Column(db.String(200))
    email = db.Column(db.String(200))
    avatar = db.Column(db.String(200))
    permission = db.Column(db.Integer)
    status = db.Column(db.Integer, default=1)  # 默认值为1表示正常

    def __init__(self, adminname, password, avatar, permission, status=1):
        """
        初始化管理员对象
        :param adminname: 管理员用户名
        :param password: 管理员密码
        :param avatar: 管理员头像
        :param permission: 管理员权限
        :param status: 管理员状态 (1: 正常, 0: 封禁)
        """
        self.adminname = adminname
        self.password = password
        self.avatar = avatar
        self.permission = permission
        self.status = status

    def to_dict(self):
        """
        将管理员对象转换为字典格式
        :return: 管理员对象的字典表示
        """
        return {
            'id': self.id,
            'adminname': self.adminname,
            'nickname': self.nickname,
            'email': self.email,
            'permission': self.permission,
            'status': self.status
        }

    def __repr__(self):
        """
        管理员对象的字符串表示
        :return: 管理员用户名的字符串表示
        """
        return '<User %s>' % self.adminname
