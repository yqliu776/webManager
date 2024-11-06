import os


class Config:
    # 基础配置
    SECRET_KEY = os.environ.get('SECRET_KEY', 'default_secret_key')
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # 为了减少内存使用量，推荐设置为False
    SQLALCHEMY_ECHO = False  # 是否打印SQL语句，调试时可设为True

    # MySQL数据库配置
    HOSTNAME = os.environ.get('DB_HOSTNAME', 'localhost')
    PORT = os.environ.get('DB_PORT', '3306')
    DATABASE = os.environ.get('DB_DATABASE', 'web_manager')
    USERNAME = os.environ.get('DB_USERNAME', 'root')
    PASSWORD = os.environ.get('DB_PASSWORD', '090910')
    DB_URI = f'mysql+pymysql://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DATABASE}'
    SQLALCHEMY_DATABASE_URI = DB_URI


class DevelopmentConfig(Config):
    DEBUG = True
    ENV = 'development'


class ProductionConfig(Config):
    DEBUG = False
    ENV = 'production'


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
