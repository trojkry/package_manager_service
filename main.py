# importy
from flask import Flask
from app.routes import install, update, uninstall, status, dependencies, list

# Vytvoření instance Flask aplikace
app = Flask(__name__)

# Přidání blueprintů (modulů) pro jednotlivé části API
app.register_blueprint(install.bp)
app.register_blueprint(list.bp)
#app.register_blueprint(update.bp)
#app.register_blueprint(uninstall.bp)
#app.register_blueprint(status.bp)
#app.register_blueprint(dependencies.bp)

# Spuštění aplikace
if __name__ == '__main__':
    app.run(debug=True)
