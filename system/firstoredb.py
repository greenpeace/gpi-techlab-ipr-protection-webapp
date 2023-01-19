from flask import current_app as app
from firebase_admin import credentials, firestore
import firebase_admin
from system.setenv import project_id

# initialize firebase sdk
CREDENTIALS = credentials.ApplicationDefault()
firebase_admin.initialize_app(
    CREDENTIALS,
    {
        "projectId": project_id,
    },
)

# Initialize Firestore DB
db = firestore.client()

# Initialize Firestore DB
# Brand IPR firestore collection
brandlinkdetails_ref = db.collection("illegalmerchandise")
# Brand IPR firestore collection
brandlinks_ref = db.collection("searchlinks")
# Brand IPR firestore collection
brandsearchquery_ref = db.collection("searchquery")
# Brand IPR firestore collection
brandstopwords_ref = db.collection("searchquerykeywords")
# Fake News firestore collection
users_ref = db.collection("Users")
# Fake News firestore collection
Settings_ref = db.collection("Settings")
