import hashlib
import hmac
import os
from functools import wraps
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired
from flask import request, jsonify


# Secret key for signing tokens (should be kept secret in production)
SECRET_KEY = os.environ.get("SECRET_KEY", "development_secret_key")

# Serializer for generating and verifying tokens
serializer = URLSafeTimedSerializer(SECRET_KEY)


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
makes a signed token with the user ID as the payload.
the Frontend hides the token and stores it in Authentication header.

"""


def generate_token(user_id: str) -> str:
    return serializer.dumps({"user_id": user_id})


"""
verifies the token and extracts the user ID from it.

the Header request should include the token in the Authentication header as "Bearer <token>".
"""


def get_user_id_from_request():
    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        return None

    token = auth_header.replace("Bearer ", "").strip()

    try:

        # max_age is the token expiration time in seconds (e.g., 3600 for 1 hour)
        # Token valid for 24 hours
        payload = serializer.loads(token, max_age=60 * 60 * 24)
        return payload.get("user_id")
    except (BadSignature, SignatureExpired):
        return None


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
