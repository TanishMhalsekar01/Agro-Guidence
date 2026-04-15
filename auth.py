"""
auth.py — MongoDB Authentication Module for Agro Guidance
Handles user registration and login with bcrypt password hashing.
"""

import bcrypt
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError, ConnectionFailure

MONGO_URI = "mongodb+srv://tanishmhalsekar999_db_user:60FFpomMZXEOy7Dj@cluster0.ffgfoyu.mongodb.net/?appName=Cluster0"
DB_NAME = "agro_guidance"
USERS_COLLECTION = "users"

_client = None
_db = None


def get_db():
    """Return a cached MongoDB database connection."""
    global _client, _db
    if _db is None:
        _client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=8000)
        _db = _client[DB_NAME]
        # Ensure unique index on username and email
        _db[USERS_COLLECTION].create_index("username", unique=True)
        _db[USERS_COLLECTION].create_index("email", unique=True)
    return _db


def register_user(first_name: str, last_name: str, username: str, email: str, password: str) -> dict:
    """
    Register a new user.
    Returns {"success": True, "message": "..."} or {"success": False, "message": "..."}
    """
    username = username.strip().lower()
    email = email.strip().lower()

    if not all([first_name, last_name, username, email, password]):
        return {"success": False, "message": "All fields are required."}

    if len(password) < 6:
        return {"success": False, "message": "Password must be at least 6 characters."}

    try:
        db = get_db()
        collection = db[USERS_COLLECTION]

        hashed_pw = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

        user_doc = {
            "first_name": first_name.strip(),
            "last_name": last_name.strip(),
            "username": username,
            "email": email,
            "password": hashed_pw,
        }

        collection.insert_one(user_doc)
        return {"success": True, "message": "Account created successfully! Please log in."}

    except DuplicateKeyError as e:
        err_str = str(e)
        if "username" in err_str:
            return {"success": False, "message": "Username already taken. Please choose another."}
        if "email" in err_str:
            return {"success": False, "message": "An account with this email already exists."}
        return {"success": False, "message": "Duplicate entry detected."}
    except ConnectionFailure:
        return {"success": False, "message": "Cannot connect to the database. Check your internet connection."}
    except Exception as exc:
        return {"success": False, "message": f"Unexpected error: {exc}"}


def login_user(username: str, password: str) -> dict:
    """
    Verify username and password.
    Returns {"success": True, "user": {...}} or {"success": False, "message": "..."}
    """
    username = username.strip().lower()

    if not username or not password:
        return {"success": False, "message": "Username and password are required."}

    try:
        db = get_db()
        collection = db[USERS_COLLECTION]

        user = collection.find_one({"username": username})
        if not user:
            return {"success": False, "message": "Invalid username or password."}

        if bcrypt.checkpw(password.encode("utf-8"), user["password"]):
            return {
                "success": True,
                "user": {
                    "username": user["username"],
                    "first_name": user["first_name"],
                    "last_name": user["last_name"],
                    "email": user["email"],
                },
            }
        else:
            return {"success": False, "message": "Invalid username or password."}

    except ConnectionFailure:
        return {"success": False, "message": "Cannot connect to the database. Check your internet connection."}
    except Exception as exc:
        return {"success": False, "message": f"Unexpected error: {exc}"}
