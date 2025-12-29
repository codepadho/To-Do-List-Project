from http import HTTPStatus
from django.test import TestCase, Client
from django.db import connection
import json

class TaskAPITest(TestCase):
    @classmethod
    def setUpTestData(cls):
        with connection.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS tasks (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    title VARCHAR(255) NOT NULL,
                    description TEXT,
                    priority TEXT,
                    due_date DATE NOT NULL,
                    status VARCHAR(50),
                    is_deleted TINYINT(1) DEFAULT 0)""")

    def setUp(self):
        self.client = Client()

    #----------------------- POST -------------------
    def test_create_task(self):
        response = self.client.post(
            "/api/tasks/",
            data=json.dumps({
                "title": "Test Task",
                "description": "Testing",
                "priority": "High",
                "due_date": "2025-12-31",
                "status": "Pending"
            }),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 201)

    #------------------------ Check Validation Error ----------------
    def test_create_task_validation_fail(self):
        response = self.client.post(
            "/api/tasks/",
            data=json.dumps({
                "validation_check": "No title",
                "due_date": "2025-12-31"
            }),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

    #---------------------- GET -------------------
    def test_get_tasks(self):
        response = self.client.get("/api/tasks/")
        self.assertEqual(response.status_code, 200)

    def test_get_single_task(self):
        response = self.client.get("/api/tasks/1/")
        self.assertEqual(response.status_code, HTTPStatus.OK)

    # ---------- PUT ----------
    def test_update_task(self):
        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO tasks (title, due_date) VALUES ('Old Task', '2025-12-31')")
        response = self.client.put(
            "/api/tasks/1/",
            data=json.dumps({
                "title": "Updated Task",
                "due_date": "2025-01-10"
            }),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
