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
    nickname = db.Column(db.String(200))
    brief = db.Column(db.String(200))
    email = db.Column(db.String(200))
    avatar = db.Column(db.String(200))
    permission = db.Column(db.Integer, primary_key=False, autoincrement=False)

    def __init__(self, adminname, password, nickname, brief, avatar, permission):
        """
        To fix error:__init__() takes 1 positional argument but 4 were given
        :param adminname:
        :param password:
        """
        self.adminname = adminname
        self.password = password
        self.avatar = avatar
        self.permission = permission

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.adminname,
            'name': self.nickname,
            'brief': self.brief,
            'permission': self.permission
        }

    def __repr__(self):
        return '<User %s>' % self.adminname
