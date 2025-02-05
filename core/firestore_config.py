import firebase_admin
from firebase_admin import credentials, firestore

# Use the application default credentials.
cred = credentials.ApplicationDefault()

firebase_admin.initialize_app(cred)
db = firestore.client()

MOVIES_COLLECTION = "movies"

movies_ref = db.collection("MOVIES_COLLECTION")
