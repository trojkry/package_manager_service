from flask import Flask
from app.routes.install import install  

app = Flask(__name__)

app.register_blueprint(install)  

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
