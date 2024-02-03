import bcrypt
from pymongo import errors
from decouple import config
from datetime import datetime
from pymongo import MongoClient

client = MongoClient(config("MONGO_URI"))
db = client[config("MONGO_DB")]
doctor_collection = db["doctors"]
patient_collection = db["patients"]

salt = config("SALT")


def create_doctor(name, speciality, phone, email, password):
    try:
        pw_hash = bcrypt.hashpw(password.encode("utf-8"), salt.encode("utf-8"))
        created_doctor = doctor_collection.insert_one({
            "name": name,
            "speciality": speciality,
            "phone": phone,
            "email": email,
            "password": pw_hash.decode("utf-8"),
            "is_available": True,
            "created_at": datetime.now()
        })
        doctor = doctor_collection.find_one(
            {"_id": created_doctor.inserted_id})
        doctor.pop("password")
        return dict(doctor)
    except errors.PyMongoError as e:
        print(e)
        return False


def create_patient(name, phone, email, password):
    try:
        pw_hash = bcrypt.hashpw(password.encode("utf-8"), salt.encode("utf-8"))
        created_patient = patient_collection.insert_one({
            "name": name,
            "phone": phone,
            "email": email,
            "password": pw_hash.decode("utf-8"),
            "created_at": datetime.now()
        })
        patient = patient_collection.find_one(
            {"_id": created_patient.inserted_id})
        patient.pop("password")
        return dict(patient)
    except errors.PyMongoError as e:
        print(e)
        return False


def get_doctor_by_email(email):
    try:
        doctor = doctor_collection.find_one({"email": email})
        if doctor:
            doctor["_id"] = str(doctor["_id"])
            return doctor
        return False
    except errors.PyMongoError as e:
        print(e)
        return None


def get_patient_by_email(email):
    try:
        patient = patient_collection.find_one({"email": email})
        if patient:
            return patient
        return False
    except errors.PyMongoError as e:
        print(e)
        return None


def get_all_doctors():
    try:
        doctor_cursor = doctor_collection.find()
        doctors = list(doctor_cursor)
        for doctor in doctors:
            doctor.pop("password")
        return doctors
    except errors.PyMongoError as e:
        print(e)
        return None


def get_available_doctors(speciality):
    try:
        doctor_cursor = doctor_collection.find(
            {
                "speciality": {
                    "$regex": speciality, "$options": "i"
                },
                "is_available": True,
            }, {
                "password": 0,
                "created_at": 0,
            })
        doctors = list(doctor_cursor)
        for doctor in doctors:
            doctor["_id"] = str(doctor["_id"])
        return doctors
    except errors.PyMongoError as e:
        print(e)
        return None


def set_doctor_availability(doctor_id, is_available):
    try:
        doctor_collection.update_one(
            {"_id": doctor_id}, {"$set": {"is_available": is_available}})
        return True
    except errors.PyMongoError as e:
        print(e)
        return False
