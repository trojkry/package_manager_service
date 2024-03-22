from flask import Flask
from app.routes.install import install
from app.routes.update import update
from app.routes.upgrade import upgrade


app = Flask(__name__)

app.register_blueprint(install)
app.register_blueprint(update)
app.register_blueprint(upgrade)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
