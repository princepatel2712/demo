import firebase_admin
from django.conf import settings
from firebase_admin import credentials

cred = credentials.Certificate(settings.FIREBASE_DIR)
firebase_admin.initialize_app(cred)
