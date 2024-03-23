from exts import db


class AdminModel(db.Model):
    """
    管理员 数据表 模型
    属性：id， adminname， password······
    """
    __tablename__ = 'admin'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    adminname = db.Column(db.String(200))
    password = db.Column(db.String(200))
    permission = db.Column(db.Integer, primary_key=False, autoincrement=False)

    def __init__(self, adminname, password, permission):
        """
        To fix error:__init__() takes 1 positional argument but 3 were given
        :param adminname:
        :param password:
        """
        self.adminname = adminname
        self.password = password
        self.permission = permission

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.adminname,
            'permission': self.permission
        }

    def __repr__(self):
        return '<User %s>' % self.adminname
