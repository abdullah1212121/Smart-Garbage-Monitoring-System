import firebase_admin
from firebase_admin import credentials

cred = credentials.Certificate("../../Downloads/smart-garbage-monitoring-f4b77-firebase-adminsdk-y7z0f-92477466b7.json")
firebase_admin.initialize_app(cred)