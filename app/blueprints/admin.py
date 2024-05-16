import logging
from flask import Blueprint, render_template, request, session, redirect, url_for, flash, current_app
from app.models import AdminModel
from sqlalchemy.sql import exists
from app.forms import AdminLoginForm, AdminProfileForm, AdminAddForm
from werkzeug.security import check_password_hash, generate_password_hash
from extensions import db
import os

# 创建日志记录器
logger = logging.getLogger('admin')
logger.setLevel(logging.INFO)

# 创建文件处理器
if not os.path.exists('app/logs'):
    os.makedirs('app/logs')

file_handler = logging.FileHandler('app/logs/admin.log')
file_handler.setLevel(logging.INFO)

# 创建日志格式器并添加到文件处理器
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

bp = Blueprint('admin', __name__, url_prefix='/admin')


@bp.route('/index')
def index():
    if 'admin_id' in session:
        admin_id = session.get('admin_id')
        admin = AdminModel.query.filter_by(id=admin_id).first()
        logger.info(f'Admin {admin.adminname} accessed index page')
        return render_template('index_admin.html', admin=admin)
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


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('pages_admin/lyear_pages_login.html')
    else:
        form = AdminLoginForm(request.form)
        if form.validate():
            adminname = form.adminname.data
            password = form.password.data
            admin = AdminModel.query.filter_by(adminname=adminname).first()
            if admin is None:
                flash('没有这个管理员用户!')
                logger.warning(f'Failed login attempt for non-existent admin: {adminname}')
                return render_template('pages_admin/lyear_pages_login.html')
            else:
                if admin and check_password_hash(admin.password, password):
                    session['admin_id'] = admin.id
                    session['name'] = admin.adminname
                    session['permission'] = admin.permission
                    logger.info(f'Admin {admin.adminname} logged in successfully')
                    return redirect(url_for('admin.index'))
                else:
                    flash('管理员密码错误！')
                    logger.warning(f'Failed login attempt for admin: {adminname}')
                    return render_template('pages_admin/lyear_pages_login.html')
        else:
            flash('账户名称或密码格式不对，请检查后重试!')
            return render_template('pages_admin/lyear_pages_login.html')


@bp.route('/logout')
def logout():
    adminname = session.get('name')
    session.pop('admin_id', None)
    session.pop('permission', None)
    session.pop('name', None)
    logger.info(f'Admin {adminname} logged out')
    return redirect(url_for('admin.index'))


@bp.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'admin_id' in session:
        admin_id = session.get('admin_id')
        admin = AdminModel.query.filter_by(id=admin_id).first()
        if request.method == 'POST':
            form = AdminProfileForm(request.form)
            if form.validate():
                nickname = request.form.get('nickname')
                email = request.form.get('email')
                brief = request.form.get('brief')
                admin.nickname = nickname
                admin.email = email
                admin.brief = brief
                db.session.commit()
                logger.info(f'Admin {admin.adminname} updated their profile')
                flash('个人资料已更新！')
                return render_template('pages_admin/lyear_pages_profile.html', admin=admin, success=True)
            else:
                flash('邮箱格式错误或昵称简介字数过多！')
                return render_template('pages_admin/lyear_pages_profile.html', admin=admin, success=False)
        return render_template('pages_admin/lyear_pages_profile.html', admin=admin)
    else:
        return redirect(url_for('admin.login'))


