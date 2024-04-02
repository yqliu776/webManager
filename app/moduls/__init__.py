import os
import sys

current_dir = os.path.abspath(os.path.dirname(__file__))
sys.path.append(current_dir)
from app.moduls.admin_model import AdminModel
from app.moduls.member_model import MemberModel
