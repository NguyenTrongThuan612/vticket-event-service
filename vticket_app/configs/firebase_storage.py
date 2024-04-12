from django.conf import settings
from firebase_admin import credentials, initialize_app

cred = credentials.Certificate(settings.FIREBASE_ACCOUNT_CERTIFICATE)
initialize_app(
    cred, 
    {
        "storageBucket": "vticket-1ccb9.appspot.com"
    }
)