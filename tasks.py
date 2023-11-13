from dataclasses import dataclass
from flask import Blueprint, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_basicauth import BasicAuth

tasks_bp = Blueprint('tasks', __name__)
db = SQLAlchemy()
basic_auth = BasicAuth()


@dataclass
class Task(db.Model):
    id: int
    title: str
    description: str
    done: bool

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255), default="")
    done = db.Column(db.Boolean, default=False)


def init_app(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['BASIC_AUTH_USERNAME'] = 'username'
    app.config['BASIC_AUTH_PASSWORD'] = 'password'
    app.config['BASIC_AUTH_FORCE'] = True

    basic_auth.init_app(app)
    db.init_app(app)

    with app.app_context():
        db.create_all()


@tasks_bp.route('/todo/api/v1.0/tasks', methods=['GET'])
@basic_auth.required
def get_tasks_route():
    tasks = Task.query.all()
    return jsonify({'tasks': [task for task in tasks]})


@tasks_bp.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['GET'])
@basic_auth.required
def get_task_route(task_id):
    task = Task.query.get(task_id)
    if task is None:
        return jsonify({'error': 'Not found'}), 404
    return jsonify({'task': task})


@tasks_bp.route('/todo/api/v1.0/tasks', methods=['POST'])
@basic_auth.required
def create_task_route():
    data = request.json
    if 'title' not in data:
        return jsonify({'error': 'Bad request'}), 400

    new_task = Task(title=data['title'], description=data.get('description', ""))
    db.session.add(new_task)
    db.session.commit()

    return jsonify({'task': new_task}), 201


@tasks_bp.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['DELETE'])
@basic_auth.required
def delete_task_route(task_id):
    task = Task.query.get(task_id)
    if task is None:
        return jsonify({'error': 'Not found'}), 404

    db.session.delete(task)
    db.session.commit()

    return jsonify({'result': True})


@tasks_bp.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['PUT'])
@basic_auth.required
def update_task_route(task_id):
    task = Task.query.get(task_id)
    if task is None:
        return jsonify({'error': 'Not found'}), 404

    data = request.json
    if 'title' in data:
        task.title = data['title']
    if 'description' in data:
        task.description = data['description']
    if 'done' in data:
        task.done = data['done']

    db.session.commit()

    return jsonify({'task': task})


@tasks_bp.route('/todo/api/v1.0/tasks/<int:task_id>/toggle', methods=['PATCH'])
@basic_auth.required
def toggle_task_route(task_id):
    task = Task.query.get(task_id)
    if task is None:
        return jsonify({'error': 'Not found'}), 404

    if not task.done:
        task.done = True
        db.session.commit()
        return jsonify({'result': 'Task is set to done'})
    else:
        return jsonify({'error': 'Task is already done'}), 400
