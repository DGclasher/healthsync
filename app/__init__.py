from flask import Flask
from decouple import config
from utils import collection

app = Flask(__name__)

app.secret_key = config("SECRET_KEY") 

try:
    print(collection.create_doctor_collection("doctors"))
    print(collection.create_patient_collection("patients"))
except Exception as e:
    print(e)
    pass

from app import views