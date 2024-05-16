import os
import sys

current_dir = os.path.abspath(os.path.dirname(__file__))
sys.path.append(current_dir)
from app.models.admin_model import AdminModel
from app.models.member_model import MemberModel
from app.models.product_model import ProductModel
from app.models.order_model import OrderModel