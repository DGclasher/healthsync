import os
import json
import aiohttp
import requests
from app import app
from utils import user, db
from decouple import config
from flask import jsonify, current_app, request


@app.route('/')
def home():
    return jsonify({'message': 'Hello, World!'})


@app.route('/login/doctor', methods=['POST'])
def login():
    data = request.get_json()
    if not data:
        return jsonify({"message": "No input data provided"}), 400
    email = data.get("email")
    password = data.get("password")
    if not email or not password:
        return jsonify({"message": "No input data provided"}), 400
    user_obj = db.get_doctor_by_email(email)
    if not user:
        return jsonify({"message": "User does not exist"}), 400
    if not user.check_password(password, user_obj["password"]):
        return jsonify({"message": "Incorrect password"}), 400
    token = user.generate_token(str(user_obj["_id"]), "doctor")
    return jsonify({"token": token})


@app.route('/login/patient', methods=['POST'])
def login_patient():
    data = request.get_json()
    if not data:
        return jsonify({"message": "No input data provided"}), 400
    email = data.get("email")
    password = data.get("password")
    if not email or not password:
        return jsonify({"message": "No input data provided"}), 400
    user_obj = db.get_patient_by_email(email)
    if not user:
        return jsonify({"message": "Incorrect credentials"}), 400
    if not user.check_password(password, user_obj["password"]):
        return jsonify({"message": "Incorrect credentials"}), 400
    token = user.generate_token(str(user_obj["_id"]), "patient")
    return jsonify({"token": token})


@app.route('/register/patient', methods=['POST'])
def register_patient():
    data = request.get_json()
    if not data:
        return jsonify({"message": "No input data provided"}), 400
    name = data.get("name")
    phone = data.get("phone")
    email = data.get("email")
    password = data.get("password")
    if not name or not phone or not email or not password:
        return jsonify({"message": "No input data provided"}), 400
    if db.get_patient_by_email(email):
        return jsonify({"message": "User already exists"}), 400
    created_patient = db.create_patient(name, phone, email, password)
    if not created_patient:
        return jsonify({"message": "Error creating user"}), 500
    created_patient["_id"] = str(created_patient["_id"])
    token = user.generate_token(created_patient["_id"], "patient")
    return jsonify({"message": "User created successfully", "data": created_patient, "token":token}), 201


@app.route('/register/doctor', methods=['POST'])
def register_doctor():
    data = request.get_json()
    if not data:
        return jsonify({"message": "No input data provided"}), 400
    name = data.get("name")
    speciality = data.get("speciality")
    phone = data.get("phone")
    email = data.get("email")
    password = data.get("password")
    if not name or not speciality or not phone or not email or not password:
        return jsonify({"message": "No input data provided"}), 400
    if db.get_doctor_by_email(email):
        return jsonify({"message": "User already exists"}), 400
    created_doctor = db.create_doctor(name, speciality, phone, email, password)
    if not created_doctor:
        return jsonify({"message": "Error creating user"}), 500
    created_doctor["_id"] = str(created_doctor["_id"])
    token = user.generate_token(created_doctor["_id"], "doctor")
    return jsonify({"message": "Doctor created successfully", "data": created_doctor, "token":token}), 201


@app.route('/validate_json', methods=['GET'])
def validate_json():
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return jsonify({"message": "Missing authorization header"}), 400

    try:
        auth_token = auth_header.split(" ")[1]
        user_type = user.get_user_type(auth_token)
        if user_type is None:
            return jsonify({"message": "Invalid token"}), 401
        else:
            return jsonify({"message": "Valid token", "user_type": user_type}), 200
    except Exception as e:
        print(e)
        return jsonify({"message": "Invalid token"}), 401


@app.route('/predict', methods=['POST'])
async def predict_disease():
    data = request.get_json()
    if not data:
        return jsonify({"message": "No input data provided"}), 400
    symptoms = data.get("symptoms")
    if not symptoms:
        return jsonify({"message": "No input data provided"}), 400
    endpoint = "https://api-inference.huggingface.co/models/timpal0l/mdeberta-v3-base-squad2"
    headers = {
        "Authorization": f"Bearer {config('AI_API_KEY')}",
    }
    context_path = os.path.join(os.getcwd(), 'app', 'context.txt')
    with open(context_path, 'r') as f:
        context = f.read()
    payload = {
        "inputs": {
            "question": symptoms,
            "context": context
        }
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(endpoint, headers=headers, json=payload) as response:
            try:
                res = await response.text()
                return jsonify({"message": "Success", "data": json.loads(res)}), 200
            except Exception as e:
                return jsonify({"message": "Error", "data": str(e)}), 500

def get_available_doctors(speciality):
    doctors = db.get_available_doctors(speciality)
    return doctors

@app.route('/analyze_image', methods=['POST'])
def analyze_image():
    image = request.files.get("image")
    endpoint = "https://api-inference.huggingface.co/models/Salesforce/blip-image-captioning-large"
    headers = {
        "Authorization": f"Bearer {config('AI_API_KEY')}",
    }
    res = requests.post(endpoint, headers=headers, data=image)
    res = json.loads(res.text)
    generated_text = res[0]["generated_text"]
    r = requests.post("http://localhost:5000/predict", json={"symptoms": generated_text})
    r = json.loads(r.text)
    speciality = r["data"]["answer"]
    print(speciality)
    speciality = speciality.split(" ")[0]
    print(speciality)
    docs = get_available_doctors(speciality)
    return jsonify({"message": "Success", "data":res, "specialist":r, "doctors":docs}), 200