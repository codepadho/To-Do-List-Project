# Django Task Manager (Raw SQL)
A Django-based Task Manager application using **Raw SQL (No ORM)** with both API and Template-based UI.

## Features
- Create, Read, Update, Delete tasks
- RESTful API (CRUD)
- Raw SQL (No Django ORM)
- Django Templates UI
- Soft delete support
- Logging & Error Handling
- Pytest test cases

# Installation and setup
## clone Repo
- git clone

## Create virtual Environment 
- python3.11 -m env env

## Activate Environment 
- source env/bin/activate             #For Linux

## Install Dependencies 
- pip install -r requirements.txt


## Database Table
- CREATE TABLE tasks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    due_date DATE NOT NULL,
    priority VARCHAR(20),
    status VARCHAR(20),
    is_deleted TINYINT(1) DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);


## API Endpoints

- GET | /api/tasks/ | Get all tasks |
- GET | /api/tasks/<id>/ | Get task by ID |
- POST | /api/tasks/ | Create task |
- PUT | /api/tasks/<id>/ | Update task |
- DELETE | /api/tasks/<id>/ | Delete task |

## Template URLs

Add Task: http://127.0.0.1:8000/add/

Task List: http://127.0.0.1:8000/

## Run Project
python manage.py runserver

## Sample POST Request
```json
{
  "title": "Separate Task",
  "description": "To create TO-DO-LIST",
  "priority": "high",
  "due_date": "2025-12-31",
  "status": "pending"
}
