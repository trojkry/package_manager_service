from flask import Flask
from app.routes import execute

app = Flask(__name__)

app.register_blueprint(execute.bp)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
