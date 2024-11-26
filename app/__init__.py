# app/__init__.py
from flask import Flask
from flask_pymongo import PyMongo

# Initialize the PyMongo instance
mongo = PyMongo()

def create_app():
    app = Flask(__name__)

    # MongoDB configuration
    app.config["MONGO_URI"] = "mongodb+srv://healthsphere:Office9087@cluster0.lvgai.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

    # Initialize PyMongo with the app
    mongo.init_app(app)

    # Import routes after initializing the app
    from app import routes, models

    return app
