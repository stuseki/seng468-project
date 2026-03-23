'''
Semantic Retrieval System API
'''
from flask import Flask, request, jsonify, Response
from flask_sqlalchemy import SQLAlchemy
import os
from datetime import datetime, timedelta
import secrets

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
    'DATABASE_URL',
    'postgresql://system:password@localhost:5432/system'
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

tomorrow = datetime.now() + timedelta(days=1)

# Database Models

class User(db.Model):
    __tablename__ = 'users'
    
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    
class Session(db.Model):
    __tablename__ = 'sessions'
    
    session_id = db.Column(db.String(40), primary_key=True)
    session_exp = db.Column(db.DateTime, default=tomorrow)
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))

# API Endpoints

@app.route('/auth/signup', methods=['POST'])
def create_user():
    
    data = request.get_json()
    
    user = User(
        username = data['username'],
        password = data['password']
    )
    
    try:
        db.session.add(user)
        db.session.commit()
    
        #retrieving generated user_id
        get_user = db.session.query(User).filter_by(username=user.username).first()
    
        return jsonify(
            message="User created successfully",
            user_id=get_user.user_id
        ), 200

    except:
        return jsonify(
            error="Username already exists"
        ), 409


@app.route('/auth/login', methods=['POST'])
def login_user():
    
    data = request.get_json()
    
    try:
        #check entered user and password against database, create session if match
        get_user = db.session.query(User).filter_by(username=data['username']).first()
        if (get_user.password == data['password']):
        
            session_token = secrets.token_urlsafe(16) #generate unique session token
        
            session = Session(
                session_id = session_token,
                user_id = get_user.user_id
            )
    
            db.session.add(session)
            db.session.commit()
        
            return jsonify(
                token=session_token,
                user_id=get_user.user_id
            ), 200
        else:
            return jsonify(
                error="Invalid credentials"
            ), 401
    except:
        return jsonify(
            error="Invalid credentials"
        ), 401
    
# Database initialization

with app.app_context():
    db.create_all()
    
if __name__ == '__main__':
    
    app.run(host='0.0.0.0', port=8080, debug=True)
    
    