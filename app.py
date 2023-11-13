from flask import Flask
from flask_basicauth import BasicAuth
from tasks import tasks_bp, init_app

app = Flask(__name__)
app.config['BASIC_AUTH_USERNAME'] = 'username'
app.config['BASIC_AUTH_PASSWORD'] = 'password'
app.config['BASIC_AUTH_FORCE'] = True

basic_auth = BasicAuth(app)
init_app(app)
app.register_blueprint(tasks_bp)

if __name__ == '__main__':
    app.run(debug=True)
