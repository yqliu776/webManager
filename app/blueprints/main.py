from flask import Blueprint, render_template, request, session, redirect, url_for, flash, current_app
from sqlalchemy.sql import exists
from app.forms import AdminLoginForm, AdminProfileForm, AdminAddForm
from werkzeug.security import check_password_hash, generate_password_hash
from extensions import db
import os

bp = Blueprint('main', __name__, url_prefix='/')


@bp.route('/')
def index():
    return render_template('index.html')
