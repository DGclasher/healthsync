from decouple import config
from pymongo import MongoClient

client = MongoClient(config("MONGO_URI"))
db = client[config("MONGO_DB")]


def create_doctor_collection(collection_name):
    res = db.create_collection(collection_name, validator={
        '$jsonSchema': {
            'bsonType': 'object',
            'required': ['name', 'speciality', 'phone', 'email', 'password', 'is_available', 'created_at'],
            'properties': {
                'name': {
                    'bsonType': 'string',
                    'description': 'must be a string and is required'
                },
                'phone': {
                    'bsonType': 'string',
                    'description': 'must be a string and is required'
                },
                'email': {
                    'bsonType': 'string',
                    'description': 'must be a string and is required',
                    'uniqueItems': True
                },
                'speciality': {
                    'bsonType': 'string',
                    'description': 'must be a string and is required'
                },
                'password': {
                    'bsonType': 'string',
                    'description': 'must be a string and is required'
                },
                'is_available': {
                    'bsonType': 'bool',
                    'description': 'must be a boolean'
                },
                'created_at': {
                    'bsonType': 'date',
                    'description': 'must be a date and is required'
                }
            }
        }
    })
    return res


def create_patient_collection(collection_name):
    res = db.create_collection(collection_name, validator={
        '$jsonSchema': {
            'bsonType': 'object',
            'required': ['name', 'phone', 'email', 'password', 'created_at'],
            'properties': {
                'doctors")name': {
                    'bsonType': 'string',
                    'description': 'must be a string and is required'
                },
                'phone': {
                    'bsonType': 'string',
                    'description': 'must be a string and is required'
                },
                'email': {
                    'bsonType': 'string',
                    'description': 'must be a string and is required',
                    'uniqueItems': True
                },
                'password': {
                    'bsonType': 'string',
                    'description': 'must be a string and is required'
                },
                'created_at': {
                    'bsonType': 'date',
                    'description': 'must be a date and is required'
                }
            }
        }
    })
    return res
