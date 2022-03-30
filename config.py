import os

CURRENT_USER = 'Jack'
PATH_UPLOAD_IMAGE = os.path.join(os.getcwd(), f'static/user_pics/{CURRENT_USER}')


class Configuration(object):
    DEBUG = True
    SERVER_NAME = 'flask.localhost:6001'
    SECRET_KEY = os.urandom(24)
    UPLOADED_PHOTOS_DEST = PATH_UPLOAD_IMAGE
