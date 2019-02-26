from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap

app = Flask(__name__)

app.config['SECRET_KEY'] = 'Secret*23@'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://issue_tracker:today*123@127.0.0.1/issue_tracker'

db = SQLAlchemy(app)
Bootstrap(app)
login_manager = LoginManager(app)
migrate = Migrate(app, db)
login_manager.login_message = "You must be logged in to access this page."
login_manager.login_view = "auth.login"



from app import models

from .admin import admin as admin_blueprint
app.register_blueprint(admin_blueprint, url_prefix='/admin')

from .auth import auth as auth_blueprint
app.register_blueprint(auth_blueprint)

from .home import home as home_blueprint
app.register_blueprint(home_blueprint)