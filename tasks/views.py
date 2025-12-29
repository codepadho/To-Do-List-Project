from http import HTTPStatus

from django.shortcuts import render, redirect
import logging
import json
from .db import get_connection
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
# Create your views here.

logger = logging.getLogger(__name__)

#---------------------------------------- API --------------------------------
@csrf_exempt
def task_api(request, task_id=None):
    connection = get_connection()
    cursor = connection.cursor()
    try:
        #-----------------GET----------
        if request.method == 'GET':
            if task_id:
                cursor.execute('SELECT * FROM tasks WHERE id = %s AND is_deleted=0', (task_id,))
                row = cursor.fetchone()
                if not row:
                    return JsonResponse({'msg': 'Task not found'}, status=HTTPStatus.NOT_FOUND)
                return JsonResponse({'id': row[0],
                                     'title':row[1],
                                     'description':row[2],
                                     'due_date':row[3],
                                     'priority':row[4],
                                     'status':row[5]
                                     },status=HTTPStatus.OK)
            else:
                cursor.execute('SELECT * FROM tasks WHERE is_deleted=0')
                task = cursor.fetchall()
                data = []
                for row in task:
                    data.append(
                        {
                        "id": row[0],
                        "title": row[1],
                        "description": row[2],
                        "due_date": row[3],
                        "priority": row[4],
                        "status": row[5],
                        }
                    )
                return JsonResponse(data, safe=False)
        #-------------------POST---------------------
        elif request.method == 'POST':
            data = json.loads(request.body)
            title=data.get('title')
            due_date = data.get('due_date')
            if not title or not due_date:
                return JsonResponse({'message': 'Title and Due date is required'}, status=HTTPStatus.BAD_REQUEST)
            description=data.get('description')
            priority=data.get('priority')
            status=data.get('status')
            try:
                cursor.execute("INSERT INTO tasks (title, description, due_date, priority, status) VALUES (%s, %s, %s, %s, %s)",
                               (title, description, due_date, priority, status))
            except Exception as e:
                logger.exception("Table Not Exist")
                return JsonResponse({'msg': 'Internal server error'}, status=500)
            connection.commit()
            return JsonResponse({'msg':'Task created'}, status=201)
        #------------------PUT----------------
        elif request.method == 'PUT':
            if not task_id:
                return JsonResponse({'msg':'Task ID required'}, status=400)
            data = json.loads(request.body)
            title=data.get('title')
            if not title:
                return JsonResponse({'message': 'Title is required'}, status=400)
            description=data.get('description')
            due_date=data.get('due_date')
            if not due_date:
                return JsonResponse({'message': 'Due date is required'}, status=400)
            priority=data.get('priority')
            status=data.get('status')
            cursor.execute("UPDATE tasks SET title=%s, description=%s, due_date=%s, priority=%s, status =%s WHERE id = %s AND is_deleted = 0",
                           (title, description, due_date, priority, status, task_id))
            if cursor.rowcount == 0:
                return JsonResponse({'msg':'Task not found or deleted'}, status=HTTPStatus.NOT_FOUND)
            connection.commit()
            return JsonResponse({'msg':'Task updated'}, status=200)
        #---------------------DELETE----------------
        elif request.method == 'DELETE':
            if not task_id:
                return JsonResponse({'msg':'Task ID required'}, status=400)
            cursor.execute("UPDATE tasks SET is_deleted=1 WHERE id = %s", (task_id,))
            connection.commit()
            return JsonResponse({'msg':'Task deleted'}, status=200)
        return JsonResponse({'msg':'Invalid Reaquest'}, status=400)

    except Exception as e:
        logger.error(f"Error something went wrong: {e}", exc_info=True)
        return JsonResponse({'msg':'Internal server error'}, status=500)
    finally:
        connection.close()

#--------------------------- TEMPLATE PART -------------------------
def task_list(request):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM tasks WHERE is_deleted=0")
    task = cursor.fetchall()
    connection.close()
    return render(request, "tasks/list.html", {'tasks': task})

def add_task(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description=request.POST.get('description')
        due_date=request.POST.get('due_date')
        priority = request.POST.get('priority')
        status=request.POST.get('status')

        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("INSERT INTO tasks (title, description, due_date, priority, status) VALUES (%s, %s, %s, %s, %s)",
                       (title, description, due_date, priority, status),
                       )
        connection.commit()
        connection.close()
        return redirect('/')
    return render(request, "tasks/add.html")

