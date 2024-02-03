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
            'required': ['name', 'phone', 'email', 'password', 'created_at', 'dob', 'sex'],
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
                'password': {
                    'bsonType': 'string',
                    'description': 'must be a string and is required'
                },
                'created_at': {
                    'bsonType': 'date',
                    'description': 'must be a date and is required'
                },
                'dob': {
                    'bsonType': 'date',
                    'description': 'must be a date and is required'
                },
                'sex': {
                    'bsonType': 'string',
                    'description': 'must be a string and is required'
                }
            }
        }
    })
    return res


def create_prescription_collection(collection_name):
    res = db.create_collection(collection_name, validator={
        '$jsonSchema': {
            'bsonType': 'object',
            'required': ['patient_id', 'doctor_id', 'diagnosis', 'medication', 'created_at'],
            'properties': {
                'patient_id': {
                    'bsonType': 'objectId',
                    'description': 'must be an objectId and is required'
                },
                'doctor_id': {
                    'bsonType': 'objectId',
                    'description': 'must be an objectId and is required'
                },
                'diagnosis': {
                    'bsonType': 'string',
                    'description': 'must be a string and is required'
                },
                'medication': {
                    'bsonType': 'array',
                    'description': 'must be an array and is required',
                    'items': {
                        'bsonType': 'object',
                        'required': ['name', 'dosage', 'instructions'],
                        'properties': {
                            'name': {
                                'bsonType': 'string',
                                'description': 'must be a string and is required'
                            },
                            'dosage': {
                                'bsonType': 'string',
                                'description': 'must be a string and is required'
                            },
                            'instructions': {
                                'bsonType': 'string',
                                'description': 'must be a string and is required'
                            }
                        }
                    }
                },
                'created_at': {
                    'bsonType': 'date',
                    'description': 'must be a date and is required'
                }
            }
        }
    })

    return res