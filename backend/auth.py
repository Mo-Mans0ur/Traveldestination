import hashlib
import hmac
import os
from datetime import datetime, timedelta
from functools import wraps

import jwt
from flask import request, jsonify


# Secret key for signing tokens (should be kept secret in production)
SECRET_KEY = os.environ.get("SECRET_KEY", "development_secret_key")
JWT_ALGORITHM = "HS256"
JWT_EXPIRES_SECONDS = 60 * 60 * 24  # 24 hours


"""
makes a password hash (we never store plain text passwords)

we use 

-salt (it uses random data) to make the hash more secure against attacks.
-sha256 algorithm to create the hash.
"""


def hash_password(password: str) -> str:
    salt = os.urandom(16)  # Generate a random salt
    # Combine salt with password
    salted_password = salt + password.encode('utf-8')
    password_hash = hashlib.sha256(salted_password).hexdigest()  # Create hash
    return salt.hex() + ':' + password_hash  # Store salt and hash together


"""
verifies a password against the stored hash.
it extracts the salt from the stored hash, combines it with the provided password, 
and checks if the resulting hash matches the stored hash.
"""


def verify_password(stored_hash: str, plain_password: str) -> bool:
    try:
        salt_hex, saved_hash = stored_hash.split(":", 1)
        salt = bytes.fromhex(salt_hex)
    except Exception:
        # stored_hash is not in the expected format
        return False

    salted_password = salt + plain_password.encode("utf-8")
    candidate_hash = hashlib.sha256(salted_password).hexdigest()

    # Compare only the hash part securely
    return hmac.compare_digest(saved_hash, candidate_hash)


"""
creates a JWT for a user.

we put the user id into the token and set an expiry time.
the frontend stores this token and sends it back in the Authorization header.
"""


def generate_token(user_id: str) -> str:

    now = datetime.utcnow()
    payload = {
        "sub": str(user_id),
        "iat": now,
        "exp": now + timedelta(seconds=JWT_EXPIRES_SECONDS),
    }

    # PyJWT returns a string token in v2+
    token = jwt.encode(payload, SECRET_KEY, algorithm=JWT_ALGORITHM)
    return token


"""
reads the Authorization header, checks the JWT and returns the user id.

if the token is missing, expired or invalid we just return None.
"""


def get_user_id_from_request():
    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        return None

    token = auth_header.replace("Bearer ", "").strip()

    try:
        payload = jwt.decode(token, SECRET_KEY,
                             algorithms=[JWT_ALGORITHM])
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

    # We store the user id in the "sub" (subject) claim
    return payload.get("sub")


"""
decorator to protect routes that require authentication.

if there is no valid token, it returns a 401 Unauthorized response.
"""


def require_auth(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        user_id = get_user_id_from_request()
        if not user_id:
            return jsonify({"error": "Unauthorized"}), 401

        # we put the user_id in the kwargs so the route can access it if needed
        return fn(user_id=user_id, *args, **kwargs)

    return wrapper
