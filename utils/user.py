import jwt
import bcrypt
from decouple import config
from datetime import datetime, timedelta

def check_password(password, hash):
    return bcrypt.checkpw(password.encode("utf-8"), hash.encode("utf-8"))

def generate_token(user_id, user_type):
    try:
        payload = {
            "exp": datetime.utcnow() + timedelta(days=7),
            "iat": datetime.utcnow(),
            "sub": user_id,
            "type": user_type
        }
        return jwt.encode(payload, config("SECRET_KEY"), algorithm="HS256")
    except Exception as e:
        print(f"Error generating token: {e}")
        return None

def get_user_type(token):
    try:
        payload = jwt.decode(token, config("SECRET_KEY"), algorithms=["HS256"])
        return payload["type"]
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
    except Exception as e:
        print(e)
        return None

def get_user_id(token):
    try:
        payload = jwt.decode(token, config("SECRET_KEY"), algorithms=["HS256"])
        return payload["sub"]
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
    except Exception as e:
        print(e)
        return None