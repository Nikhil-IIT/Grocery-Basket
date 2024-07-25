from flask import Flask, Response, jsonify, render_template, request, session, redirect, url_for, flash, get_flashed_messages
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from flask_mail import Mail
import json
import os
import io
import re
import math
from datetime import datetime
from flask_login import LoginManager, UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, EqualTo, Email, Length, ValidationError, DataRequired
from flask_bcrypt import Bcrypt
import random
import pymysql
import numpy as np
import matplotlib.pyplot as plt
from flask_cors import CORS, cross_origin
from sqlalchemy.exc import SQLAlchemyError
import csv
from sqlalchemy import DateTime, and_
from config import LocalDevementConfig
from flask_restful import Api
import workers
import redis
from flask_caching import Cache
from flask import Flask, current_app

cache = Cache()

app = Flask(__name__)
CORS(app, support_credentials=True)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = 'whatcanisaywordsnotenoughtodescribeyou'
app.config['CORS_HEADERS'] = 'Content-Type'
CORS(app, resources={r"/*": {'origins': "http://localhost:8080", "allow_headers": "Access-Control-Allow-Origin"}})
login_manager = LoginManager(app)
login_manager.init_app(app)
login_manager.login_view = 'login'
app.secret_key = '8f42a73054b1749f8f58848be5e6502c'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://username:password@localhost/database_name'  # Update URI for MySQL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
celery = None

def create_ap():
    if os.getenv('ENV', 'development') == 'production':
        raise Exception('Production environment not configured yet')
    else:
        print('Starting in development mode')
        app.config.from_object(LocalDevementConfig)
    app.app_context().push()
    
    celery = workers.celery

    celery.conf.update(
        broker_url=app.config["CELERY_BROKER_URL"],
        result_backend=app.config["CELERY_RESULT_BACKEND"],
    )

    celery.Task = workers.ContextTask
    app.app_context().push()

    redis_connection = redis.StrictRedis(
        host=app.config['REDIS_HOST'],
        port=app.config['REDIS_PORT'],
        db=app.config['REDIS_DB']
    )
    app.redis = redis_connection
    app.app_context().push()

    cache.init_app(app)
    app.app_context().push()

    return app, celery, cache

app, celery, cache = create_ap()

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

@login_manager.user_loader
def load_user(sm_id):
    return Store_managers.query.get(int(sm_id))

class Users(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    last_visited = db.Column(db.DateTime, default=datetime.utcnow)

class Store_managers(db.Model, UserMixin):
    __tablename__ = 'store_managers'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    sm_username = db.Column(db.String(80), unique=True, nullable=False)
    sm_email = db.Column(db.String(80), unique=True, nullable=False)
    sm_password = db.Column(db.String(120), nullable=False)
    approved = db.Column(db.Integer, nullable=False)

class Products(db.Model):
    __tablename__ = 'grocery'
    product_id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(80), nullable=False)
    quantity = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    category = db.Column(db.String(80), nullable=False)
    image = db.Column(db.String(500), nullable=False)
    sm_id = db.Column(db.Integer, nullable=False)
    stock = db.Column(db.Integer, nullable=False)

class Orders(db.Model):
    __tablename__ = 'orders'
    order_id = db.Column(db.Integer, primary_key=True, unique=True)
    username = db.Column(db.Integer, nullable=False)
    product_name = db.Column(db.String(80), nullable=False)
    no_of_items = db.Column(db.Integer, nullable=False)
    product_id = db.Column(db.Integer, nullable=False)

class Category(db.Model):
    __tablename__ = 'category'
    c_id = db.Column(db.Integer, primary_key=True, unique=True)
    c_name = db.Column(db.String(80), nullable=False)

class Requests(db.Model):
    __tablename__ = 'requests'
    r_id = db.Column(db.Integer, primary_key=True, unique=True)
    r_name = db.Column(db.String(80), nullable=False)

with app.app_context():
    db.create_all()
@app.route('/signup', methods=['POST'])
def signup():
    try:
        data = request.json
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        existing_user = Users.query.filter_by(username=username).first()

        if existing_user:
            return jsonify({'message': 'User already exists'})

        new_user = Users(username=username, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'Signup successful'})
    except Exception as e:
        print(str(e))
        return jsonify({'message': 'Signup failed'})

