from django.urls import path
from . import views
urlpatterns = [
    path("", views.task_list),
    path("add/", views.add_task, name="add_task"),
    path("api/tasks/", views.task_api),
    path("api/tasks/<int:task_id>/", views.task_api),
]