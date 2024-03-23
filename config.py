# mysql
HOSTNAME = 'localhost'
PORT = '3306'
DATABASE = 'web_manager'
USERNAME = 'root'
PASSWORD = '090910'
DB_URI = 'mysql+pymysql://{}:{}@{}:{}/{}'.format(USERNAME, PASSWORD, HOSTNAME, PORT, DATABASE)
SQLALCHEMY_DATABASE_URI = DB_URI
SQLALCHEMY_TRACK_MODIFICATIONS = True
SECRET_KEY = 'woshinibabaliuyongqi'
