from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost:3306/practise'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Example(db.Model):
    __tablename__ = 'users'

    id = db.Column('id', db.Integer, primary_key = True)
    name = db.Column('name', db.Unicode)
    email = db.Column('email', db.Unicode)

    def __init__(self, name, email):
        self.name = name
        self.email = email