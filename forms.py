# 表单验证
from wtforms.validators import length, Email
import wtforms


class AdminLoginForm(wtforms.Form):
    """
    admin 登陆 表单
    """
    adminname = wtforms.StringField(validators=[length(min=3, max=25)])
    password = wtforms.StringField(validators=[length(min=6, max=16)])


class AdminProfileForm(wtforms.Form):
    """
    admin 个人信息
    """
    nickname = wtforms.StringField(validators=[length(min=3, max=25)])
    email = wtforms.EmailField(validators=[Email()])
    brief = wtforms.StringField(validators=[length(min=0, max=150)])


class AdminAddForm(wtforms.Form):
    """
    admin 添加 表单
    """
    adminname = wtforms.StringField(validators=[length(min=3, max=25)])
    password = wtforms.StringField(validators=[length(min=6, max=16)])
    Permission = wtforms.IntegerField(validators=[])


class UserLoginForm(wtforms.Form):
    """
    user 登陆 表单
    """
    username = wtforms.StringField(validators=[length(min=3, max=25)])
    password = wtforms.StringField(validators=[length(min=6, max=16)])


class UserRegisterForm(wtforms.Form):
    """
    user 注册 表单
    """
    username = wtforms.StringField(validators=[length(min=3, max=25)])
    password = wtforms.StringField(validators=[length(min=6, max=16)])
