from flask import Flask,render_template,request,flash,redirect,make_response
from flask_sqlalchemy import SQLAlchemy
app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///airportdb.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] ='ghksrj'
db=SQLAlchemy(app)



class Users(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.Text)
    password = db.Column(db.Text)
    def __repr__(self):
        return f'user({self.username},{self.password})'

