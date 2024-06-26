# database_models.py
# Contains the user model for user authentication

from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), unique=True, nullable=False)
    api_key = db.Column(db.String(36), unique=True, nullable=False) # UUID TOKEN AUTHENTICATION