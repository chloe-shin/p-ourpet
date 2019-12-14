from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin
from flask_dance.consumer.storage.sqla import OAuthConsumerMixin
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
db = SQLAlchemy()


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String,  unique=False)
    is_sitter = db.Column(db.Boolean, default = False)
    phone_number = db.Column(db.String)
    sitter = db.relationship('Sitter', backref='user', uselist=False)
    booking = db.relationship('Booking', backref='user')

    # password: 지금 입력한 비밀번호 #self.password: 사용자 비밀번호
    def generate_password(self, password):
        self.password = generate_password_hash(password)  # password를 암호화
    def check_password(self, password):
        return check_password_hash(self.password, password) 

    def render(self):
        return {
            "name": self.name,
            "email": self.email
        }

class OAuth(OAuthConsumerMixin, db.Model):
    provider_user_id = db.Column(db.String(256), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship(User)
 
class Token(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False) #token
    user = db.relationship(User) 

class Sitter(db.Model):
    __tablename__ = 'sitters'
    id = db.Column(db.Integer, primary_key=True)
    picture = db.Column(db.String)
    quote = db.Column(db.String)
    city = db.Column(db.String)
    price = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    bookings = db.relationship('Booking', backref='sitter')

    def render(self):
        return {
            "name": self.user.name,
            "email": self.user.email,
            "image": self.picture,
            "quote": self.quote,
            "price": self.price,
            "city": self.city,
            "sitter_id": self.id,
            "user_id": self.user.id
        }

class Booking(db.Model):
    __tablename__='bookings'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    sitter_id = db.Column(db.Integer, db.ForeignKey('sitters.id'), nullable=False)
    start = db.Column(db.DateTime, nullable=False)
    finish = db.Column(db.DateTime, nullable=False)
    price = db.Column(db.Integer)
    created_at = db.Column(db.DateTime)
    message = db.Column(db.String)
    is_confirmed= db.Column(db.Boolean, default= False)
    total_price = db.Column(db.Integer)
    pet_type= db.Column(db.String)
    pet_size= db.Column(db.String)
    pet_name= db.Column(db.String)
    pet_breed= db.Column(db.String)
    pet_age= db.Column(db.String)
    pet_sex= db.Column(db.String)
    is_photo= db.Column(db.Boolean, default= False)

    def render(self):
        return {
            "id": self.id,
            "user_id": self.user.id,
            "sitter_id" : self.sitter.id,
            "sitter_pic": self.sitter.picture,
            "sitter_name":self.sitter.user.name,
            "start" : self.start,
            "finish" : self.finish,
            "price" : self.price,
            "message": self.message,
            "created_at": self.created_at,
            "is_confirmed": self.is_confirmed,
            "total_price": self.total_price,
            "pet_type": self.pet_type,
            "pet_size": self.pet_size,
            "pet_name": self.pet_name,
            "pet_breed": self.pet_breed,
            "pet_age": self.pet_age,
            "pet_sex": self.pet_sex,
            "is_photo": self.is_photo
        }
    # def total(self):
        # Step 1: Find how many days
        
        # Step 2: Multiply days * price

        # Step 3: Return that answer 
         
# setup login manager
login_manager = LoginManager()
# login_manager.login_view = "facebook.login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@login_manager.request_loader
def load_user_from_request(request):
    api_key = request.headers.get('Authorization')
    if api_key:
        api_key = api_key.replace('Token ', '', 1)
        token = Token.query.filter_by(uuid=api_key).first()
        if token:
            return token.user
    return None