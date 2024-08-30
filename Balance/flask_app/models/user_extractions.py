from flask_app.config.mysqlconnection import connect_to_mysql
from flask_app import stuffing
import re
from flask import flash
# from flask_app.models import recipe_extractions

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class Users:
    def __init__(self,data):
        self.id=data["id"]
        self.user_name=data["user_name"]
        self.email=data["email"]
        self.password=data["password"]
        self.created_at=data["created_at"]
        self.updated_at=data["updated_at"]
        self.recipes = []

    @classmethod
    def create(cls,data):
        query="""INSERT INTO users (user_name,email,password)
        VALUES(%(user_name)s,%(email)s,%(password)s);"""
        return connect_to_mysql(stuffing).query_db(query,data)

    @classmethod
    def get_by_id(cls, data):
        query = """SELECT * from users WHERE users.id=%(id)s;"""
        results = connect_to_mysql(stuffing).query_db(query,data) 
        if results:
            return cls(results[0])
        return False
    
    
    @classmethod
    def get_by_email(cls, data):
        query = """SELECT * FROM users WHERE users.email=%(email)s;"""
        results = connect_to_mysql(stuffing).query_db(query,data)
        if results:
            return cls(results[0])
        return False                                                #not used in this project presently
    
    @classmethod
    def pull_recipes_for_user(cls, data):
        print(data)
        query= """SELECT * from users JOIN recipes ON users.id = recipes.user_id
                    WHERE users.id=%(id)s;"""
        results = connect_to_mysql(stuffing).query_db(query,data)
        if results:
            user_whole=cls(results[0])
            for single in results:
                if single['recipes.id'] == None:
                    return user_whole
                recipe_data={
                    **single,
                    'id': single['recipes.id'],
                    'created_at': single['recipes.created_at'],
                    'updated_at': single['recipes.updated_at']
                }
                recipes_whole = recipes_extractions.Recipes(recipe_data)
                user_whole.recipes.append(recipes_whole)
            return user_whole
        print(user_whole)
        return False

    
    @staticmethod
    def valid_register(data):
        is_valid =True
        if len(data['user_name'])<1:
            is_valid = False
            flash('User name is required','reg')
        elif len(data['user_name'])<2:
            is_valid = False
            flash('User name must be at least 2 characters long','reg')
        if len(data['email'])<1:
            is_valid = False
            flash('Email is required','reg')
        elif not EMAIL_REGEX.match(data['email']):
            is_valid = False
            flash('Email must be in valid email format', 'reg')
        else:
            potential_user = Users.get_by_email({'email':data['email']})
            if potential_user:
                is_valid = False
                flash('Email is taken. Please try again', 'reg')
        if len(data['password']) < 1:
            is_valid = False
            flash('Password is required','reg')
        elif len(data['password']) < 8:
            is_valid = False
            flash('Password must be more than 8 characters','reg')
        elif data['password'] != data['confirm']:
            is_valid = False
        flash('Password do not match', 'reg')
        return is_valid
