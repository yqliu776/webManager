from flask import Blueprint, render_template, request, session, redirect, url_for, flash, current_app
from moduls import AdminModel
from sqlalchemy.sql import exists
from forms import AdminLoginForm, AdminProfileForm, AdminAddForm
from werkzeug.security import check_password_hash, generate_password_hash
from exts import db
import os

bp = Blueprint('admin', __name__, url_prefix='/admin')


@bp.route('/index')
def index():
    if 'admin_id' in session:
        admin_id = session.get('admin_id')
        admin = AdminModel.query.filter_by(id=admin_id).first()
        return render_template('index.html', admin=admin)
    else:
        return redirect(url_for('admin.login'))


@bp.route('/main')
def main():
    money = 17465
    user = 25
    download = 5
    message = 1121

    li_main = [money, user, download, message]
    return render_template('lyear_main.html', li_main=li_main)


@bp.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'admin_id' in session:
        admin_id = session.get('admin_id')
        admin = AdminModel.query.filter_by(id=admin_id).first()
        if request.method == 'POST':
            form = AdminProfileForm(request.form)
            if form.validate():
                # 从表单获取数据
                nickname = request.form.get('nickname')
                email = request.form.get('email')
                brief = request.form.get('brief')
                # 更新管理员信息
                admin.nickname = nickname
                admin.email = email
                admin.brief = brief
                db.session.commit()  # 提交更改

                flash('个人资料已更新！')
                return render_template('pages/lyear_pages_profile.html', admin=admin, success=True)
            else:
                flash('邮箱格式错误或昵称简介字数过多！')
                return render_template('pages/lyear_pages_profile.html', admin=admin, success=False)
        # 如果是 GET 请求，或者 POST 请求处理完毕后，渲染个人资料页面
        return render_template('pages/lyear_pages_profile.html', admin=admin)
    else:
        # 如果用户未登录，重定向到登录页面
        return redirect(url_for('admin.login'))


@bp.route('/edit_pwd', methods=['GET', 'POST'])
def edit_pwd():
    if request.method == 'GET':
        if 'admin_id' in session:
            return render_template('pages/lyear_pages_edit_pwd.html')
        else:
            return render_template('pages/lyear_pages_login.html')
    else:
        old_password = request.form['oldpwd']
        new_password = request.form['newpwd']
        confirm_password = request.form['confirmpwd']
        admin_id = session.get('admin_id')
        admin = AdminModel.query.get(admin_id)
        if not admin_id:
            return render_template('pages/lyear_pages_edit_pwd.html', success=False)

        if not old_password or not new_password or not confirm_password:
            flash('密码不能为空。')
            return render_template('pages/lyear_pages_edit_pwd.html', success=False)

        if not admin or not check_password_hash(admin.password, old_password):
            flash('旧密码错误。')
            return render_template('pages/lyear_pages_edit_pwd.html', success=False)

        if new_password != confirm_password:
            flash('两次输入的新密码不一致。')
            return render_template('pages/lyear_pages_edit_pwd.html', success=False)

        if old_password == confirm_password:
            flash('新密码不能与旧密码相同。')
            return render_template('pages/lyear_pages_edit_pwd.html', success=False)

        admin.password = generate_password_hash(new_password)
        db.session.commit()

        flash('密码修改成功。')
        return render_template('pages/lyear_pages_edit_pwd.html', success=True)


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
                flash('没有这个管理员用户!')
                return render_template('pages/lyear_pages_login.html')
            else:
                if admin and check_password_hash(admin.password, password):
                    session['admin_id'] = admin.id
                    session['name'] = admin.adminname
                    session['permission'] = admin.permission
                    return redirect(url_for('admin.index'))
                else:
                    flash('管理员密码错误！')
                    return render_template('pages/lyear_pages_login.html')
        else:
            flash('账户名称或密码格式不对，请检查后重试!')
            return render_template('pages/lyear_pages_login.html')


@bp.route('/add_admin', methods=['GET', 'POST'])
def add_admin():
    """
    Add an administrator
    :return:
    """
    # 如果是 GET 请求，则返回添加管理员的页面
    if request.method == 'GET':
        if 'admin_id' in session:
            if session.get('permission') == 1:
                return render_template('pages/lyear_pages_add_admin.html')
            else:
                flash('用户权限不足！')
                return render_template('pages/lyear_pages_error.html')
        else:
            return render_template('pages/lyear_pages_login.html')
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
                flash('该管理员已经存在！')
                return render_template('pages/lyear_pages_add_admin.html', success=False)
            else:
                hash_pwd = generate_password_hash(password)
                # 创建管理员对象，并将其添加到数据库中
                admin = AdminModel(adminname=adminname, password=hash_pwd, permission=permission, nickname=adminname, brief="", avatar="avatar.jpg")
                db.session.add(admin)
                db.session.commit()
                # 添加成功，返回反馈信息
                flash('添加成功！')
                return render_template('pages/lyear_pages_add_admin.html', success=True)
        else:
            # 如果表单格式不正确，则返回错误页面
            flash('用户名或密码格式错误！')
            return render_template('pages/lyear_pages_add_admin.html', success=False)


@bp.route('/logout')
def logout():
    session.pop('admin_id', None)
    session.pop('permission', None)
    session.pop('name', None)
    return redirect(url_for('admin.index'))


@bp.route('/change_avatar', methods=['POST'])
def change_avatar():
    if 'admin_id' in session:
        admin_id = session.get('admin_id')
        admin = AdminModel.query.filter_by(id=admin_id).first()
        if admin:
            file = request.files.get('avatar')
            if file and allowed_file(file.filename):
                filename = 'Avatar---' + str(admin.id)
                print(filename)
                # 构建保存路径
                save_path = os.path.join(current_app.static_folder, 'images', 'users', filename)
                print(save_path)
                # 保存文件
                file.save(save_path)
                # 更新数据库中的头像信息
                admin.avatar = filename
                db.session.commit()
                flash('头像更新成功！')
                return render_template('pages/lyear_pages_profile.html', success=True, admin=admin)
            else:
                flash('请上传符合要求的图片文件！')
                return render_template('pages/lyear_pages_profile.html', success=False, admin=admin)
    else:
        return redirect(url_for('admin.login'))


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}


'''
@bp.route('/manage_admin', methods=['GET'])
def manage_admin():
    if 'admin_id' in session:
        is_logged_in = True
        return render_template('admin/manage_admin.html', is_logged_in=is_logged_in)
    else:
        return render_template('admin/login_admin.html')

'''
