from extensions import db


class ProductModel(db.Model):
    """
    商品 数据表 模型
    属性：id， product_code， product_name， product_price， product_description， product_image， product_type， included_products， product_stock
    """
    __tablename__ = 'product'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_code = db.Column(db.String(200))
    product_name = db.Column(db.String(200))
    product_price = db.Column(db.Float)
    product_description = db.Column(db.String(500))
    product_image = db.Column(db.String(500))
    product_type = db.Column(db.String(50))  # 'regular' 表示常规商品, 'bundle' 表示套餐商品
    included_products = db.Column(db.Text, nullable=True)  # 套餐包含的商品，以JSON格式存储
    product_stock = db.Column(db.Integer, nullable=False, default=0)  # 商品库存

    def __init__(self, product_code, product_name, product_price, product_description, product_image, product_type, product_stock, included_products=None):
        """
        初始化商品对象
        :param product_code: 商品代码
        :param product_name: 商品名称
        :param product_price: 商品价格
        :param product_description: 商品描述
        :param product_image: 商品图片（url）
        :param product_type: 商品类型 ('regular' 表示常规商品, 'bundle' 表示套餐商品)
        :param product_stock: 商品库存数量
        :param included_products: 套餐包含的商品（适用于套餐商品），以JSON格式存储
        """
        self.product_code = product_code
        self.product_name = product_name
        self.product_price = product_price
        self.product_description = product_description
        self.product_image = product_image
        self.product_type = product_type
        self.product_stock = product_stock
        self.included_products = included_products

    def to_dict(self):
        """
        将商品对象转换为字典格式
        :return: 商品对象的字典表示
        """
        return {
            'id': self.id,
            'product_code': self.product_code,
            'product_name': self.product_name,
            'product_price': self.product_price,
            'product_description': self.product_description,
            'product_image': self.product_image,
            'product_type': self.product_type,
            'included_products': self.included_products,
            'product_stock': self.product_stock
        }

    def __repr__(self):
        """
        商品对象的字符串表示
        :return: 商品名称的字符串表示
        """
        return '<Product %s>' % self.product_name
