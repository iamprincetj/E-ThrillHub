import os
from dotenv import load_dotenv

load_dotenv()

class Config(object):
    MAIL_SERVER = os.getenv.get('MAIL_SERVER')
    MAIL_PORT = int(os.getenv.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.getenv.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.getenv.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv.get('MAIL_PASSWORD')
    ADMINS = ['tochukwunwanze5@gmail.com']