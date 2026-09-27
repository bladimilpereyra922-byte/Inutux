import os


def firebase_config(request):
    return {
        "FIREBASE_API_KEY": os.environ.get("FIREBASE_WEB_API_KEY", ""),
        "FIREBASE_AUTH_DOMAIN": os.environ.get("FIREBASE_AUTH_DOMAIN", ""),
        "FIREBASE_PROJECT_ID": os.environ.get("FIREBASE_PROJECT_ID", ""),
    }
