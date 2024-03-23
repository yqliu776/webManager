from app import app
from exts import db
from models import AdminModel


def add_admins():
    """
    创建默认管理员
    :return:
    """
    adminname = 'kevin'
    # 090910
    password = 'pbkdf2:sha256:260000$fdcKsqq38OyZ3ind$55da715f09e9131240ead3be598f1efa5a505496fd0130a3372aa0ee76f4c1c2'
    permission = 1

    new_admin = AdminModel(adminname=adminname, password=password, permission=permission)
    db.session.add(new_admin)
    db.session.commit()
    message = 'Success!'
    print(message)


def generate_products(products):
    category_list = ['女装','鞋子', '', '', '', '', '']
    return 1


if __name__ == '__main__':
    app.app_context().push()
    add_admins()
