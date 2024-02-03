from flask import Flask
from flask_cors import CORS
from decouple import config
from utils import collection

app = Flask(__name__)
CORS(app)

app.secret_key = config("SECRET_KEY") 

try:
    print(collection.create_patient_collection("patients"))
    print(collection.create_prescription_collection("prescriptions"))
    print(collection.create_doctor_collection("doctors"))
except Exception as e:
    print(e)
    pass
 
from app import views