import requests
import os
from dotenv import load_dotenv

load_dotenv()

def firebase_auth(email, password):
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={os.getenv('FIREBASE_API_KEY')}"
    response = requests.post(url, json={
        "email": email,
        "password": password,
        "returnSecureToken": True
    })
    return response.json()

def firebase_config():
    return {
        "apiKey": os.getenv("FIREBASE_API_KEY"),
        "authDomain": os.getenv("FIREBASE_AUTH_DOMAIN"),
        "projectId": os.getenv("FIREBASE_PROJECT_ID"),
        "storageBucket": os.getenv("FIREBASE_STORAGE_BUCKET")
    }