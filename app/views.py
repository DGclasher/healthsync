import os
import re
from app import app
import pandas as pd
from utils import calls
from utils import user, db
from flask import jsonify, request

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
    print(user_obj)
    if not user_obj:
        return jsonify({"message": "Invalid credentials"}), 400
    if not user.check_password(password, user_obj["password"]):
        return jsonify({"message": "Invalid credentials"}), 400
    user_obj["_id"] = str(user_obj["_id"])
    user_obj.pop("password")
    token = user.generate_token(str(user_obj["_id"]), "doctor")
    return jsonify({"token": token, "data":user_obj}), 200

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
    if not user_obj:
        return jsonify({"message": "User does not exist"}), 400
    if not user.check_password(password, user_obj["password"]):
        return jsonify({"message": "Incorrect credentials"}), 400
    token = user.generate_token(str(user_obj["_id"]), "patient")
    user_obj["_id"] = str(user_obj["_id"])
    user_obj.pop("password")
    return jsonify({"token": token, "data":user_obj}), 200

@app.route('/register/patient', methods=['POST'])
def register_patient():
    data = request.get_json()
    if not data:
        return jsonify({"message": "No input data provided"}), 400
    name = data.get("name")
    phone = data.get("phone")
    email = data.get("email")
    password = data.get("password")
    sex = data.get("sex")
    dob = data.get("dob")
    if not name or not phone or not email or not password or not sex or not dob:
        return jsonify({"message": "No input data provided"}), 400
    if db.get_patient_by_email(email):
        return jsonify({"message": "User already exists"}), 400
    created_patient = db.create_patient(name, phone, email, password, dob, sex)
    if not created_patient:
        return jsonify({"message": "Error creating user"}), 500
    created_patient["_id"] = str(created_patient["_id"])
    token = user.generate_token(created_patient["_id"], "patient")
    return jsonify({"message": "User created successfully", "data": created_patient, "token": token}), 201


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
    return jsonify({"message": "Doctor created successfully", "data": created_doctor, "token": token}), 201

@app.route('/analyze_disease', methods=['POST'])
async def analyze_disease():
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return jsonify({"message": "Missing authorization header"}), 400
    auth_token = auth_header.split(" ")[1]
    try:
        user_type = user.get_user_type(auth_token)
        if user_type is None:
            return jsonify({"message": "Invalid token"}), 401
        if user_type != "patient":
            return jsonify({"message": "Unauthorized"}), 403
    except Exception as e:
        print(e)
        return jsonify({"message": "Invalid token"}), 401
    try:
        image = request.files.get("image")
        symptoms = request.form.get("symptoms")
        speciality = ""
        res=""
        if image and symptoms:
            res = calls.analyze_both(image, symptoms)
            speciality = res["answer"]
        if image and not symptoms:
            res = calls.analyze_image_only(image)
            speciality = res["answer"]
        if symptoms and not image:
            res = calls.analyze_symptoms(symptoms)
            speciality = res["answer"]
        speciality = re.sub(r'[^\w\s]', '', speciality)
        sp_list = speciality.split(" ")
        print(sp_list)
        d_set = set()
        for sp in sp_list:
            if sp!="":
                doctors = db.get_available_doctors(sp)
                if doctors:
                    for doctor in doctors:
                        d_set.add(tuple(doctor.items()))
        d_list = [dict(doctor_tuple) for doctor_tuple in d_set]
        return jsonify({"message": "Success", "specialist": speciality, "doctors": d_list}), 200
    except Exception as e:
        print(e)
        return jsonify({"message": "Error", "error":str(e)}), 500

@app.route('/connect_doctor', methods=['POST'])
def connect():
    data = request.get_json()
    if not data or "doctor_id" not in data or "availability" not in data:
        return jsonify({"message": "No input data provided"}), 400
    res = db.set_doctor_availability(data.get("doctor_id"), True if data.get("availability") else False)
    if res:
        return jsonify({"message": "Success"}), 200
    return jsonify({"message": "Error"}), 500

@app.route('/recommend_drug', methods=['POST'])
def search():
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return jsonify({"message": "Missing authorization header"}), 400
    auth_token = auth_header.split(" ")[1]
    try:
        user_type = user.get_user_type(auth_token)
        if user_type is None:
            return jsonify({"message": "Invalid token"}), 401
    except Exception as e:
        print(e)
        return jsonify({"message": "Invalid token"}), 401
    medical_condition = request.json.get('medical_condition')
    file_path = os.path.join(os.getcwd(), 'app', 'drugs_for_common_treatments.csv')
    df = pd.read_csv(file_path)
    if 'medical_condition' in df.columns:
        mask = df['medical_condition'].str.contains(medical_condition, case=False)
        result_df = df[mask]
        if not result_df.empty:
            drug_names = result_df['drug_name'].tolist()
            return jsonify({'medical_condition': medical_condition, 'drug_names': drug_names})
        else:
            return jsonify({'error': f'No drugs found for "{medical_condition}".'})
    else:
        return jsonify({'error': 'Column "medical_condition" not found in the CSV file.'})

@app.route('/create_prescription', methods=['POST'])
def create_prescription():
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return jsonify({"message": "Missing authorization header"}), 400
    auth_token = auth_header.split(" ")[1]
    user_type = user.get_user_type(auth_token)
    if user_type != "doctor":
        return jsonify({"message": "Unauthorized"}), 403
    data = request.get_json()
    try:
        patient_id = data.get("patient_id")
        doctor_id = user.get_user_id(auth_token)
        if not doctor_id:
            return jsonify({"message": "Invalid token"}), 401
        diagnosis = data.get("diagnosis")
        medication = data.get("medication")
        created_prescription = db.create_prescription(doctor_id, patient_id, diagnosis, medication)
        if created_prescription:
            return jsonify({"message": "Success", "data": created_prescription}), 201
        return jsonify({"message": "Error"}), 500
    except Exception as e:
        print(e)
        return jsonify({"message": "Error"}), 500

@app.route('/get_my_prescriptions', methods=['GET'])
def get_my_prescriptions():
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return jsonify({"message": "Missing authorization header"}), 400
    auth_token = auth_header.split(" ")[1]
    user_type = user.get_user_type(auth_token)
    if user_type == "patient":
        user_id = user.get_user_id(auth_token)
        prescriptions = db.get_prescriptions_by_patient(user_id)
        return jsonify({"message": "Success", "data": prescriptions}), 200
    elif user_type == "doctor":
        user_id = user.get_user_id(auth_token)
        prescriptions = db.get_prescriptions_by_doctor(user_id)
        return jsonify({"message": "Success", "data": prescriptions}), 200
    else:
        return jsonify({"message": "Unauthorized"}), 403
    