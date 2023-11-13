from flask import Flask
from flask_basicauth import BasicAuth
from tasks import tasks_bp, init_app

app = Flask(__name__)

basic_auth = BasicAuth(app)
init_app(app)
app.register_blueprint(tasks_bp)

if __name__ == '__main__':
    app.run(debug=True)