@app.route('/s_manager/signup', methods=['POST'])
def s_manager_signup():
    try:
        data = request.json
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        approved=data.get('approved')
        
        existing_user = Store_managers.query.filter_by(sm_username=username).first()
        print("here")
        if existing_user:
            return jsonify({'message': 'User already exists'})
        
        new_user = Store_managers(sm_username=username,sm_email=email, sm_password=password,approved=approved)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'Signup successful'})
    except Exception as e:
    
        print(str(e))
        return jsonify({'message': 'Signup failed'})

@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.json
        username = data.get('username')
        password = data.get('password')
        print(username,password)
        simple_user = Users.query.filter_by(username=username).first()
        store_user = Store_managers.query.filter_by(sm_username=username).first()
        
        print(type(simple_user))
        if simple_user is not None:
            print("I simple user")
            if simple_user.username==username and simple_user.password == password:
                print("I go from here")
                login_user(simple_user)
                simple_user.last_visited = datetime.now()
                db.session.commit()
                user_data = {
                'username': username,
                'user_id': simple_user.id,        
                }
                return jsonify({'message': 'Login successful','user': user_data})
            else:
                return jsonify({'message': 'Invalid credentials'})
        
        elif store_user is not None:
            print("I store user")
            if store_user.sm_username==username and store_user.sm_password == password:
                print("I go from here")
                login_user(store_user)
                store_user.last_visited = datetime.now()
                user_data = {
                'username': username,
                'user_id': store_user.id,        
                }
                print("safe")
                return jsonify({'check':"sm",'message': 'Login successful','user': user_data})
            else:
                return jsonify({'message': 'Invalid credentials'})

        else:
            return jsonify({'message': 'User already exists'})
    except SQLAlchemyError as e:
        print(str(e))
        return jsonify({'message': 'Database error'})
    except Exception as e:
        print(str(e))
        return jsonify({'message': 'Login failed'})

@app.route('/admin_login', methods=['POST'])
def admin_login():
    try:
        data = request.json
        username = data.get('username')
        password = data.get('password')
        print(username,password)
        user = Users.query.filter_by(username=username).first()
        print("I go from here")
        if user.username=="admin" and user.password == "admin123":
            print("I go from here")
            login_user(user)
            user_data = {
                'username': username,
                'user_id': user.id,        
            }
            return jsonify({'message': 'Login successful','user': user_data})
        else:
            return jsonify({'message': 'Invalid credentials'})

    except SQLAlchemyError as e:
        print(str(e))
        return jsonify({'message': 'Database error'})
    except Exception as e:
        print(str(e))
        return jsonify({'message': 'Login failed'})

@app.route('/logout', methods=['POST'])
def logout():
    logout_user()
    print("user logout")
    return jsonify({'message': 'Logout successful'})

@app.route('/protected')
@login_required
def protected():
    return jsonify({'message': 'This is a protected route'})

# @app.route('/generate_csv/<int:sm_id>', methods=['GET','POST'])
# def generate_csv(sm_id):
#     print(sm_id)
#     with sqlite3.connect("database.db") as con:
#         cur = con.cursor()
#         cur.execute("SELECT product_id,name,quantity,price,category,image FROM grocery where sm_id=?", (sm_id,))
#         data = cur.fetchall()

#     con.close()

#     output = io.StringIO()
#     csv_writer = csv.writer(output)

#     csv_writer.writerow(['product_id', 'name','quantity','price','category','image'])

#     for row in data:
#         csv_writer.writerow(row)

#     output.seek(0)

#     return Response(output, mimetype='text/csv',
#                     headers={'Content-Disposition': 'attachment; filename=data.csv'})

@app.route("/",methods=['GET','POST'])
def go():
    return("Hello,Server")

@app.route('/products/<sm_id>', methods=['GET'])
def products(sm_id):
    products = Products.query.filter_by(sm_id=sm_id).all()
    
    product_list = []
    for product in products:
        product_dict = {
            "product_id": product.product_id,
            "name": product.name,
            "quantity": product.quantity,
            "price": product.price,
            "category":product.category,
            "stock":product.stock,
            "image":product.image,
        }
        product_list.append(product_dict)

    return jsonify({
        "items": product_list,
        "status": 'success'
    })

@app.route('/my_category', methods=['GET'])
def my_category():
    categories = Category.query.all()
    
    category_list = []
    for c in categories:
        category_dict = {
            "c_id": c.c_id,
            "c_name": c.c_name,
        }
        category_list.append(category_dict)

    return jsonify({
        "categories": category_list,
        "status": 'success'
    })

