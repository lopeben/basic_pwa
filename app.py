# app.py
import ssl
import platform

from flask import Flask, render_template
from flask_socketio import SocketIO

def is_mac():
    return platform.system() == 'Darwin'

app = Flask(__name__)

if is_mac():
    socketio = SocketIO(app, logger=True, engineio_logger=True) # Use this when debugging in mac
else:
    socketio = SocketIO(app, async_mode='gevent', logger=True, engineio_logger=True, connectionStateRecovery={'maxDisconnectionDuration': 2 * 60 * 1000, 'skipMiddlewares': True})


@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':

    if is_mac(): # Debug setting WSGI
        socketio.run(app, debug=True, host='0.0.0.0', port=443, ssl_context=('cert.pem', 'key.pem'), allow_unsafe_werkzeug=True)
    else:
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        context.minimum_version = ssl.TLSVersion.TLSv1_3  # Ensure TLS 1.3 is used
        context.load_cert_chain(certfile='fullchain.pem', keyfile='server.key')
        socketio.run(app, debug=True, host='0.0.0.0', port=443, ssl_context=context)
