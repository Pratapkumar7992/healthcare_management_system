# app/models.py
from app import mongo

class User:
    @staticmethod
    def add_user(email, password):
        user = {
            "email": email,
            "password": password  # Make sure this is hashed before saving
        }
        mongo.db.users.insert_one(user)

    @staticmethod
    def get_user_by_email(email):
        return mongo.db.users.find_one({"email": email})
