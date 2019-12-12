from flask import Flask, redirect, url_for, flash, render_template, jsonify, request
from flask_login import login_required, logout_user, current_user, login_user
from .config import Config
from .models import db, login_manager, Token, User, Sitter, Booking
from .oauth import blueprint
from .cli import create_db
from flask_migrate import Migrate
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
import dateutil.parser
import datetime

app = Flask(__name__)
CORS(app)
app.config.from_object(Config)
app.register_blueprint(blueprint, url_prefix="/login")
app.cli.add_command(create_db)
db.init_app(app)

migrate = Migrate(app, db)
login_manager.init_app(app)

@app.route("/")
def index():
    return render_template("home.html")

@app.route("/logout")
@login_required
def logout():
    token = Token.query.filter_by(user_id=current_user.id).first()
    if token:
        db.session.delete(token)
        db.session.commit()
    logout_user()
    flash("You have logged out")
    return jsonify(success=True)

@app.route('/getuser', methods=['GET'])
@login_required
def getuser():
    return jsonify(user_id=current_user.id, name=current_user.name)

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    check_user = User.query.filter_by(email=data['email']).first() ## you can get NOTHING or 1 user (None or item1)
    ## if you .all() you will get a [] or [item1] or [item1,item2,item3]
    if check_user: #if email is already taken
        #do something
        return jsonify(success=False, message="email taken")
    else :
        new_user = User(name=data['name'],
                    email=data['email'])
        new_user.generate_password(data['password']) 
        db.session.add(new_user)
        db.session.commit()
        return jsonify(success=True)

@app.route('/signin', methods=['POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()
        user = User.query.filter_by(email=data['email']).first()
        if not user:
            return jsonify(success=False, message="eamil doesnt exist")
        if not user.check_password(data['password']):
            return jsonify(success=False, message="Wrong password")
        login_user(user)
        token = Token.query.filter_by(user_id = user.id).first()
        if not token:
            token = Token(user_id=user.id, uuid=str(uuid.uuid4().hex))
            db.session.add(token)
            db.session.commit()
        resp = jsonify(success=True, 
                    message="successfully logged in",
                    token=token.uuid,
                    user=user.render())
        print(resp)
        return resp        

@app.route('/sitter-list', methods=['GET', 'POST'])
def sitter():
    sitters = Sitter.query.all()
    res = {
        "success": True,
        "sitters": [ sitter.render() for sitter in sitters]
    }
    return jsonify(res)

@app.route('/sitter-register', methods=[ 'POST'])
@login_required
def sitter_register():
    if request.method == "POST":
        data = request.get_json()
        sitter = Sitter.query.filter_by(user_id = current_user.id).first()
        if sitter:
            return jsonify(success=False)
        if not sitter:
            new_sitter = Sitter(picture=data['picture'],
                                quote=data['quote'],
                                city=data['city'],
                                price=data['price'],
                                user_id=current_user.id,
                                )
            db.session.add(new_sitter)
            current_user.is_sitter = True
            db.session.commit()
            sitters = Sitter.query.all()
            res = {
                "success": True,
                "sitters": [ sitter.render() for sitter in sitters]
            }
        return jsonify(res)

@app.route('/sitter-detail/<id>', methods=['GET', 'POST'])
def sitter_detail(id):
    sitter = Sitter.query.get(id)
    res = {
        "sitter": sitter.render()
    }
    return jsonify(res)

# create booking
@app.route('/sitter-detail/<id>/contact', methods=['POST'])
@login_required
def contact_sitter(id):
    if request.method == "POST":
        data = request.get_json()
        sitter = Sitter.query.get(id)

        s = data['startDate']
        # s = "2019-1-01T06:59:00.000Z"
        startDate = dateutil.parser.parse(s)

        e = data['finishDate']
        # e = "2019-12-29T06:59:00.000Z"
        endDate = dateutil.parser.parse(e)

        # delta = end - start
        # diff = delta.days
       
        new_booking = Booking(
            user_id= current_user.id,
            sitter_id= id,
            start=startDate,
            finish=endDate,
            price=data['price'],
            message=data['message'],
            created_at= datetime.datetime.now(),
            is_confirmed = False,
            pet_type= data['pet_type'],
            pet_size= data['pet_size'],
            pet_name= data['pet_name'],
            pet_breed= data['pet_breed'],
            pet_age= data['pet_age'],
            pet_sex= data['pet_sex'],
            is_photo= data['is_photo']
        )
        db.session.add(new_booking)
        db.session.commit()
        bookings = Booking.query.all()
        res = {
        "success": True,
        "bookings": [ booking.render() for booking in bookings]
        }
        print(res)
        return jsonify(res)
