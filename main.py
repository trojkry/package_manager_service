from flask import Flask
from app.routes.install import install
from app.routes.update import update
from app.routes.upgrade import upgrade
from app.routes.remove import remove
from app.routes.list import list
from app.routes.search import search

app = Flask(__name__)

app.register_blueprint(install)
app.register_blueprint(update)
app.register_blueprint(upgrade)
app.register_blueprint(remove)
app.register_blueprint(list)
app.register_blueprint(search)

if __name__ == '__main__':
    app.run(debug=True)
