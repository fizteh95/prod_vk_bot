import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    HOST = os.environ.get('HOST') or '127.0.0.1'
    PORT = os.environ.get('PORT') or 8080

    # LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT') or 1
    BOT_TOKEN = os.environ.get('BOT_TOKEN') or "1237502356:AAGCHzrR5UxSf5poe6SRuYRraReQ2YDp3Oc"
    BOT_USER_NAME = os.environ.get('BOT_USER_NAME') or "Svalkobot_bot"
    # URL = os.environ.get('URL') or "THE-HEROKU-APP-LINK"
    # ADMIN = os.environ.get('ADMIN') or "avshubin"  # "avshubin" "Konst_test"
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
