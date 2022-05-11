from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from typing import Callable
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import os
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///datebase.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False



class MySQLAlchemy(SQLAlchemy):
    Column: Callable
    String: Callable
    Integer: Callable
    Float: Callable
    Text: Callable
    relationship: Callable
    ForeignKey: Callable
    DateTime: Callable

db = MySQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)


from main import routes