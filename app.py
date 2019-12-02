from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login.login_manager import LoginManager
from flask_mail import Mail
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
lm = LoginManager(app)
lm.session_protection = 'strong'
lm.login_view = '/login'
mail = Mail(app)
mail.init_app(app)
from routes import *



if __name__ == '__main__':
    remove_captcha()
    app.run(host='0.0.0.0', port=8080)
