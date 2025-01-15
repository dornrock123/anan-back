from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_cors import CORS
from datetime import timedelta
import json

app = Flask(__name__)
CORS(app)

# โหลดค่า DATABASE_URL จาก Environment Variable
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://falldetection_db_owner:CkW8IYy2ibZw@ep-quiet-thunder-a1p7xxpv.ap-southeast-1.aws.neon.tech/falldetection_db?sslmode=require"

db = SQLAlchemy(app)

@app.route('/')
def home():
    return "Hello, Flask!"

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False)

@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    print('data is', data)
    email = data.get('email')
    username = data.get('username')
    password = data.get('password')
    role = data.get('role', 'user')  # Default role is 'user'

    # ตรวจสอบว่า email หรือ username มีอยู่แล้วในฐานข้อมูล
    existing_user = User.query.filter((User.email == email) | (User.username == username)).first()

    if existing_user:
        return jsonify({"message": "Email หรือ Username นี้มีผู้ใช้งานแล้ว"}), 400

    new_user = User( username=username, email=email, password=password, role=role)

    try:
        db.session.add(new_user)
        db.session.commit()
        print("New user added to database successfully.")
        return jsonify({"message": "User registered successfully"}), 201
    except Exception as e:
        db.session.rollback()
        print(f"Error occurred: {str(e)}")
        return jsonify({"message": f"Error occurred: {str(e)}"}), 500


if __name__ == '__main__':
    app.run(debug=True)
