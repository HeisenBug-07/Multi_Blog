import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'multi_blog123321123321multi_blog'

dir_name = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(dir_name, 'database.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app, db)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'user.login'

from myproject.posts.view import post_blueprint
from myproject.users.view import user_blueprint
from myproject.core.view import core_blueprint

app.register_blueprint(post_blueprint)
app.register_blueprint(user_blueprint)
app.register_blueprint(core_blueprint)
