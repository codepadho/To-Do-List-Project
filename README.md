# Django Task Manager (Raw SQL)
A Django-based Task Manager application using **Raw SQL (No ORM)** with both API and Template-based UI.

## Features
- RESTful API (CRUD)
- Raw SQL (No Django ORM)
- Django Templates UI
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

- GET /api/tasks/
- GET /api/tasks/{id}/
- POST /api/tasks/  
- PUT /api/tasks/{id}/  
- DELETE /api/tasks/{id}/  


## Template URLs

Add Task: http://127.0.0.1:8000/add/

Task List: http://127.0.0.1:8000/

## Run Project
python manage.py runserver