@app.route('/edit/<product_id>', methods=['GET','POST'])
def edit(product_id):
    print(type(product_id))
    if request.method=="GET":
        product = Products.query.filter_by(product_id=product_id).first()
        
        product_list = []
        product_dict = {
                "product_id": product.product_id,
                "name": product.name,
                "quantity": product.quantity,
                "price": product.price,
                "category":product.category,
                "stock":product.stock,
                "image":product.image,
            }
        product_list.append(product_dict)
        print("sucess")
        return jsonify({"items": product_list,"status": 'success'})
    
    print("hello")
    if request.method=="POST":
        data = request.json
        name = data.get('name')
        quantity = data.get('quantity')
        price = data.get('price')
        category = data.get('category')
        stock = data.get('stock')
        image = data.get('image')
        sm_id = data.get('sm_id')
        print(name,quantity,category)
        if product_id=='0':
            print("I am here")
            product = Products(name=name,quantity=quantity,price=price,category=category,stock=stock,image=image,sm_id=sm_id)
            db.session.add(product)
            db.session.commit()
            return jsonify({'message': 'Added successful'})
        else:
            post = Products.query.filter_by(product_id=product_id).first()
            post.name=name
            post.quantity=quantity
            post.price=price
            post.category=category
            post.stock=stock
            post.image=image
            db.session.commit()
            return jsonify({'message': 'Edited successful'})

@app.route('/edit_category/<category_id>', methods=['GET','POST'])
def edit_category(category_id):
    print(type(category_id))
    
    if request.method=="GET":
        category = Category.query.filter_by(c_id=category_id).first()
        category_list = []
        category_dict = {
                "c_id": category.c_id,
                "c_name": category.c_name,
            }
        category_list.append(category_dict)
        print("sucess")
        return jsonify({"items": category_list,"status": 'success'})
    
    print("hello")
    if request.method=="POST":
        data = request.json
        name = data.get('c_name')
        print(name)
        if category_id=='0':
            print("I am here")
            post = Category(c_name=name)
            db.session.add(post)
            db.session.commit()
            return jsonify({'message': 'Added successful'})
        else:
            post = Category.query.filter_by(c_id=category_id).first()
            post.c_name=name
            db.session.commit()
            return jsonify({'message': 'Edited successful'})

@app.route('/api/products', methods=['GET'])
def get_products():
    print("I here")
    products = Products.query.all()
    products_list = [{
        'product_id': product.product_id,
        'name': product.name,
        'quantity': product.quantity,
        'price': product.price,
        'category': product.category,
        'stock': product.stock,
        'image': product.image
    } for product in products]
    return jsonify(products_list)

@app.route('/get_sm_data', methods=['GET'])
def get_sm_data():
    print("I there")
    sms = Store_managers.query.filter_by(approved=0).all()
    print(sms)
    sms_list = [{
        'sm_id':sm.id,
        'sm_username': sm.sm_username,
        'sm_email': sm.sm_email,
    } for sm in sms]
    return jsonify({"sms_list":sms_list})

@app.route('/check_approve/<int:sm_id>', methods=['POST'])
def check_approve(sm_id):
    print("i am here")
    try:
        approve=False
        print(sm_id)
        store_manager = Store_managers.query.get(sm_id)
        print(store_manager)
        if store_manager is None:
            return jsonify({'message': 'Store Manager not found'})

        if store_manager.approved== 1:
            approve=True
            return jsonify({'approve': approve})

        else:
            return jsonify({'message':"admin declined your request"})
        
    except Exception as e:
        return jsonify({'message': 'Error occurred', 'error': str(e)})
    
@app.route('/approve_or_not/<int:sm_id>/<int:value>', methods=['POST'])
def appove_or_not(sm_id, value):
    print("i am here")
    try:
        print(sm_id)
        store_manager = Store_managers.query.get(sm_id)
        print(store_manager)
        if store_manager is None:
            return jsonify({'message': 'Store Manager not found'})

        if value == 1:
            store_manager.approved = 1
        elif value == 0:
            db.session.delete(store_manager)

        db.session.commit()
        return jsonify({'message': 'Operation successful'})

    except Exception as e:
        return jsonify({'message': 'Error occurred', 'error': str(e)})

@app.route('/api/categories', methods=['GET'])
def get_categories():
    print("I there")
    categories = Category.query.all()
    categories_list = [{
        'c_id': category.c_id,
        'c_name': category.c_name
    } for category in categories]
    return jsonify(categories_list)

