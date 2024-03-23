from flask import Blueprint, render_template, request, session, redirect, url_for
from moduls import AdminModel
from forms import AdminLoginForm, AdminAddForm
from werkzeug.security import check_password_hash, generate_password_hash
from exts import db
from sqlalchemy.sql import exists

bp = Blueprint('admin', __name__, url_prefix='/admin')


@bp.route('/index')
def index():
    if 'admin_id' in session:
        is_logged_in = True
    else:
        is_logged_in = False

    return render_template('index.html', is_logged_in=is_logged_in)


@bp.route('/main')
def main():
    return render_template('lyear_main.html')


@bp.route('/profile')
def profile():
    return render_template('pages/lyear_pages_profile.html')


@bp.route('/edit_pwd')
def edit_pwd():
    return render_template('pages/lyear_pages_edit_pwd.html')


@bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    Administrator login。
    :return:
    """
    if request.method == 'GET':
        return render_template('pages/lyear_pages_login.html')
    else:
        form = AdminLoginForm(request.form)
        if form.validate():
            adminname = form.adminname.data
            password = form.password.data
            admin = AdminModel.query.filter_by(adminname=adminname).first()
            if admin is None:
                error = 'NameError：There is no such administrator!'
                return render_template('admin/login_admin.html', error=error)
            else:
                # print(generate_password_hash(password))
                if admin and check_password_hash(admin.password, password):
                    session['admin_id'] = admin.id
                    session['name'] = admin.adminname
                    session['permission'] = admin.permission
                    return redirect(url_for('admin.index'))
                else:
                    error = 'PassWorldError: The administrator password is incorrect!'
                    return render_template('admin/login_admin.html', error=error)
        else:
            error = 'FormatError: Please check your account or password format and try again!'
            return render_template('admin/login_admin.html', error=error)


'''
@bp.route('/logout')
def logout():
    session.pop('admin_id', None)
    session.pop('permission', None)
    session.pop('name', None)
    return redirect(url_for('admin.index'))


@bp.route('/add_admin', methods=['GET', 'POST'])
def add_admin():
    """
    Add an administrator
    :return:
    """
    # 如果是 GET 请求，则返回添加管理员的页面
    if 'admin_id' in session:
        is_logged_in = True
    else:
        is_logged_in = False
    if request.method == 'GET':
        if is_logged_in:
            return render_template('admin/add_admin.html', is_logged_in=is_logged_in)
        else:
            return render_template('admin/index_admin.html', is_logged_in=is_logged_in)
    else:
        # 如果用户权限不足，则返回错误页面
        if session.get('permission') != 0:
            error = 'PermissionError: The permissions are insufficient, please contact the super administrator'
            return render_template('admin/add_admin.html', error=error)
        else:
            # 获取管理员添加表单，并验证表单格式是否正确
            form = AdminAddForm(request.form)
            if form.validate():
                # 获取管理员的姓名、密码和权限等信息
                adminname = form.adminname.data
                password = form.password.data
                permission = form.Permission.data
                # 查询数据库中是否已经存在该管理员
                scalar = db.session.query(exists().where(AdminModel.adminname == adminname))
                if scalar.scalar():
                    # 如果已经存在该管理员，则返回错误页面
                    error = 'NameError: This administrator already exists！'
                    return render_template('admin/add_admin.html', error=error)
                else:
                    # 根据权限字符串转化为数字
                    match permission:
                        case "SuperRoot":
                            permission = 0
                        case "NormalAdmin":
                            permission = 1
                        case "Observer":
                            permission = 2
                        case None:
                            # 如果没有选择管理员权限，则返回错误页面
                            error = 'PermissionError: Please select an administrator privilege level！'
                            return render_template('admin/add_admin.html', error=error)
                    # 对密码进行加密处理
                    hash_pwd = generate_password_hash(password)
                    # 创建管理员对象，并将其添加到数据库中
                    admin = AdminModel(adminname=adminname, password=hash_pwd, permission=permission)
                    db.session.add(admin)
                    db.session.commit()
                    # 添加成功，返回反馈信息
                    feedback = 'Added successfully！'
                    return render_template('admin/add_admin.html', feedback=feedback)
            else:
                # 如果表单格式不正确，则返回错误页面
                error = 'FormatError: The account or password format is incorrect！ '
                return render_template('admin/add_admin.html', error=error)


@bp.route('/manage_admin', methods=['GET'])
def manage_admin():
    if 'admin_id' in session:
        is_logged_in = True
        return render_template('admin/manage_admin.html', is_logged_in=is_logged_in)
    else:
        return render_template('admin/login_admin.html')

'''
