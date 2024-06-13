#!/usr/bin/env python3

import os

# Remote library imports
from flask import request, session, jsonify, render_template
from flask_restful import Resource
from werkzeug.exceptions import NotFound
from functools import wraps
from sqlalchemy.sql import func

# Cloudinary
import cloudinary
import cloudinary.uploader
import cloudinary.api
from dotenv import load_dotenv

# Local imports
from config import app, db, api
# Add your model imports
from models.user import User
from models.favorite import Favorite

# Cloudinary
load_dotenv()
config = cloudinary.config(secure=True)

# Error Handling
@app.errorhandler(NotFound)
def not_found(error):
    return {"error": error.description}, 404

# Route Protection
def login_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return {"Error": "Access Denied. Please log in."}, 422
        return func(*args, **kwargs)
    return decorated_function

# API Routes

# Frontend Routes
@app.route('/')
@app.route('/browse')
@app.route('/user/edit')
def index(id=0):
    return render_template("index.html")


class UserById(Resource):
    @login_required
    def get(self, id):
        try: 
            if user := db.session.get(User, id):
                return user.to_dict(), 200
            else:
                return {"Error": "User not found."}, 404
        except Exception as e:
            return {"Error": str(e)}, 400
    
    @login_required
    def patch(self, id):
        if user := db.session.get(User, id):
            try:
                file = request.files['profile_image']
                if file:
                    response = cloudinary.uploader.upload(
                        file,
                        upload_preset="HomeApp",
                        unique_filename=True, 
                        overwrite=True,
                        eager=[{"width": 500, "crop": "fill"}]
                    )
                    image_url = response['eager'][0]['secure_url']
                    user.profile_image = image_url

                data = request.form
                for attr, value in data.items():
                    if attr == '_password_hash':
                        user.password_hash = value
                    else:
                        setattr(user, attr, value)
                db.session.commit()
                return user.to_dict(), 202

            except Exception as e:
                return {"Error": [str(e)]}, 400
        else:
            return {"Error": "User not found"}, 404

    @login_required    
    def delete(self, id):
        try: 
            if user := db.session.get(User, id):
                db.session.delete(user)
                db.session.commit()
                return "", 204
            else:
                return {"Error": "User not found."}, 404
        except Exception as e:
            db.session.rollback()
            return {"Error": str(e)}, 400
api.add_resource(UserById, "/users/<int:id>")

class Favorites(Resource):
    @login_required
    def get(self, user_id):
        try:
            if user := db.session.get(User, user_id):
                favorites = [favorite.to_dict() for favorite in user.favorites]
                return favorites, 200   
            else:
                return {"Error": "User not found."}, 404
        except Exception as e:
            return {"Error": str(e)}, 400
api.add_resource(Favorites, "/users/<int:user_id>/favorites")

class AddFavorite(Resource):
    @login_required
    def post(self, user_id):
        try:
            user = User.query.get(user_id)
            
            if not user:
                return {"Error": "User not found."}, 404

            data = request.json
            new_favorite = Favorite(user_id=user.id, **data)
            db.session.add(new_favorite)
            db.session.commit()
            
            return new_favorite.to_dict(), 201

        except Exception as e:
            db.session.rollback()
            return {"Error": str(e)}, 400
api.add_resource(AddFavorite, '/<int:user_id>/add_favorite')

class RemoveFavorite(Resource):
    @login_required
    def delete(self, user_id, favorite_id):
        try:
            user = User.query.get(user_id)
            if not user:
                return {"Error": "User not found."}, 404

            favorite = Favorite.query.filter_by(id=favorite_id, user_id=user_id).first()
            if not favorite:
                return {"Error": "Favorite not found."}, 404

            db.session.delete(favorite)
            db.session.commit()

            return {"Success": "Favorite removed"}, 200
        except Exception as e:
            db.session.rollback()
            return {"Error": str(e)}, 400
api.add_resource(RemoveFavorite, '/<int:user_id>/remove_favorite/<int:favorite_id>')

# User Management

# Signup
class SignUp(Resource):
    def post(self):
        file = request.files['profile_image']
        if file:
            try:
                response = cloudinary.uploader.upload(
                    file,
                    upload_preset="HomeApp",
                    unique_filename=True, 
                    overwrite=True,
                    eager=[{"width": 500, "crop": "fill"}]
                )
                image_url = response['eager'][0]['secure_url']
            except Exception as e:
                return {"Error": str(e)}, 400 

        data = request.form
        
        try:
            new_user = User(
                username=data['username'],
                email=data['email'],
                profile_image=image_url if file and image_url else None
            )
            new_user.password_hash = data['_password_hash']
            
            db.session.add(new_user)
            db.session.commit()

            session['user_id'] = new_user.id
            return new_user.to_dict(), 201
        except Exception as e:
            db.session.rollback()
            return {"Error": str(e)}, 400
api.add_resource(SignUp, '/signup')

class Login(Resource):
    def post(self):
        try:  
            data = request.form
            user = User.query.filter_by(email=data.get("email")).first()
            if user and user.authenticate(data.get('_password_hash')):
                session["user_id"] = user.id
                return user.to_dict(), 200
            else:
                return {"Error": "Invalid Login"}, 422
        except Exception as e:
            db.session.rollback()
            return {"Error": str(e)}, 400
api.add_resource(Login, '/login')

class Logout(Resource):
    def delete(self):
        try:
            if "user_id" in session:
                del session['user_id']
                return {}, 204
            else:
                return {"Error": "A User is not logged in."}, 404
        except Exception as e:
            db.session.rollback()
            return {"Error": str(e)}, 400
api.add_resource(Logout, '/logout')

class CheckMe(Resource):
    def get(self):
        if "user_id" in session:
            user = db.session.get(User, session.get("user_id"))
            return user.to_dict(), 200
        else:
            return {"Error": "Please log in."}, 400       
api.add_resource(CheckMe, '/me')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
