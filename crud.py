import imp
from flask import Flask, request, jsonify
import sql_requests
from psycopg2 import errors
import psycopg2
import hashlib
import jwt
import os
import socket

SECRET_KEY = "SUPER_SECRET_KEY?" 
DB_PASS = "123" # Пароль от пользователя БД
DB_HOST = "192.168.1.20" # IP сервера, где находится БД
USER = "cars_user" # Имя пользователя в БД
PORT = "5432" # Порт БД

connect = psycopg2.connect(
    f"dbname=cars user={USER} password={DB_PASS} host={DB_HOST} port={PORT}")
cursor = connect.cursor()

app = Flask(__name__)

@app.route('/')
def main():
    ip = socket.gethostbyname(socket.gethostname())
    return f"{ip}"

# AUTHORIZATION
@app.route('/auth/login/', methods=["POST"])
def auth():
    # {"user", "password"}
    #
    body = request.get_json()
    user = body["user"]
    password = body["password"]
    encode_password = hashlib.md5(f"{password}{SECRET_KEY}".encode()).hexdigest()
    
    cursor.execute(sql_requests.sql_auth(user, encode_password))
    data = cursor.fetchone()
    try:
        user_id, name = data
    except TypeError:
        return 'Access denied', 403
    
    encoded_jwt = jwt.encode({"name": name, "user_id": user_id}, 
                             SECRET_KEY, 
                             algorithm="HS256")
    return jsonify({"access_token":encoded_jwt})

# INSERT
@app.route('/cars/', methods=["POST"])
def insert():
    body = request.get_json()
    try:
        cursor.execute(sql_requests.sql_insert(body))
    except (errors.UniqueViolation):
        return 'Not unique value', 400    
        
    connect.commit()
    return '', 201

# GET
@app.route('/cars/', methods=["GET"])
def fetch_all():
    cars = []
    cursor.execute(sql_requests.sql_get())
    data = cursor.fetchall()
    
    for row in data:
        car_id, car_name, car_country, car_auto_kpp = row
        cars.append({
            "id": car_id,
            "name": car_name,
            "country": car_country,
            "auto_kpp": car_auto_kpp
        })
        
    return jsonify({"data": cars})

# RETRIEVE
@app.route('/cars/<car_id>/', methods=["GET"])
def fetch(car_id):
    cursor.execute(sql_requests.sql_retrieve(car_id))
    data = cursor.fetchone()
    try:
        car_id, car_name, car_country, car_auto_kpp = data
    except TypeError:
        return 'Not found', 404
    
    return jsonify({"data": {
        "id": car_id,
        "name": car_name,
        "country": car_country,
        "auto_kpp": car_auto_kpp
    }})
    
# UPDATE
@app.route('/cars/<car_id>/', methods=["POST"])
def update(car_id):
    body = request.get_json()
    cursor.execute(sql_requests.sql_update(car_id, body))
    connect.commit()
    
    return '', 201

# DELETE
@app.route('/cars/<car_id>/', methods=["DELETE"])
def delete(car_id):
    cursor.execute(sql_requests.sql_delete(car_id))
    connect.commit()
    return '', 204

if __name__ == '__main__':
    app.run(host='0.0.0.0')