@bp.route('/edit_pwd', methods=['GET', 'POST'])
def edit_pwd():
    if request.method == 'GET':
        if 'admin_id' in session:
            return render_template('pages_admin/lyear_pages_edit_pwd.html')
        else:
            return render_template('pages_admin/lyear_pages_login.html')
    else:
        old_password = request.form['oldpwd']
        new_password = request.form['newpwd']
        confirm_password = request.form['confirmpwd']
        admin_id = session.get('admin_id')
        admin = AdminModel.query.get(admin_id)

        if not admin_id:
            logger.warning('Attempt to change password without being logged in')
            return render_template('pages_admin/lyear_pages_login.html')

        if not old_password or not new_password or not confirm_password:
            flash('密码不能为空。', 'danger')
            logger.warning(f'Admin {admin.adminname} provided empty password fields')
            return render_template('pages_admin/lyear_pages_edit_pwd.html')

        if not check_password_hash(admin.password, old_password):
            flash('旧密码错误。', 'danger')
            logger.warning(f'Admin {admin.adminname} provided incorrect old password')
            return render_template('pages_admin/lyear_pages_edit_pwd.html')

        if new_password != confirm_password:
            flash('两次输入的新密码不一致。', 'danger')
            logger.warning(f'Admin {admin.adminname} new password and confirmation do not match')
            return render_template('pages_admin/lyear_pages_edit_pwd.html')

        if old_password == confirm_password:
            flash('新密码不能与旧密码相同。', 'danger')
            logger.warning(f'Admin {admin.adminname} new password is the same as old password')
            return render_template('pages_admin/lyear_pages_edit_pwd.html')

        admin.password = generate_password_hash(new_password)
        db.session.commit()

        flash('密码修改成功。', 'success')
        logger.info(f'Admin {admin.adminname} successfully changed password')
        return render_template('pages_admin/lyear_pages_edit_pwd.html')


@bp.route('/add_admin', methods=['GET', 'POST'])
def add_admin():
    """
    Add an administrator
    :return:
    """
    if request.method == 'GET':
        if 'admin_id' in session:
            if session.get('permission') == 1:
                return render_template('pages_admin/lyear_pages_add_admin.html')
            else:
                flash('用户权限不足！')
                logger.warning(f"Admin ID {session.get('admin_id')} attempted to add an admin without sufficient permissions")
                return render_template('pages_admin/lyear_pages_error.html')
        else:
            logger.warning("Attempt to access add_admin page without being logged in")
            return render_template('pages_admin/lyear_pages_login.html')
    else:
        form = AdminAddForm(request.form)
        if form.validate():
            adminname = form.adminname.data
            password = form.password.data
            permission = form.Permission.data
            scalar = db.session.query(exists().where(AdminModel.adminname == adminname))
            if scalar.scalar():
                flash('该管理员已经存在！', 'danger')
                logger.warning(f"Admin {adminname} already exists")
                return render_template('pages_admin/lyear_pages_add_admin.html')
            else:
                hash_pwd = generate_password_hash(password)
                admin = AdminModel(adminname=adminname, password=hash_pwd, permission=permission, avatar="avatar.jpg")
                db.session.add(admin)
                db.session.commit()
                flash('添加成功！', 'success')
                logger.info(f"Admin {adminname} added successfully by Admin ID {session.get('admin_id')}")
                return render_template('pages_admin/lyear_pages_add_admin.html', redirect_url=url_for('admin.manage_admin'))
        else:
            flash('用户名或密码格式错误！', 'danger')
            logger.warning(f"Admin ID {session.get('admin_id')} provided invalid username or password format for new admin")
            return render_template('pages_admin/lyear_pages_add_admin.html')


@bp.route('/change_avatar', methods=['POST'])
def change_avatar():
    if 'admin_id' in session:
        admin_id = session.get('admin_id')
        admin = AdminModel.query.filter_by(id=admin_id).first()
        if admin:
            file = request.files.get('avatar')
            if file and Rules.allowed_file(file.filename):
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
                flash('头像更新成功！', 'success')
                return render_template('pages_admin/lyear_pages_profile.html', admin=admin)
            else:
                flash('请上传符合要求的图片文件！', 'danger')
                return render_template('pages_admin/lyear_pages_profile.html', admin=admin)
    else:
        return redirect(url_for('admin.login'))


@bp.route('/manage_admin')
def manage_admin():
    if 'admin_id' in session:
        permission = session.get('permission')
        return render_template('pages_admin/lyear_pages_data_admin.html', permission=permission)
    else:
        return render_template(url_for('admin.login'))


@bp.route('/manage_users')
def manage_users():
    if 'admin_id' in session:
        permission = session.get('permission')
        return render_template('pages_admin/lyear_pages_data_member.html', permission=permission)
    else:
        return redirect(url_for('admin.login'))


@bp.route('/orders')
def manage_orders():
    if 'admin_id' in session:
        permission = session.get('permission')
        return render_template('pages_admin/lyear_pages_data_order.html', permission=permission)
    else:
        return redirect(url_for('admin.login'))


class Rules:
    @staticmethod
    def allowed_file(self, filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}
