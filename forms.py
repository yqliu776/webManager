# 表单验证
from wtforms.validators import length
import wtforms


class AdminLoginForm(wtforms.Form):
    """
    admin 登陆 表单
    """
    adminname = wtforms.StringField(validators=[length(min=3, max=25)])
    password = wtforms.StringField(validators=[length(min=6, max=16)])


class AdminAddForm(wtforms.Form):
    """
    admin 添加 表单
    """
    adminname = wtforms.StringField(validators=[length(min=3, max=25)])
    password = wtforms.StringField(validators=[length(min=6, max=16)])
    Permission = wtforms.StringField(validators=[length(min=1, max=100)])


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