@app.route('/my_request', methods=['GET','POST'])
def request_fun():
    if request.method=='POST':
        data = request.json
        name = data.get('r_name')
        print(name)
        post = Requests(r_name=name)
        db.session.add(post)
        db.session.commit()
        return jsonify({'message': 'Added successful'})
    else:
        reqs=Requests.query.all()
        req_list = [{
        'r_id': req.r_id,
        'r_name': req.r_name
    } for req in reqs]
    return jsonify({'requests':req_list,'message': 'sent successful'})

@app.route('/addToCart', methods=['POST'])
def addToCart():
    data = request.json
    username = data.get('username')
    product_id = data.get('product_id')
    product_name = data.get('product_name')
    no_of_items=data.get('quantity')
    
    if username and product_id and product_name:
        product = Products.query.filter_by(product_id=product_id).first()
        order = Orders(
            username=username,
            product_name=product_name,
            no_of_items=no_of_items,
            product_id=product_id,
        )
        product.stock -= no_of_items
        db.session.add(order)
        db.session.commit()
        return jsonify({'message': 'Product added to cart successfully'})
    else:
        return jsonify({'message': 'Invalid data sent'})

@app.route('/cart/<u_id>', methods=['GET'])
def cart(u_id):
    print("I'm here")
    orders = Orders.query.filter_by(username=u_id).all()
    p_ids = [order.product_id for order in orders]

    product_prices = {}
    
    for product_id in p_ids:
        product = Products.query.filter_by(product_id=product_id).first()
        if product:
            product_prices[product_id] = product.price
    
    print(p_ids)
    
    orders_list = []
    for order in orders:
        order_id=order.order_id
        product_id = order.product_id
        product_name = order.product_name
        quantity = order.no_of_items
        
        price = product_prices.get(product_id, 0)
        orders_list.append({
            'order_id':order_id,
            'product_name': product_name,
            'no_of_items': quantity,
            'price': price
        })

    return jsonify({'items': orders_list})

@app.route('/search/<prodt>', methods=['GET'])
@cache.cached(timeout=6000)
def search_product(prodt):
    query=prodt
    print("internal here")
    if query:
        results = Products.query.filter(Products.name.ilike(f'%{query}%')).all()

        products_list = [{
            'product_id': result.product_id,
            'name': result.name,
            'quantity': result.quantity,
            'price': result.price,
            'category': result.category,
            'stock': result.stock,
            'image': result.image
        } for result in results]
        print(products_list)
        return jsonify(products_list)
    else:
        return jsonify([])

@app.route('/search_category/<cat>/<prodt>', methods=['GET'])
@cache.cached(timeout=6000)
def search_by_category(cat, prodt):
    query = prodt
    if query:
        results = Products.query.filter(and_(Products.name.ilike(f'%{query}%'), Products.category == cat)).all()

        products_list = [{
            'product_id': result.product_id,
            'name': result.name,
            'quantity': result.quantity,
            'price': result.price,
            'category': result.category,
            'stock': result.stock,
            'image': result.image
        } for result in results]
        print(products_list)
        return jsonify(products_list)
    else:
        return jsonify([])


@app.route('/delete_request/<r_id>', methods=['GET','POST','DELETE'])
def delete_request(r_id):
    post = Requests.query.filter_by(r_id=r_id).first()
    db.session.delete(post)
    db.session.commit()
    return jsonify({'message': 'Deleted successful'})

@app.route('/delete_order/<o_id>', methods=['GET','POST','DELETE'])
def delete_order(o_id):
    post = Orders.query.filter_by(order_id=o_id).first()
    product = Products.query.filter_by(product_id=post.product_id).first()
    product.stock += post.no_of_items
    db.session.delete(post)
    db.session.commit()
    return jsonify({'message': 'Deleted successful'})      


@app.route('/delete_product/<p_id>', methods=['GET','POST','DELETE'])
def delete_product(p_id):
    post = Products.query.filter_by(product_id=p_id).first()
    db.session.delete(post)
    db.session.commit()
    return jsonify({'message': 'Deleted successful'})      


@app.route('/delete_category/<c_id>', methods=['GET','POST','DELETE'])
def delete_category(c_id):
    post = Category.query.filter_by(c_id=c_id).first()
    db.session.delete(post)
    db.session.commit()
    return jsonify({'message': 'Deleted successful'})      

# if __name__ == "__main__":
#     app.run(debug=True)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
