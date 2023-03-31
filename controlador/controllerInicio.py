from app import app,db
from flask import Flask,render_template
from flask_sqlalchemy import SQLAlchemy
from models.categoria import *
from models.producto import *

with app.app_context():
    db.create_all()

