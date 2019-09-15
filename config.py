import datetime
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

SECRET_KEY = os.getenv("SECRET_KEY", "shuuuutsecretkey")
JWT_SECRET_KEY = os.getenv("SECRET_KEY", "sangat rahasia banget")
JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(hours=3)

SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(os.path.join(BASE_DIR, "app.db"))
SQLALCHEMY_TRACK_MODIFICATIONS = True
