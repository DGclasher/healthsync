from flask import Flask
from flask_cors import CORS
from flask_mail import Mail
from decouple import config
from utils import collection

app = Flask(__name__)
CORS(app)
   
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = config("MAIL_USERNAME")
app.config['MAIL_PASSWORD'] = config("MAIL_PASSWORD")
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.mail = Mail(app) 

app.secret_key = config("SECRET_KEY") 

try:
    print(collection.create_patient_collection("patients"))
    print(collection.create_prescription_collection("prescriptions"))
    print(collection.create_doctor_collection("doctors"))
except Exception as e:
    print(e)
    pass
 
from app import views