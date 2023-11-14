# To-Do List API Documentation

This API provides basic functionality for managing tasks in a to-do list.

## Authentication

This API uses Basic Authentication. Provide your username and password when making requests.

## Endpoints

### 1. Get All Tasks

- **URL:** `/todo/api/v1.0/tasks`
- **Method:** `GET`
- **Description:** Retrieve a list of all tasks.
- **Authentication:** Required
- **Response:**
  ```json
  {
    "tasks": [
      {
        "id": 1,
        "title": "Buy groceries",
        "description": "Milk, Cheese, Pizza, Fruit, Tylenol",
        "done": false
      },
      {
        "id": 2,
        "title": "Learn Python",
        "description": "Need to find a good Python tutorial on the web",
        "done": false
      }
    ]
  }
  
### 2. Get a Specific Task

- **URL:** `/todo/api/v1.0/tasks/<int:task_id>`
- **Method:** `GET`
- **Description:** Retrieve details of a specific task by providing its `task_id`.
- **Authentication:** Required
- **Response:**
  ```json
  {
    "task": {
      "id": 1,
      "title": "Buy groceries",
      "description": "Milk, Cheese, Pizza, Fruit, Tylenol",
      "done": false
    }
  }

### 3. Create a New Task

- **URL:** `/todo/api/v1.0/tasks`
- **Method:** `POST`
- **Description:** Create a new task by providing the `title` and optional `description` in the request JSON.
- **Authentication:** Required
- **Request:**
  ```json
  {
    "title": "New Task Title",
    "description": "Optional task description"
  }
- **Response:**
  ```json
  {
  "task": {
    "id": 3,
    "title": "New Task Title",
    "description": "Optional task description",
    "done": false
  }

### 4. Update a Task

- **URL:** `/todo/api/v1.0/tasks/<int:task_id>`
- **Method:** `PUT`
- **Description:** Update an existing task by providing the `title`, `description`, and `done` status in the request JSON.
- **Authentication:** Required
- **Request:**
  ```json
  {
    "title": "Updated Task Title",
    "description": "Updated task description",
    "done": true
  }
- **Response:**
  ```json
  {
  "task": {
    "id": 3,
    "title": "Updated Task Title",
    "description": "Updated task description",
    "done": true
  }

### 5. Delete a Task

- **URL:** `/todo/api/v1.0/tasks/<int:task_id>`
- **Method:** `DELETE`
- **Description:** Delete an existing task by providing its `task_id`.
- **Authentication:** Required
- **Response:**
  ```json
  {
    "result": true
  }

### 6. Toggle Task Completion

- **URL:** `/todo/api/v1.0/tasks/<int:task_id>/toggle`
- **Method:** `PATCH`
- **Description:** Toggle the completion status of an existing task from `false` to `true`.
- **Authentication:** Required
- **Response:**
  ```json
  {
    "task": {
      "id": 3,
      "title": "Updated Task Title",
      "description": "Updated task description",
      "done": true
    }
  }

**Note**: Replace '**<int:task_id>**' with the actual ID of the task when making requests.
