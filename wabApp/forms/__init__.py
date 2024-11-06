import os
import sys

current_dir = os.path.abspath(os.path.dirname(__file__))
sys.path.append(current_dir)
from admin_forms import AdminProfileForm, AdminAddForm, AdminLoginForm
from rule_forms import Rules
