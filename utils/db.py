import bcrypt
from bson import ObjectId
from pymongo import errors
from decouple import config
from datetime import datetime
from pymongo import MongoClient

client = MongoClient(config("MONGO_URI"))
db = client[config("MONGO_DB")]
doctor_collection = db["doctors"]
patient_collection = db["patients"]
prescription_collection = db["prescriptions"]

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


def create_patient(name, phone, email, password, dob, sex):
    try:
        pw_hash = bcrypt.hashpw(password.encode("utf-8"), salt.encode("utf-8"))
        dob_datetime = datetime.strptime(dob, "%Y-%m-%d")
        created_patient = patient_collection.insert_one({
            "name": name,
            "phone": phone,
            "email": email,
            "password": pw_hash.decode("utf-8"),
            "created_at": datetime.now(),
            "dob": dob_datetime,
            "sex": sex
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

def get_doctor_by_id(id):
    try:
        doctor = doctor_collection.find_one({"_id":ObjectId(id)})
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

def get_patient_by_id(id):
    try:
        patient = patient_collection.find_one({"_id":ObjectId(id)})
        if patient:
            patient["_id"] = str(patient["_id"])
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
        doctor_collection.find_one_and_update(
            {"_id": ObjectId(doctor_id)},
            {"$set": {"is_available": is_available}}
        )
        return True
    except errors.PyMongoError as e:
        print(e)
        return False

# Prescription Handling
def create_prescription(doctor_id, patient_id, diagnosis, medication):
    try:
        created_prescription = prescription_collection.insert_one({
            "doctor_id": ObjectId(doctor_id),
            "patient_id": ObjectId(patient_id),
            "diagnosis": diagnosis,
            "medication": medication,
            "created_at": datetime.now()
        })
        prescription = prescription_collection.find_one(
            {"_id": created_prescription.inserted_id})
        prescription["_id"] = str(prescription["_id"])
        prescription["doctor_id"] = str(prescription["doctor_id"])
        prescription["patient_id"] = str(prescription["patient_id"])
        return prescription
    except errors.PyMongoError as e:
        print(e)
        return False
    
def get_prescriptions_by_patient(patient_id):
    try:
        prescription_cursor = prescription_collection.find(
            {"patient_id": ObjectId(patient_id)},
        )
        prescriptions = list(prescription_cursor)
        for prescription in prescriptions:
            prescription["_id"] = str(prescription["_id"])
            prescription["doctor_id"] = str(prescription["doctor_id"])
            prescription["patient_id"] = str(prescription["patient_id"])
        return prescriptions
    except errors.PyMongoError as e:
        print(e)
        return None

def get_prescriptions_by_doctor(doctor_id):
    try:
        prescription_cursor = prescription_collection.find(
            {"doctor_id": ObjectId(doctor_id)},
        )
        prescriptions = list(prescription_cursor)
        for prescription in prescriptions:
            prescription["_id"] = str(prescription["_id"])
            prescription["doctor_id"] = str(prescription["doctor_id"])
            prescription["patient_id"] = str(prescription["patient_id"])
        return prescriptions
    except errors.PyMongoError as e:
        print(e)
        return None

def get_prescription_by_id(prescription_id):
    try:
        prescription = prescription_collection.find_one(
            {"_id": ObjectId(prescription_id)}
        )
        if prescription:
            prescription["_id"] = str(prescription["_id"])
            prescription["doctor_id"] = str(prescription["doctor_id"])
            prescription["patient_id"] = str(prescription["patient_id"])
            return prescription
        return False
    except errors.PyMongoError as e:
        print(e)
        return None
