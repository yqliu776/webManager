import os
import sys

current_dir = os.path.abspath(os.path.dirname(__file__))
sys.path.append(current_dir)
from admin import bp as admin_bp
from debug import bp as debug_bp
