# Import knihoven a modulů
from flask import Flask
from app.routes.install import install
from app.routes.update import update
from app.routes.upgrade import upgrade
from app.routes.remove import remove
from app.routes.list import list
from app.routes.search import search
import ssl

# Inicializace Flask frameworku
app = Flask(__name__)

# Registrace blueprintů
app.register_blueprint(install)
app.register_blueprint(update)
app.register_blueprint(upgrade)
app.register_blueprint(remove)
app.register_blueprint(list)
app.register_blueprint(search)

# Spuštění aplikace
if __name__ == '__main__':
    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    context.load_cert_chain('cert.pem', 'key.pem')
    app.run(debug=True, ssl_context=context)

    
