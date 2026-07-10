import firebase_admin
from firebase_admin import credentials, db, messaging
import requests
from requests.adapters import HTTPAdapter
from urllib3.util import Retry

# 1. OPTIMIZACIÓN: Connection Pooling para peticiones HTTP a Firebase
firebase_session = requests.Session()

# Estrategia de reintentos por si falla la red en Render
retries = Retry(total=3, backoff_factor=0.5, status_forcelist=[500, 502, 503, 504])

# Mantenemos hasta 10 conexiones HTTP abiertas en el Pool para mayor velocidad
adapter = HTTPAdapter(pool_connections=10, pool_maxsize=10, max_retries=retries)
firebase_session.mount('https://', adapter)


# 2. INICIALIZACIÓN: Conexión segura al Admin SDK
if not firebase_admin._apps:
    # Este es el archivo JSON que ya configuraste en tu raíz junto a manage.py
    cred = credentials.Certificate("firebase-credentials.json")
    
    # ¡URL ACTUALIZADA con tu proyecto real de Firebase!
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://unitux-c7b8b-default-rtdb.firebaseio.com/'
    })


# 3. FIREBASE NOTIFICATIONS: Función para enviar alertas en segundo plano
def enviar_notificacion_push(token_dispositivo, titulo, cuerpo):
    """ Envía alertas al celular o navegador del usuario usando Firebase Cloud Messaging """
    try:
        mensaje = messaging.Message(
            notification=messaging.Notification(
                title=titulo,
                body=cuerpo,
            ),
            token=token_dispositivo,
        )
        response = messaging.send(mensaje)
        return response
    except Exception as e:
        print(f"Error enviando notificación: {e}")
        return None