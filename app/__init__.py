from flask import Flask, redirect, url_for, flash, render_template, jsonify, request
from flask_login import login_required, logout_user, current_user, login_user
from .config import Config
from .models import db, login_manager, Token, User
from .oauth import blueprint
from .cli import create_db
from flask_migrate import Migrate
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import uuid

app = Flask(__name__)
CORS(app)
app.config.from_object(Config)
app.register_blueprint(blueprint, url_prefix="/login")
app.cli.add_command(create_db)
db.init_app(app)

migrate = Migrate(app, db)
login_manager.init_app(app)

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

@app.route("/")
def index():
    return render_template("home.html")

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
        
