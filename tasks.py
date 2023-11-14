# Import necessary modules and classes
from dataclasses import dataclass
from flask import Blueprint, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_basicauth import BasicAuth

# Create a Blueprint for tasks
tasks_bp = Blueprint('tasks', __name__)

# Create a SQLAlchemy instance for database operations
db = SQLAlchemy()

# Create a BasicAuth instance for basic authentication
basic_auth = BasicAuth()

# Define a data class for the Task model
@dataclass
class Task(db.Model):
    # Define attributes for the Task model
    id: int
    title: str
    description: str
    done: bool

    # Define database columns for the Task model
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255), default="")
    done = db.Column(db.Boolean, default=False)

# Function to initialize the Flask app
def init_app(app):
    # Configure the database URI and other settings
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['BASIC_AUTH_USERNAME'] = 'username'
    app.config['BASIC_AUTH_PASSWORD'] = 'password'
    app.config['BASIC_AUTH_FORCE'] = True

    # Initialize BasicAuth and SQLAlchemy with the app
    basic_auth.init_app(app)
    db.init_app(app)

    # Create database tables within the app context
    with app.app_context():
        db.create_all()

# Route to get all tasks
@tasks_bp.route('/todo/api/v1.0/tasks', methods=['GET'])
@basic_auth.required
def get_tasks_route():
    # Retrieve all tasks from the database
    tasks = Task.query.all()
    return jsonify({'tasks': [task for task in tasks]})

# Route to get a specific task by ID
@tasks_bp.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['GET'])
@basic_auth.required
def get_task_route(task_id):
    # Retrieve a task by its ID from the database
    task = Task.query.get(task_id)
    if task is None:
        return jsonify({'error': 'Not found'}), 404
    return jsonify({'task': task})

# Route to create a new task
@tasks_bp.route('/todo/api/v1.0/tasks', methods=['POST'])
@basic_auth.required
def create_task_route():
    # Extract JSON data from the request
    data = request.json
    # Check if 'title' is present in the data
    if 'title' not in data:
        return jsonify({'error': 'Bad request'}), 400

    # Create a new task and add it to the database
    new_task = Task(title=data['title'], description=data.get('description', ""))
    db.session.add(new_task)
    db.session.commit()

    return jsonify({'task': new_task}), 201

# Route to delete a task by ID
@tasks_bp.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['DELETE'])
@basic_auth.required
def delete_task_route(task_id):
    # Retrieve a task by its ID from the database
    task = Task.query.get(task_id)
    if task is None:
        return jsonify({'error': 'Not found'}), 404

    # Delete the task from the database
    db.session.delete(task)
    db.session.commit()

    return jsonify({'result': True})

# Route to update a task by ID
@tasks_bp.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['PUT'])
@basic_auth.required
def update_task_route(task_id):
    # Retrieve a task by its ID from the database
    task = Task.query.get(task_id)
    if task is None:
        return jsonify({'error': 'Not found'}), 404

    # Extract JSON data from the request
    data = request.json
    # Update task attributes based on the data
    if 'title' in data:
        task.title = data['title']
    if 'description' in data:
        task.description = data['description']
    if 'done' in data:
        task.done = data['done']

    # Commit the changes to the database
    db.session.commit()

    return jsonify({'task': task})

# Route to toggle the 'done' status of a task
@tasks_bp.route('/todo/api/v1.0/tasks/<int:task_id>/toggle', methods=['PATCH'])
@basic_auth.required
def toggle_task_route(task_id):
    # Retrieve a task by its ID from the database
    task = Task.query.get(task_id)
    if task is None:
        return jsonify({'error': 'Not found'}), 404

    # Toggle the 'done' status of the task and commit the change
    if not task.done:
        task.done = True
        db.session.commit()
        return jsonify({'result': 'Task is set to done'})
    else:
        return jsonify({'error': 'Task is already done'}), 400
